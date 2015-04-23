import datetime

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from models import Invitation
from . import app_settings


@override_settings(
    INVITATIONS_INVITATION_ONLY=True
)
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
    pass
