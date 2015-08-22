import datetime
import re

from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.core import mail

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from freezegun import freeze_time
from nose_parameterized import parameterized

from .models import Invitation, InvitationsAdapter
from .app_settings import app_settings


class InvitationModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        freezer = freeze_time('2015-07-30 12:00:06')
        freezer.start()
        cls.invitation = Invitation.create('email@example.com')
        freezer.stop()

    @classmethod
    def tearDownClass(cls):
        cls.invitation.delete()

    @freeze_time('2015-07-30 12:00:06')
    def test_create_invitation(self):
        assert self.invitation.email == 'email@example.com'
        assert self.invitation.key is not None
        assert self.invitation.accepted is False
        assert self.invitation.created == datetime.datetime.now()

    def test_invitation_key_expiry(self):
        self.invitation.sent = timezone.now() - datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY, minutes=1)
        assert self.invitation.key_expired() is True
        self.invitation.sent = timezone.now() - datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY, minutes=-1)
        assert self.invitation.key_expired() is False


class InvitationsAdapterTests(TestCase):

    @classmethod
    def setUp(cls):
        cls.adapter = get_adapter()
        cls.signup_request = RequestFactory().get(reverse(
            'account_signup', urlconf='allauth.account.urls'))

    @classmethod
    def tearDownClass(cls):
        del cls.adapter

    def test_fetch_adapter(self):
        assert isinstance(self.adapter, InvitationsAdapter)

    def test_adapter_default_signup(self):
        assert self.adapter.is_open_for_signup(self.signup_request) is True

    @override_settings(
        INVITATIONS_INVITATION_ONLY=True
    )
    def test_adapter_invitations_only(self):
        assert self.adapter.is_open_for_signup(self.signup_request) is False
        response = self.client.get(
            reverse('account_signup'))
        assert 'Sign Up Closed' in response.content.decode('utf8')


class InvitationsSendViewTests(TestCase):

    @classmethod
    def setUp(cls):
        cls.user = get_user_model().objects.create_user(
            username='flibble',
            password='password')
        cls.invitation = Invitation.create('invited@example.com')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        Invitation.objects.all().delete()

    def test_auth(self):
        response = self.client.post(
            reverse('invitations:send-invite'), {'email': 'valid@example.com'},
            follow=True)
        assert response.status_code == 200
        assert response.template_name == ['account/login.html']

    @parameterized.expand([
        ('invalid@example', 'Enter a valid email address'),
        ('invited@example.com', 'This e-mail address has already been'),
    ])
    def test_invalid_form_submissions(self, email, error):
        self.client.login(username='flibble', password='password')
        resp = self.client.post(
            reverse('invitations:send-invite'), {'email': email})

        form = resp.context_data['form']
        assert error in form.errors['email'][0]

    @freeze_time('2015-07-30 12:00:06')
    def test_valid_form_submission(self):
        self.client.login(username='flibble', password='password')
        resp = self.client.post(
            reverse('invitations:send-invite'), {'email': 'email@example.com'})
        invitation = Invitation.objects.get(email='email@example.com')

        assert resp.status_code == 200
        assert 'success_message' in resp.context_data.keys()

        assert invitation.sent == datetime.datetime.now()
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to[0] == 'email@example.com'
        assert 'Invitation to join example.com' in mail.outbox[0].subject
        url = re.search("(?P<url>/invitations/[^\s]+)", mail.outbox[0].body).group("url")
        assert url == reverse('invitations:accept-invite', kwargs={'key': invitation.key})


class InvitationsAcceptViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.invitation = Invitation.create('email@example.com')

    @classmethod
    def tearDownClass(cls):
        Invitation.objects.all().delete()

    @override_settings(
        INVITATIONS_CONFIRM_INVITE_ON_GET=False
    )
    def test_accept_invite_get_disabled(self):
        resp = self.client.get(
            reverse('invitations:accept-invite', kwargs={'key': self.invitation.key}),
            follow=True)
        assert resp.status_code == 404

    @parameterized.expand([
        ('get'),
        ('post'),
    ])
    def test_accept_invite_invalid_key(self, method):
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite', kwargs={'key': 'invalidKey'}),
            follow=True)
        assert resp.status_code == 404

    @parameterized.expand([
        ('get'),
        ('post'),
    ])
    def test_accept_invite(self, method):
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite',
                    kwargs={'key': self.invitation.key}), follow=True)
        invite = Invitation.objects.get(email='email@example.com')
        assert invite.accepted is True
        assert resp.request['PATH_INFO'] == reverse('account_signup')

        form = resp.context_data['form']
        assert 'email@example.com' == form.fields['email'].initial
        messages = resp.context['messages']
        message_text = [message.message for message in messages]
        assert message_text == ['Invitation to - email@example.com - has been accepted']

        resp = self.client.post(
            reverse('account_signup'),
            {'email': 'email@example.com',
             'username': 'username',
             'password1': 'password',
             'password2': 'password'
             })

        allauth_email_obj = EmailAddress.objects.get(email='email@example.com')
        assert allauth_email_obj.verified is True

    @override_settings(
        INVITATIONS_SIGNUP_REDIRECT='/non-existent-url/'
    )
    def test_signup_redirect(self):
        resp = self.client.post(
            reverse('invitations:accept-invite',
                    kwargs={'key': self.invitation.key}), follow=True)
        invite = Invitation.objects.get(email='email@example.com')
        assert invite.accepted is True
        assert resp.request['PATH_INFO'] == '/non-existent-url/'
