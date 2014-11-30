from django.views.generic import FormView, View
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect

from braces.views import LoginRequiredMixin, GroupRequiredMixin
from allauth.account.adapter import get_adapter

from .forms import InviteForm
from .models import Invitation
from . import app_settings, signals


class SendInvite(LoginRequiredMixin, GroupRequiredMixin, FormView):
    template_name = 'invitations/forms/_invite.html'
    form_class = InviteForm

    if app_settings.ALLOWED_GROUPS:
        group_required = app_settings.ALLOWED_GROUPS

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        try:
            invite = form.save(email)
            invite.send_invitation(self.request)
        except Exception as e:
            return self.form_invalid(form)

        return self.render_to_response(
            self.get_context_data(
                success_message='%s has been invited' % email))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class AcceptInvite(SingleObjectMixin, View):
    form_class = InviteForm

    def get(self, *args, **kwargs):
        if app_settings.CONFIRM_INVITE_ON_GET:
            return self.post(*args, **kwargs)
        else:
            raise Http404()

    def post(self, *args, **kwargs):
        self.object = invitation = self.get_object()
        invitation.accepted = True
        invitation.save()
        get_adapter().stash_verified_email(self.request, invitation.email)
        
        signals.invite_accepted.send(sender=self.request.user.__class__,
                                     request=self.request,
                                     email=invitation.email)

        get_adapter().add_message(self.request,
                                  messages.SUCCESS,
                                  'invitations/messages/invite_accepted.txt',
                                  {'email': invitation.email})

        return redirect(app_settings.SIGNUP_REDIRECT)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except Invitation.DoesNotExist:
            raise Http404()

    def get_queryset(self):
        return Invitation.objects.all_valid()
