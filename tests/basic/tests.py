import datetime
import re
import json
from mock import patch

from django.test import Client
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils import timezone
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.models import AnonymousUser

import pytest
from freezegun import freeze_time

from invitations.adapters import (
    BaseInvitationsAdapter, get_invitations_adapter)
from invitations.app_settings import app_settings
from invitations.views import AcceptInvite, SendJSONInvite
from invitations.forms import InviteForm
from .. models import ExampleSwappableInvitation
from invitations.utils import get_invitation_model

Invitation = get_invitation_model()


class TestInvitationModel:

    @freeze_time('2015-07-30 12:00:06')
    def test_create_invitation(self, invitation_a):
        assert invitation_a.email == 'email@example.com'
        assert invitation_a.key
        assert invitation_a.accepted is False
        assert invitation_a.created == datetime.datetime.now()

    def test_invitation_key_expiry(self, invitation_a):
        invitation_a.sent = timezone.now() - datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY, minutes=1)
        assert invitation_a.key_expired() is True

        invitation_a.sent = timezone.now() - datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY, minutes=-1)
        assert invitation_a.key_expired() is False


class TestInvitationsAdapter:

    def test_fetch_adapter(self):
        adapter = get_invitations_adapter()
        assert isinstance(adapter, BaseInvitationsAdapter)

    def test_email_subject_prefix_settings_with_site(self):
        adapter = get_invitations_adapter()
        with patch('invitations.adapters.Site') as MockSite:
            MockSite.objects.get_current.return_value.name = 'Foo.com'
            result = adapter.format_email_subject('Bar')
            assert result == '[Foo.com] Bar'

    @override_settings(
        INVITATIONS_EMAIL_SUBJECT_PREFIX=''
    )
    def test_email_subject_prefix_settings_with_custom_override(self):
        adapter = get_invitations_adapter()
        result = adapter.format_email_subject('Bar')
        assert result == 'Bar'


class TestInvitationsSendView:
    client = Client()

    def test_auth(self):
        response = self.client.post(
            reverse('invitations:send-invite'), {'email': 'valid@example.com'},
            follow=True)

        assert response.status_code == 404

    @pytest.mark.parametrize('email, error', [
        ('invalid@example', 'Enter a valid email address'),
        ('invited@example.com', 'This e-mail address has already been'),
        ('flobble@example.com', 'An active user is'),
    ])
    def test_invalid_form_submissions(
            self, user_a, user_b, invitation_b, email, error):
        self.client.login(username='flibble', password='password')
        resp = self.client.post(
            reverse('invitations:send-invite'), {'email': email})

        form = resp.context_data['form']
        assert error in form.errors['email'][0]

    @freeze_time('2015-07-30 12:00:06')
    def test_valid_form_submission(self, user_a):
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
        url = re.search(
            "(?P<url>/invitations/[^\s]+)", mail.outbox[0].body).group("url")
        assert url == reverse(
            'invitations:accept-invite', kwargs={'key': invitation.key})

    @override_settings(
        INVITATION_MODEL='ExampleSwappableInvitation'
    )
    @freeze_time('2015-07-30 12:00:06')
    def test_valid_form_submission_with_swapped_model(self, user_a):
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
        url = re.search(
            "(?P<url>/invitations/[^\s]+)", mail.outbox[0].body).group("url")
        assert url == reverse(
            'invitations:accept-invite', kwargs={'key': invitation.key})


