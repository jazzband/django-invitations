import datetime

import pytest

from django.contrib.auth import get_user_model
from django.utils import timezone

from freezegun import freeze_time

from invitations.utils import get_invitation_model
from invitations.app_settings import app_settings

Invitation = get_invitation_model()


@pytest.fixture
def invitation_a(db):
    freezer = freeze_time('2015-07-30 12:00:06')
    freezer.start()
    inivitation = Invitation.create('email@example.com')
    freezer.stop()
    return inivitation


@pytest.fixture
def invitation_b(db):
    return Invitation.create('invited@example.com')


@pytest.fixture
def user_a(db):
    return get_user_model().objects.create_user(
        username='flibble',
        password='password'
    )


@pytest.fixture
def user_b(db):
    return get_user_model().objects.create_user(
        username='flobble',
        password='password',
        email='flobble@example.com'
    )


@pytest.fixture
def super_user(db):
    return get_user_model().objects.create_superuser(
        username='flibble',
        password='password',
        email='mrflibble@example.com'
    )


@pytest.fixture
def sent_invitation_by_user_a(db, user_a):
    invite = Invitation.create('email@example.com', inviter=user_a)
    invite.sent = timezone.now()
    invite.save()
    return invite


@pytest.fixture
def accepted_invitation(db, user_a):
    invite = Invitation.create('accepted@example.com', inviter=user_a)
    invite.sent = timezone.now()
    invite.accepted = True
    invite.save()
    return invite


@pytest.fixture
def pending_invitation(db, user_a):
    invite = Invitation.create('pending@example.com', inviter=user_a)
    invite.sent = timezone.now() - datetime.timedelta(
        days=app_settings.INVITATION_EXPIRY - 1)
    invite.save()
    return invite


@pytest.fixture
def expired_invitation(db, user_a):
    invite = Invitation.create('expired@example.com')
    invite.sent = timezone.now() - datetime.timedelta(
        days=app_settings.INVITATION_EXPIRY + 1)
    invite.save()
    return invite
