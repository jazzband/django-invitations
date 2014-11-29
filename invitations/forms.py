from django import forms
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import AddEmailForm

from .models import Invitation


class InviteForm(AddEmailForm):

    def clean_email(self):
        value = super(InviteForm, self).clean_email()

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
