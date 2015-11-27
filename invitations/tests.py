import datetime
import re
import json
from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.contrib.auth.models import AnonymousUser

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from freezegun import freeze_time
from nose_parameterized import parameterized

from .models import Invitation, InvitationsAdapter
from .app_settings import app_settings
from .views import AcceptInvite, SendJSONInvite
from .forms import InviteForm


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
        self.assertEqual(self.invitation.email, 'email@example.com')
        self.assertIsNotNone(self.invitation.key)
        self.assertFalse(self.invitation.accepted)
        self.assertEqual(self.invitation.created, datetime.datetime.now())

    def test_invitation_key_expiry(self):
        self.invitation.sent = timezone.now() - datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY, minutes=1)
        self.assertTrue(self.invitation.key_expired())
        self.invitation.sent = timezone.now() - datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY, minutes=-1)
        self.assertFalse(self.invitation.key_expired())


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
        self.assertIsInstance(self.adapter, InvitationsAdapter)

    def test_adapter_default_signup(self):
        self.assertTrue(self.adapter.is_open_for_signup(self.signup_request))

    @override_settings(
        INVITATIONS_INVITATION_ONLY=True
    )
    def test_adapter_invitations_only(self):
        self.assertFalse(self.adapter.is_open_for_signup(self.signup_request))
        response = self.client.get(
            reverse('account_signup'))
        self.assertIn('Sign Up Closed', response.content.decode('utf8'))


class InvitationsSendViewTests(TestCase):

    @classmethod
    def setUp(cls):
        cls.user = get_user_model().objects.create_user(
            username='flibble',
            password='password')
        cls.existing_user = get_user_model().objects.create_user(
            username='flobble',
            password='password',
            email='flobble@example.com')
        cls.invitation = Invitation.create('invited@example.com')

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()
        Invitation.objects.all().delete()

    def test_auth(self):
        response = self.client.post(
            reverse('invitations:send-invite'), {'email': 'valid@example.com'},
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['account/login.html'])

    @parameterized.expand([
        ('invalid@example', 'Enter a valid email address'),
        ('invited@example.com', 'This e-mail address has already been'),
        ('flobble@example.com', 'An active user is')
    ])
    def test_invalid_form_submissions(self, email, error):
        self.client.login(username='flibble', password='password')
        resp = self.client.post(
            reverse('invitations:send-invite'), {'email': email})

        form = resp.context_data['form']
        self.assertIn(error, form.errors['email'][0])

    @freeze_time('2015-07-30 12:00:06')
    def test_valid_form_submission(self):
        self.client.login(username='flibble', password='password')
        resp = self.client.post(
            reverse('invitations:send-invite'), {'email': 'email@example.com'})
        invitation = Invitation.objects.get(email='email@example.com')

        self.assertEqual(resp.status_code, 200)
        self.assertIn('success_message', resp.context_data.keys())

        self.assertEqual(invitation.sent, datetime.datetime.now())
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], 'email@example.com')
        self.assertIn('Invitation to join example.com', mail.outbox[0].subject)
        url = re.search(
            "(?P<url>/invitations/[^\s]+)", mail.outbox[0].body).group("url")
        self.assertEqual(url, reverse(
            'invitations:accept-invite', kwargs={'key': invitation.key}))


class InvitationsAcceptViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = get_user_model().objects.create_user(
            username='flibble',
            password='password')
        cls.invitation = Invitation.create(
            'email@example.com', inviter=cls.user)

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()
        Invitation.objects.all().delete()

    @override_settings(
        INVITATIONS_CONFIRM_INVITE_ON_GET=False
    )
    def test_accept_invite_get_disabled(self):
        resp = self.client.get(
            reverse(
                'invitations:accept-invite',
                kwargs={'key': self.invitation.key}),
            follow=True)
        self.assertEqual(resp.status_code, 404)

    @parameterized.expand([
        ('get'),
        ('post'),
    ])
    def test_accept_invite_invalid_key(self, method):
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite', kwargs={'key': 'invalidKey'}),
            follow=True)
        self.assertEqual(resp.status_code, 404)

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
        self.assertTrue(invite.accepted)
        self.assertEqual(invite.inviter, self.user)
        self.assertEqual(resp.request['PATH_INFO'], reverse('account_signup'))

        form = resp.context_data['form']
        self.assertEqual('email@example.com', form.fields['email'].initial)
        messages = resp.context['messages']
        message_text = [message.message for message in messages]
        self.assertEqual(
            message_text, [
                'Invitation to - email@example.com - has been accepted'])

        resp = self.client.post(
            reverse('account_signup'),
            {'email': 'email@example.com',
             'username': 'username',
             'password1': 'password',
             'password2': 'password'
             })

        allauth_email_obj = EmailAddress.objects.get(email='email@example.com')
        self.assertTrue(allauth_email_obj.verified)

    @override_settings(
        INVITATIONS_SIGNUP_REDIRECT='/non-existent-url/'
    )
    def test_signup_redirect(self):
        resp = self.client.post(
            reverse('invitations:accept-invite',
                    kwargs={'key': self.invitation.key}), follow=True)
        invite = Invitation.objects.get(email='email@example.com')
        self.assertTrue(invite.accepted)
        self.assertEqual(resp.request['PATH_INFO'], '/non-existent-url/')


