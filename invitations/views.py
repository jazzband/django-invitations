import json

from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, View
from django.views.generic.detail import SingleObjectMixin

from .adapters import get_invitations_adapter
from .app_settings import app_settings
from .exceptions import AlreadyAccepted, AlreadyInvited, UserRegisteredEmail
from .forms import CleanEmailMixin
from .signals import invite_accepted
from .utils import get_invitation_model, get_invite_form

Invitation = get_invitation_model()
InviteForm = get_invite_form()


class SendInvite(FormView):
    template_name = "invitations/forms/_invite.html"
    form_class = InviteForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        try:
            invite = form.save(email)
            invite.inviter = self.request.user
            invite.save()
            invite.send_invitation(self.request)
        except Exception:
            return self.form_invalid(form)
        return self.render_to_response(
            self.get_context_data(
                success_message=_("%(email)s has been invited") % {"email": email},
            ),
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class SendJSONInvite(View):
    http_method_names = ["post"]

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if app_settings.ALLOW_JSON_INVITES:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        status_code = 400
        invitees = json.loads(request.body.decode())
        response = {"valid": [], "invalid": []}
        if isinstance(invitees, list):
            for invitee in invitees:
                try:
                    validate_email(invitee)
                    CleanEmailMixin().validate_invitation(invitee)
                    # ^as a read-only check it does not change old entries as needed:
                    invalid_invitations = Invitation.objects.all().exclude(
                        pk__in=Invitation.objects.all_valid()
                    )
                    target_invitation = invalid_invitations.filter(
                        email__iexact=invitee
                    )
                    if target_invitation:
                        target_invitation.get().delete()  # email is unique, .get works
                    invite = Invitation.create(invitee)
                except (ValueError, KeyError):
                    pass
                except ValidationError:
                    response["invalid"].append({invitee: "invalid email"})
                except AlreadyAccepted:
                    response["invalid"].append({invitee: "already accepted"})
                except AlreadyInvited:
                    response["invalid"].append({invitee: "pending invite"})
                except UserRegisteredEmail:
                    response["invalid"].append({invitee: "user registered email"})
                else:
                    invite.inviter = self.request.user
                    invite.save()
                    invite.send_invitation(request)
                    response["valid"].append({invitee: "invited"})

        if response["valid"]:
            status_code = 201

        return HttpResponse(
            json.dumps(response),
            status=status_code,
            content_type="application/json",
        )


class AcceptInvite(SingleObjectMixin, View):
    form_class = InviteForm

    def get_signup_redirect(self):
        try:
            signup_redirect = reverse(app_settings.SIGNUP_REDIRECT)
        except NoReverseMatch:
            signup_redirect = app_settings.SIGNUP_REDIRECT
        if next_ := self.request.GET.get(REDIRECT_FIELD_NAME):
            signup_redirect += f"?{REDIRECT_FIELD_NAME}={next_}"
        return signup_redirect

    def get_login_redirect(self):
        try:
            login_redirect = reverse(app_settings.LOGIN_REDIRECT)
        except NoReverseMatch:
            login_redirect = app_settings.LOGIN_REDIRECT
        if next_ := self.request.GET.get(REDIRECT_FIELD_NAME):
            login_redirect += f"?{REDIRECT_FIELD_NAME}={next_}"
        return login_redirect

    def get(self, *args, **kwargs):
        if app_settings.CONFIRM_INVITE_ON_GET:
            return self.post(*args, **kwargs)
        else:
            return HttpResponseNotAllowed(["GET"], _("405 Method Not Allowed"))

    def post(self, *args, **kwargs):
        self.object = invitation = self.get_object()

        # Compatibility with older versions: return an HTTP 410 GONE if there
        # is an error. # Error conditions are: no key, expired key or
        # previously accepted key.
        if app_settings.GONE_ON_ACCEPT_ERROR and (
            not invitation
            or (invitation and (invitation.accepted or invitation.key_expired()))
        ):
            return HttpResponse(status=410)

        # No invitation was found.
        if not invitation:
            # Newer behavior: show an error message and redirect.
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                "invitations/messages/invite_invalid.txt",
            )
            return HttpResponseRedirect(self.get_login_redirect())

        # The invitation was previously accepted, redirect to the login
        # view.
        if invitation.accepted:
            logout(self.request)  # prepare for redirection to login page
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                "invitations/messages/invite_already_accepted.txt",
                {"email": invitation.email},
            )
            # Redirect to login since there's hopefully an account already.
            return HttpResponseRedirect(self.get_login_redirect())

        # The key was expired.
        if invitation.key_expired():
            logout(self.request)  # prepare for redirection to signup page
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                "invitations/messages/invite_expired.txt",
                {"email": invitation.email},
            )
            # Redirect to sign-up since they might be able to register anyway.
            return HttpResponseRedirect(self.get_signup_redirect())

        # The invitation is valid.

        # Log out (if logged in) and clear session. Do this in order to prevent
        # user confusion and to ensure that the sign up page is displayed
        # correctly
        logout(self.request)

        # Mark it as accepted now if ACCEPT_INVITE_AFTER_SIGNUP is False.
        if not app_settings.ACCEPT_INVITE_AFTER_SIGNUP:
            accept_invitation(
                invitation=invitation,
                request=self.request,
                signal_sender=self.__class__,
            )

        get_invitations_adapter().stash_verified_email(self.request, invitation.email)

        return HttpResponseRedirect(self.get_signup_redirect())

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except Invitation.DoesNotExist:
            return None

    def get_queryset(self):
        return Invitation.objects.all()


def accept_invitation(invitation, request, signal_sender):
    invitation.accepted = True
    invitation.save()

    invite_accepted.send(
        sender=signal_sender,
        email=invitation.email,
        request=request,
        invitation=invitation,
    )

    get_invitations_adapter().add_message(
        request,
        messages.SUCCESS,
        "invitations/messages/invite_accepted.txt",
        {"email": invitation.email},
    )


def accept_invite_after_signup(sender, request, user, **kwargs):
    invitation = Invitation.objects.filter(email__iexact=user.email).first()
    if invitation:
        accept_invitation(
            invitation=invitation,
            request=request,
            signal_sender=Invitation,
        )


if app_settings.ACCEPT_INVITE_AFTER_SIGNUP:
    signed_up_signal = get_invitations_adapter().get_user_signed_up_signal()
    signed_up_signal.connect(accept_invite_after_signup)