@pytest.mark.django_db
class TestInvitationsAcceptView:
    client = Client()

    def test_accept_invite_get_is_404(self, settings, invitation_b):
        settings.INVITATIONS_CONFIRM_INVITE_ON_GET = False
        resp = self.client.get(
            reverse(
                'invitations:accept-invite',
                kwargs={'key': invitation_b.key}),
            follow=True)
        assert resp.status_code == 404

    @pytest.mark.parametrize('method', [
        ('get'),
        ('post'),
    ])
    def test_accept_invite_invalid_key(self, method):
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite', kwargs={'key': 'invalidKey'}),
            follow=True)
        assert resp.status_code == 410

    @pytest.mark.parametrize('method', [
        ('get'),
        ('post'),
    ])
    def test_accept_invite_invalid_key_error_disabled(self, settings, method):
        settings.INVITATIONS_GONE_ON_ACCEPT_ERROR = False
        settings.INVITATIONS_LOGIN_REDIRECT = '/login-url/'
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite', kwargs={'key': 'invalidKey'}),
            follow=True)
        assert resp.request['PATH_INFO'] == '/login-url/'

    @pytest.mark.parametrize('method', [
        ('get'),
        ('post'),
    ])
    def test_accept_invite_accepted_key(self, accepted_invitation, method):
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite',
                    kwargs={'key': accepted_invitation.key}), follow=True)
        assert resp.status_code == 410

    @pytest.mark.parametrize('method', [
        ('get'),
        ('post'),
    ])
    def test_accept_invite_accepted_key_error_disabled(
            self, settings, accepted_invitation, method):
        settings.INVITATIONS_GONE_ON_ACCEPT_ERROR = False
        settings.INVITATIONS_LOGIN_REDIRECT = '/login-url/'
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite',
                    kwargs={'key': accepted_invitation.key}), follow=True)
        assert resp.request['PATH_INFO'] == '/login-url/'

    @pytest.mark.parametrize('method', [
        ('get'),
        ('post'),
    ])
    def test_accept_invite_expired_key(
            self, settings, sent_invitation_by_user_a, method):
        settings.INVITATIONS_INVITATION_EXPIRY = 0
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite',
                    kwargs={'key': sent_invitation_by_user_a.key}
                    ), follow=True)
        assert resp.status_code == 410

    @pytest.mark.parametrize('method', [
        ('get'),
        ('post'),
    ])
    def test_accept_invite_expired_key_error_disabled(
            self, sent_invitation_by_user_a, method, settings):
        settings.INVITATIONS_INVITATION_EXPIRY = 0
        settings.INVITATIONS_GONE_ON_ACCEPT_ERROR = False
        settings.INVITATIONS_SIGNUP_REDIRECT = '/signup-url/'
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite',
                    kwargs={'key': sent_invitation_by_user_a.key}
                    ), follow=True)
        assert resp.request['PATH_INFO'] == '/signup-url/'

    @pytest.mark.parametrize('method', [
        ('get'),
        ('post'),
    ])
    def test_accept_invite(
            self, settings, sent_invitation_by_user_a, user_a, method):
        settings.INVITATIONS_SIGNUP_REDIRECT = '/non-existent-url/'
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse('invitations:accept-invite',
                    kwargs={'key': sent_invitation_by_user_a.key}
                    ), follow=True)
        invite = Invitation.objects.get(email='email@example.com')
        assert invite.accepted is True
        assert invite.inviter == user_a
        assert resp.request['PATH_INFO'] == '/non-existent-url/'

    def test_signup_redirect(self, settings, sent_invitation_by_user_a):
        settings.INVITATIONS_SIGNUP_REDIRECT = '/non-existent-url/'
        resp = self.client.post(
            reverse('invitations:accept-invite',
                    kwargs={'key': sent_invitation_by_user_a.key}
                    ), follow=True)
        invite = Invitation.objects.get(email='email@example.com')
        assert invite.accepted is True
        assert resp.request['PATH_INFO'] == '/non-existent-url/'


class TestInvitationSignals:
    client = Client()

    @patch('invitations.signals.invite_url_sent.send')
    def test_invite_url_sent_triggered_correctly(
            self, mock_signal, sent_invitation_by_user_a, user_a):
        invite_url = reverse('invitations:accept-invite',
                             args=[sent_invitation_by_user_a.key])
        request = RequestFactory().get('/')
        invite_url = request.build_absolute_uri(invite_url)

        sent_invitation_by_user_a.send_invitation(request)

        assert mock_signal.called
        assert mock_signal.call_count == 1

        mock_signal.assert_called_with(
            instance=sent_invitation_by_user_a,
            invite_url_sent=invite_url,
            inviter=user_a,
            sender=Invitation,
        )

    @override_settings(
        INVITATIONS_SIGNUP_REDIRECT='/non-existent-url/'
    )
    @patch('invitations.signals.invite_accepted.send')
    def test_invite_invite_accepted_triggered_correctly(
            self, mock_signal, sent_invitation_by_user_a):
        request = RequestFactory().get('/')
        sent_invitation_by_user_a.send_invitation(request)

        self.client.post(
            reverse('invitations:accept-invite',
                    kwargs={'key': sent_invitation_by_user_a.key}
                    ), follow=True)
        assert mock_signal.called
        assert mock_signal.call_count == 1

        assert mock_signal.call_args[1]['email'] == 'email@example.com'
        assert mock_signal.call_args[1]['sender'] == AcceptInvite


