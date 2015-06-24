import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.adapter import get_adapter

from .managers import InvitationManager
from . import app_settings
from . import signals


@python_2_unicode_compatible
class Invitation(models.Model):

    email = models.EmailField(unique=True, verbose_name=_('e-mail address'))
    accepted = models.BooleanField(verbose_name=_('accepted'), default=False)
    created = models.DateTimeField(verbose_name=_('created'),
                                   default=timezone.now)
    key = models.CharField(verbose_name=_('key'), max_length=64, unique=True)
    sent = models.DateTimeField(verbose_name=_('sent'), null=True)

    objects = InvitationManager()

    @classmethod
    def create(cls, email):
        key = get_random_string(64).lower()
        instance = cls._default_manager.create(
            email=email,
            key=key)
        return instance

    def key_expired(self):
        expiration_date = (
            self.sent + datetime.timedelta(
                days=app_settings.INVITATION_EXPIRY))
        return expiration_date <= timezone.now()
    key_expired.boolean = True

    def send_invitation(self, request, **kwargs):
        current_site = (kwargs['site'] if 'site' in kwargs
                        else Site.objects.get_current())
        invite_url = reverse('invitations:accept-invite',
                             args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)

        ctx = {
            'invite_url': invite_url,
            'current_site': current_site,
            'email': self.email,
            'key': self.key,
        }

        email_template = 'invitations/email/email_invite'

        get_adapter().send_mail(email_template,
                                self.email,
                                ctx)
        self.sent = timezone.now()
        self.save()

        signals.invite_url_sent.send(
            sender=self.__class__,
            instance=self,
            invite_url_sent=invite_url,
            inviter=request.user)

    def __str__(self):
        return u"Invite: {}".format(self.email)


class InvitationsAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        if request.session.get('account_verified_email'):
            mail = request.session.get('account_verified_email')
            return True
        elif app_settings.INVITATION_ONLY is True:
            # Site is ONLY open for invites
            return False
        else:
            # Site is open to signup
            return True
