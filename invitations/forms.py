from django import forms
from django.utils.translation import ugettext_lazy as _
from allauth.account.adapter import get_adapter
from .models import Invitation


class CleanEmailMixin(object):

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


class InviteForm(forms.Form, CleanEmailMixin):

    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        widget=forms.TextInput(attrs={"type": "email", "size": "30"}))

    def save(self, email):
        return Invitation.create(email=email)


class InvitationAdminAddForm(forms.ModelForm, CleanEmailMixin):
    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        widget=forms.TextInput(attrs={"type": "email", "size": "30"}))

    def save(self, *args, **kwargs):
        cleaned_data = super(InvitationAdminAddForm, self).clean()
        email = cleaned_data.get("email")
        instance = Invitation.create(email=email)
        instance.send_invitation(self.request)
        super(InvitationAdminAddForm, self).save(*args, **kwargs)
        return instance

    class Meta:
        model = Invitation
        fields = ("email", )


class InvitationAdminChangeForm(forms.ModelForm):

    class Meta:
        model = Invitation
        fields = '__all__'