class TestInvitationsForm:

    @pytest.mark.parametrize('email, form_validity, errors', [
        ('bogger@example.com', True, None),
        ('accepted@example.com', False, 'has already accepted an invite'),
        ('pending@example.com', False, 'has already been invited'),
        ('flobble@example.com', False, 'active user is using this'),
    ])
    def test_form(
            self, email, form_validity, errors,
            accepted_invitation, pending_invitation, user_b):
        form = InviteForm(data={'email': email})
        if errors:
            assert errors in str(form.errors)
        else:
            assert form.errors == {}
        assert form.is_valid() is form_validity


@pytest.mark.django_db
class TestInvitationsManager:

    def test_managers(
            self, sent_invitation_by_user_a, accepted_invitation,
            expired_invitation, invitation_b):
        valid = Invitation.objects.all_valid().values_list(
            'email', flat=True)
        expired = Invitation.objects.all_expired().values_list(
            'email', flat=True)
        expected_valid = ['email@example.com', 'invited@example.com']
        expected_expired = ['accepted@example.com', 'expired@example.com']

        assert sorted(valid) == sorted(expected_valid)
        assert sorted(expired) == sorted(expected_expired)

    def test_delete_all(self):
        valid = Invitation.objects.all_valid().values_list(
            'email', flat=True)
        Invitation.objects.delete_expired_confirmations()
        remaining_invites = Invitation.objects.all().values_list(
            'email', flat=True)
        assert sorted(valid) == sorted(remaining_invites)


class TestInvitationsJSON:
    client = Client()

    @pytest.mark.parametrize('data, expected, status_code', [
        (['accepted@example.com'],
         {u'valid': [],
          u'invalid': [{u'accepted@example.com': u'already accepted'}]},
         400),
        (['xample.com'],
         {u'valid': [], u'invalid': [{u'xample.com': u'invalid email'}]},
         400),
        ('xample.com',
         {u'valid': [], u'invalid': []},
         400),
        (['pending@example.com'],
         {u'valid': [],
          u'invalid': [{u'pending@example.com': u'pending invite'}]},
         400),
        (['flobble@example.com'],
         {u'valid': [],
          u'invalid': [{u'flobble@example.com': u'user registered email'}]},
         400),
        (['example@example.com'],
         {u'valid': [{u'example@example.com': u'invited'}],
          u'invalid': []},
         201),
    ])
    def test_post(
            self, settings, data, expected, status_code,
            user_a, accepted_invitation,
            pending_invitation, user_b):
        settings.INVITATIONS_ALLOW_JSON_INVITES = True
        self.client.login(username='flibble', password='password')
        response = self.client.post(
            reverse('invitations:send-json-invite'),
            data=json.dumps(data),
            content_type='application/json')

        assert response.status_code == status_code
        assert json.loads(response.content.decode()) == expected

    def test_json_setting(self, user_a):
        self.client.login(username='flibble', password='password')
        response = self.client.post(
            reverse('invitations:send-json-invite'),
            data=json.dumps(['example@example.com']),
            content_type='application/json')

        assert response.status_code == 404

    @override_settings(
        INVITATIONS_ALLOW_JSON_INVITES=True
    )
    def test_anonymous_get(self):
        request = RequestFactory().get(
            reverse('invitations:send-json-invite'),
            content_type='application/json')
        request.user = AnonymousUser()
        response = SendJSONInvite.as_view()(request)

        assert response.status_code == 302

    def test_authenticated_get(self, settings, user_a):
        settings.INVITATIONS_ALLOW_JSON_INVITES = True
        request = RequestFactory().get(
            reverse('invitations:send-json-invite'),
            content_type='application/json')
        request.user = user_a
        response = SendJSONInvite.as_view()(request)

        assert response.status_code == 405


class TestInvitationsAdmin:
    client = Client()

    def test_admin_form_add(self, super_user):
        self.client.login(username='flibble', password='password')
        response = self.client.post(
            reverse('admin:invitations_invitation_add'),
            {'email': 'valid@example.com', 'inviter': super_user.id},
            follow=True)
        invite = Invitation.objects.get(email='valid@example.com')

        assert response.status_code == 200
        assert invite.sent
        assert invite.inviter == super_user

    def test_admin_form_change(self, super_user, invitation_b):
        self.client.login(username='flibble', password='password')
        response = self.client.get(
            reverse('admin:invitations_invitation_change',
                    args=(invitation_b.id,)),
            follow=True)

        assert response.status_code == 200
        fields = list(response.context_data['adminform'].form.fields.keys())
        expected_fields = ['accepted',
                           'key', 'sent', 'inviter', 'email', 'created']
        assert fields == expected_fields
