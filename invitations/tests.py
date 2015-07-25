import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from allauth.account.adapter import get_adapter

from .models import Invitation, InvitationsAdapter
from .app_settings import app_settings


class InvitationModelTests(TestCase):

    def setUp(self):
        self.invitation = Invitation.create('email@example.com')

    def test_create_invitation(self):
        assert self.invitation.email == 'email@example.com'
        assert self.invitation.key is not None

    def test_invitation_key_expiry(self):
        self.invitation.sent = timezone.now() - datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY, minutes=1)
        assert self.invitation.key_expired() is True
        self.invitation.sent = timezone.now() - datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY, minutes=-1)
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


class InvitationsViewsTests(TestCase):

    def _create_user_and_login(self):
        user = get_user_model().objects.create(username='flibble', is_active=True)
        user.set_password('password')
        user.save()
        self.client.login(username='flibble', password='password')
        return user

    def test_valid_submission(self):
        self._create_user_and_login()
        resp = self.client.post(
            reverse('invitations:send-invite'), {'email': 'email@example.com'})
        assert resp.status_code == 200