class InvitationsSignalTests(TestCase):

    @patch('invitations.signals.invite_url_sent.send')
    def test_invite_url_sent_triggered_correctly(self, mock_signal):
        invite = Invitation.create('email@example.com')
        invite_url = reverse('invitations:accept-invite', args=[invite.key])

        request = RequestFactory().get('/')
        request.user = 'monkey'
        invite_url = request.build_absolute_uri(invite_url)

        invite.send_invitation(request)

        self.assertTrue(mock_signal.called)
        self.assertEqual(mock_signal.call_count, 1)

        mock_signal.assert_called_with(
            instance=invite,
            invite_url_sent=invite_url,
            inviter='monkey',
            sender=Invitation,
        )

        invite.delete()

    @patch('invitations.signals.invite_accepted.send')
    def test_invite_invite_accepted_triggered_correctly(self, mock_signal):
        invite = Invitation.create('email@example.com')
        request = RequestFactory().get('/')
        request.user = 'monkey'
        invite.send_invitation(request)

        self.client.post(
            reverse('invitations:accept-invite',
                    kwargs={'key': invite.key}), follow=True)

        self.assertTrue(mock_signal.called)
        self.assertEqual(mock_signal.call_count, 1)

        self.assertEqual(
            mock_signal.call_args[1]['email'], 'email@example.com')
        self.assertEqual(
            mock_signal.call_args[1]['sender'], AcceptInvite)

        invite.delete()


class InvitationsFormTests(TestCase):

    @classmethod
    def setUp(cls):
        cls.accepted_invite = Invitation.create('already@accepted.com')
        cls.accepted_invite.accepted = True
        cls.accepted_invite.save()
        pending_invite = Invitation.create('pending@example.com')
        pending_invite.sent = timezone.now() - datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY - 1)
        pending_invite.save()
        cls.existing_user = get_user_model().objects.create_user(
            username='flobble',
            password='password',
            email='flobble@example.com')

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()
        Invitation.objects.all().delete()

    @parameterized.expand([
        ('bogger@something.com', True, None),
        ('already@accepted.com', False, 'has already accepted an invite'),
        ('pending@example.com', False, 'has already been invited'),
        ('flobble@example.com', False, 'active user is using this'),
    ])
    def test_form(self, email, form_validity, errors):
        form = InviteForm(data={'email': email})
        if errors:
            assert errors in str(form.errors)
        else:
            self.assertEqual(form.errors, {})
        self.assertEqual(form.is_valid(), form_validity)


class InvitationsManagerTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.invitation1 = Invitation.create('email1@example.com')
        cls.invitation2 = Invitation.create('email2@example.com')
        cls.invitation3 = Invitation.create('email3@example.com')
        cls.invitation4 = Invitation.create('email4@example.com')
        cls.invitation1.accepted = True
        cls.invitation1.save()
        cls.invitation2.sent = timezone.now() - datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY + 1)
        cls.invitation2.save()

    @classmethod
    def tearDownClass(cls):
        Invitation.objects.all().delete()

    def test_managers(self):
        valid = Invitation.objects.all_valid().values_list(
            'email', flat=True)
        expired = Invitation.objects.all_expired().values_list(
            'email', flat=True)
        expected_valid = ['email3@example.com', 'email4@example.com']
        expected_expired = ['email1@example.com', 'email2@example.com']

        self.assertEqual(sorted(valid), sorted(expected_valid))
        self.assertEqual(sorted(expired), sorted(expected_expired))


class InvitationsJSONTests(TestCase):

    @classmethod
    def setUp(cls):
        cls.user = get_user_model().objects.create_user(
            username='flibble',
            password='password')
        cls.accepted_invite = Invitation.create('already@accepted.com')
        cls.accepted_invite.accepted = True
        cls.accepted_invite.save()
        Invitation.create('email3@example.com')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        Invitation.objects.all().delete()

    @parameterized.expand([
        (['already@accepted.com'],
         {u'valid': [],
          u'invalid': [{u'already@accepted.com': u'already accepted'}]},
         400),
        (['xample.com'],
         {u'valid': [], u'invalid': [{u'xample.com': u'invalid email'}]},
         400),
        ('xample.com',
         {u'valid': [], u'invalid': []},
         400),
        (['email3@example.com'],
         {u'valid': [],
          u'invalid': [{u'email3@example.com': u'pending invite'}]},
         400),
        (['example@example.com'],
         {u'valid': [{u'example@example.com': u'invited'}],
          u'invalid': []},
         201),
    ])
    @override_settings(
        INVITATIONS_ALLOW_JSON_INVITES=True
    )
    def test_post(self, data, expected, status_code):
        self.client.login(username='flibble', password='password')
        response = self.client.post(
            reverse('invitations:send-json-invite'),
            data=json.dumps(data),
            content_type='application/json')

        self.assertEqual(response.status_code, status_code)
        self.assertEqual(json.loads(response.content.decode()), expected)

    def test_json_setting(self):
        self.client.login(username='flibble', password='password')
        response = self.client.post(
            reverse('invitations:send-json-invite'),
            data=json.dumps(['example@example.com']),
            content_type='application/json')

        self.assertEqual(response.status_code, 404)

    @override_settings(
        INVITATIONS_ALLOW_JSON_INVITES=True
    )
    def test_anonymous_get(self):
        request = RequestFactory().get(
            reverse('invitations:send-json-invite'),
            content_type='application/json')
        request.user = AnonymousUser()
        response = SendJSONInvite.as_view()(request)

        self.assertEqual(response.status_code, 302)

    @override_settings(
        INVITATIONS_ALLOW_JSON_INVITES=True
    )
    def test_authenticated_get(self):
        request = RequestFactory().get(
            reverse('invitations:send-json-invite'),
            content_type='application/json')
        request.user = self.user
        response = SendJSONInvite.as_view()(request)

        self.assertEqual(response.status_code, 405)
