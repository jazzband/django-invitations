from invitations.app_settings import app_settings

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.test import Client
from django.test.client import RequestFactory

from invitations.adapters import get_invitations_adapter
from invitations.models import InvitationsAdapter
from invitations.utils import get_invitation_model

Invitation = get_invitation_model()


class TestAllAuthIntegrationAcceptAfterSignup:
    client = Client()
    adapter = get_invitations_adapter()

    @pytest.mark.parametrize(
        "method",
        [
            ("get"),
            ("post"),
        ],
    )
    def test_accept_invite_accepted_invitation_after_signup(
        self,
        settings,
        method,
        sent_invitation_by_user_a,
        user_a,
    ):
        settings.INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP = True
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse(
                app_settings.CONFIRMATION_URL_NAME,
                kwargs={"key": sent_invitation_by_user_a.key},
            ),
            follow=True,
        )
        assert resp.status_code == 200

        invite = Invitation.objects.get(email="email@example.com")
        assert invite.inviter == user_a
        assert invite.accepted is False
        assert resp.request["PATH_INFO"] == reverse("account_signup")
        form = resp.context_data["form"]
        assert "email@example.com" == form.fields["email"].initial

        resp = self.client.post(
            reverse("account_signup"),
            {
                "email": "email@example.com",
                "username": "username",
                "password1": "password",
                "password2": "password",
            },
        )
        invite = Invitation.objects.get(email="email@example.com")
        assert invite.accepted is True

    @pytest.mark.parametrize(
        "method",
        [
            ("get"),
            ("post"),
        ],
    )
    def test_invite_accepted_after_signup_with_altered_case_email(
        self,
        settings,
        method,
        sent_invitation_by_user_a,
        user_a,
    ):
        settings.INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP = True
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse(
                app_settings.CONFIRMATION_URL_NAME,
                kwargs={"key": sent_invitation_by_user_a.key},
            ),
            follow=True,
        )

        invite = Invitation.objects.get(email="email@example.com")
        assert invite.accepted is False
        form = resp.context_data["form"]
        assert "email@example.com" == form.fields["email"].initial

        resp = self.client.post(
            reverse("account_signup"),
            {
                "email": "EMAIL@EXAMPLE.COM",
                "username": "username",
                "password1": "password",
                "password2": "password",
            },
        )
        invite = Invitation.objects.get(email="email@example.com")
        assert invite.accepted is True


class TestAllAuthIntegration:
    client = Client()
    adapter = get_invitations_adapter()

    @pytest.mark.parametrize(
        "method",
        [
            ("get"),
            ("post"),
        ],
    )
    def test_accept_invite_allauth(
        self,
        method,
        settings,
        user_a,
        sent_invitation_by_user_a,
    ):
        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse(
                app_settings.CONFIRMATION_URL_NAME,
                kwargs={"key": sent_invitation_by_user_a.key},
            ),
            follow=True,
        )
        invite = Invitation.objects.get(email="email@example.com")
        assert invite.accepted
        assert invite.inviter == user_a
        assert resp.request["PATH_INFO"] == reverse("account_signup")

        form = resp.context_data["form"]
        assert "email@example.com" == form.fields["email"].initial
        messages = resp.context["messages"]
        message_text = [message.message for message in messages]
        assert "Invitation to - email@example.com - has been accepted" in message_text

        resp = self.client.post(
            reverse("account_signup"),
            {
                "email": "email@example.com",
                "username": "username",
                "password1": "password",
                "password2": "password",
            },
        )

        allauth_email_obj = EmailAddress.objects.get(email="email@example.com")
        assert allauth_email_obj.verified is True

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "method",
        [
            ("get"),
            ("post"),
        ],
    )
    def test_accept_invite_with_signup_redirect(
        self, settings, sent_invitation_by_user_a, method
    ):
        client_with_method = getattr(self.client, method)
        next_ = "/foo/bar"
        url = reverse(
            app_settings.CONFIRMATION_URL_NAME,
            kwargs={
                "key": sent_invitation_by_user_a.key,
            },
        )
        resp = client_with_method(f"{url}?{REDIRECT_FIELD_NAME}={next_}")

        assert resp.status_code == 302
        assert (
            resp.url
            == f"{reverse(app_settings.SIGNUP_REDIRECT)}?{REDIRECT_FIELD_NAME}={next_}"
        )

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "method",
        [
            ("get"),
            ("post"),
        ],
    )
    def test_accept_already_accepted_invite_with_login_redirect(
        self, settings, accepted_invitation, method
    ):
        # Disable old behavior (immediately returning a 410 GONE)
        settings.INVITATIONS_GONE_ON_ACCEPT_ERROR = False
        client_with_method = getattr(self.client, method)
        next_ = "/foo/bar"
        url = reverse(
            app_settings.CONFIRMATION_URL_NAME,
            kwargs={
                "key": accepted_invitation.key,
            },
        )
        resp = client_with_method(f"{url}?{REDIRECT_FIELD_NAME}={next_}")

        assert resp.status_code == 302
        assert (
            resp.url == f"{app_settings.LOGIN_REDIRECT}?{REDIRECT_FIELD_NAME}={next_}"
        )

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "method",
        [
            ("get"),
            ("post"),
        ],
    )
    def test_accept_inviter_logged_in(
        self, settings, sent_invitation_by_user_a, method
    ):
        assert self.client.login(username="flibble", password="password")
        admin_resp = self.client.get(reverse("admin:index"), follow=True)
        assert admin_resp.wsgi_request.user.is_authenticated

        client_with_method = getattr(self.client, method)
        resp = client_with_method(
            reverse(
                app_settings.CONFIRMATION_URL_NAME,
                kwargs={"key": sent_invitation_by_user_a.key},
            )
        )
        assert not resp.wsgi_request.user.is_authenticated

    def test_fetch_adapter(self):
        assert isinstance(self.adapter, InvitationsAdapter)

    def test_allauth_signup_open(self):
        signup_request = RequestFactory().get(
            reverse("account_signup", urlconf="allauth.account.urls"),
        )
        assert self.adapter.is_open_for_signup(signup_request) is True

    @pytest.mark.django_db
    def test_allauth_adapter_invitation_only(self, settings):
        settings.INVITATIONS_INVITATION_ONLY = True
        signup_request = RequestFactory().get(
            reverse("account_signup", urlconf="allauth.account.urls"),
        )
        assert self.adapter.is_open_for_signup(signup_request) is False
        response = self.client.get(reverse("account_signup"))
        assert "Sign Up Closed" in response.content.decode("utf8")
