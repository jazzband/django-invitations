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
