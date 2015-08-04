from django import forms
from django.utils.translation import ugettext_lazy as _
from allauth.account.adapter import get_adapter
from .models import Invitation


class InviteForm(forms.Form):

    email = forms.EmailField(label=_("E-mail"),
                             required=True,
                             widget=forms.TextInput(attrs={"type": "email",
                                                           "size": "30"}))

    def clean_email(self):
        value = self.cleaned_data["email"]
        value = get_adapter().clean_email(value)
        errors = {
            "already_invited": _("This e-mail address has already been"
                                 " invited."),
        }
        if Invitation.objects.filter(email__iexact=value,
                                     accepted=False):
            raise forms.ValidationError(errors["already_invited"])

        return value

    def save(self, email):
        return Invitation.create(email=email)

class InviteModelForm(forms.ModelForm):
    model = Invitation
    email = forms.EmailField(label=_("E-mail"),
                             required=True,
                             widget=forms.TextInput(attrs={"type": "email",
                                                           "size": "30"}))

    class Meta:
        model = Invitation
        fields = '__all__'

    def clean_email(self):
        value = self.cleaned_data["email"]
        value = get_adapter().clean_email(value)
        errors = {
            "this_account": _("This e-mail address is already associated"
                              " with this account."),
            "different_account": _("This e-mail address is already associated"
                                   " with another account."),
        }
        emails = EmailAddress.objects.filter(email__iexact=value)
        if app_settings.UNIQUE_EMAIL:
            if emails.exists():
                raise forms.ValidationError(errors["different_account"])
        errors = {
            "already_invited": _("This e-mail address has already been"
                                 " invited."),
        }
        if Invitation.objects.filter(email__iexact=value,
                                     accepted=False):
            raise forms.ValidationError(errors["already_invited"])
        return value

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        try:
            invite = form.save(email)
            invite.send_invitation(self.request)
        except Exception as e:
            return self.form_invalid(form)
        self.save()
        return super(InviteModelForm, self).form_valid(form)    

    def save(self, *args, **kwargs):
        cleaned_data = super(InviteModelForm, self).clean()
        email = cleaned_data.get("email")
        invite = Invitation.create(email=email)
        invite.send_invitation(self.request)
        self.instance = invite
        super(InviteModelForm, self).save(*args, **kwargs)
        return invite