from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils import timezone

from nose_parameterized import parameterized
from allauth.account.models import EmailAddress

from invitations.models import Invitation, InvitationsAdapter
from invitations.adapters import get_invitations_adapter


class AllAuthIntegrationTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = get_user_model().objects.create_user(
            username='flibble',
            password='password')
        cls.invitation = Invitation.create(
            'email@example.com', inviter=cls.user)
        cls.invitation.sent = timezone.now()
        cls.invitation.save()
        cls.adapter = get_invitations_adapter()

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()
        Invitation.objects.all().delete()

    @parameterized.expand([
        ('get'),
        ('post'),
    ])
    def test_accept_invite_allauth(self, method):
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite',
                    kwargs={'key': self.invitation.key}), follow=True)
        invite = Invitation.objects.get(email='email@example.com')
        self.assertTrue(invite.accepted)
        self.assertEqual(invite.inviter, self.user)
        self.assertEqual(
            resp.request['PATH_INFO'], reverse('account_signup'))

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

        allauth_email_obj = EmailAddress.objects.get(
            email='email@example.com')
        self.assertTrue(allauth_email_obj.verified)

    @parameterized.expand([
        ('get'),
        ('post'),
    ])
    @override_settings(
        INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP=True,
    )
    def test_accept_invite_accepted_invitation_after_signup(self, method):
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite',
                    kwargs={'key': self.invitation.key}), follow=True)
        self.assertEqual(resp.status_code, 200)

        invite = Invitation.objects.get(email='email@example.com')
        self.assertEqual(invite.inviter, self.user)
        self.assertFalse(invite.accepted)
        self.assertEqual(
            resp.request['PATH_INFO'], reverse('account_signup'))
        form = resp.context_data['form']
        self.assertEqual('email@example.com', form.fields['email'].initial)

        resp = self.client.post(
            reverse('account_signup'),
            {'email': 'email@example.com',
             'username': 'username',
             'password1': 'password',
             'password2': 'password'
             })
        invite = Invitation.objects.get(email='email@example.com')
        self.assertTrue(invite.accepted)

    def test_fetch_adapter(self):
        self.assertIsInstance(self.adapter, InvitationsAdapter)

    def test_allauth_signup_open(self):
        signup_request = RequestFactory().get(reverse(
            'account_signup', urlconf='allauth.account.urls'))
        self.assertTrue(
            self.adapter.is_open_for_signup(signup_request))

    @override_settings(
        INVITATIONS_INVITATION_ONLY=True,
    )
    def test_allauth_adapter_invitations_only(self):
        signup_request = RequestFactory().get(reverse(
            'account_signup', urlconf='allauth.account.urls'))
        self.assertFalse(
            self.adapter.is_open_for_signup(signup_request))
        response = self.client.get(
            reverse('account_signup'))
        self.assertIn('Sign Up Closed', response.content.decode('utf8'))
