import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils import timezone
from django.core.urlresolvers import reverse

from allauth.account.adapter import get_adapter

from .models import Invitation, InvitationsAdapter
from . import app_settings as inv_app_settings


class InvitationModelTests(TestCase):

    def setUp(self):
        self.invitation = Invitation.create('email@example.com')

    def test_create_invitation(self):
        assert self.invitation.email == 'email@example.com'
        assert self.invitation.key is not None

    def test_invitation_key_expiry(self):
        self.invitation.sent = timezone.now() - datetime.timedelta(
            days=inv_app_settings.INVITATION_EXPIRY, minutes=1)
        assert self.invitation.key_expired() is True
        self.invitation.sent = timezone.now() - datetime.timedelta(
            days=inv_app_settings.INVITATION_EXPIRY, minutes=-1)
        assert self.invitation.key_expired() is False


class InvitationsAdapterTests(TestCase):

    def setUp(self):
        self.adapter = get_adapter()
        self.signup_request = RequestFactory().get(reverse(
            'account_signup', urlconf='allauth.account.urls'))

    def test_fetch_adapter(self):
        assert isinstance(self.adapter, InvitationsAdapter)

    def test_adapter_default_signup(self):
        assert self.adapter.is_open_for_signup(self.signup_request) is True

    @override_settings(
        INVITATIONS_INVITATION_ONLY=True
    )
    def test_adapter_invitations_only(self):
        assert self.adapter.is_open_for_signup(self.signup_request) is False
