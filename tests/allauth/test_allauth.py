try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.test import Client

import pytest
from allauth.account.models import EmailAddress

from invitations.models import InvitationsAdapter
from invitations.utils import get_invitation_model
from invitations.adapters import get_invitations_adapter

Invitation = get_invitation_model()


class TestAllAuthIntegrationAcceptAfterSignup:
    client = Client()
    adapter = get_invitations_adapter()

    @pytest.mark.parametrize('method', [
        ('get'),
        ('post'),
    ])
    def test_accept_invite_accepted_invitation_after_signup(
            self, settings, method, sent_invitation_by_user_a, user_a):
        settings.INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP = True
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite',
                    kwargs={'key': sent_invitation_by_user_a.key}
                    ), follow=True)
        assert resp.status_code == 200

        invite = Invitation.objects.get(email='email@example.com')
        assert invite.inviter == user_a
        assert invite.accepted is False
        assert resp.request['PATH_INFO'] == reverse('account_signup')
        form = resp.context_data['form']
        assert 'email@example.com' == form.fields['email'].initial

        resp = self.client.post(
            reverse('account_signup'),
            {'email': 'email@example.com',
             'username': 'username',
             'password1': 'password',
             'password2': 'password'
             })
        invite = Invitation.objects.get(email='email@example.com')
        assert invite.accepted is True


class TestAllAuthIntegration:
    client = Client()
    adapter = get_invitations_adapter()

    @pytest.mark.parametrize('method', [
        ('get'),
        ('post'),
    ])
    def test_accept_invite_allauth(
            self, method, settings, user_a, sent_invitation_by_user_a):
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse(
                'invitations:accept-invite',
                kwargs={'key': sent_invitation_by_user_a.key}
            ), follow=True)
        invite = Invitation.objects.get(email='email@example.com')
        assert invite.accepted
        assert invite.inviter == user_a
        assert resp.request['PATH_INFO'] == reverse('account_signup')

        form = resp.context_data['form']
        assert 'email@example.com' == form.fields['email'].initial
        messages = resp.context['messages']
        message_text = [message.message for message in messages]
        assert (
            'Invitation to - email@example.com - has been accepted' in
            message_text
        )

        resp = self.client.post(
            reverse('account_signup'),
            {'email': 'email@example.com',
             'username': 'username',
             'password1': 'password',
             'password2': 'password'
             })

        allauth_email_obj = EmailAddress.objects.get(
            email='email@example.com')
        assert allauth_email_obj.verified is True

    def test_fetch_adapter(self):
        assert isinstance(self.adapter, InvitationsAdapter)

    def test_allauth_signup_open(self):
        signup_request = RequestFactory().get(reverse(
            'account_signup', urlconf='allauth.account.urls'))
        assert self.adapter.is_open_for_signup(signup_request) is True

    @pytest.mark.django_db
    def test_allauth_adapter_invitations_only(self, settings):
        settings.INVITATIONS_INVITATION_ONLY = True
        signup_request = RequestFactory().get(reverse(
            'account_signup', urlconf='allauth.account.urls'))
        assert self.adapter.is_open_for_signup(signup_request) is False
        response = self.client.get(
            reverse('account_signup'))
        assert 'Sign Up Closed' in response.content.decode('utf8')
