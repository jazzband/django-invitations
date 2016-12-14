from django.contrib import admin

from .forms import InvitationAdminAddForm, InvitationAdminChangeForm
from .utils import get_invitation_model

Invitation = get_invitation_model()


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'sent', 'accepted')

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            kwargs['form'] = InvitationAdminChangeForm
        else:
            kwargs['form'] = InvitationAdminAddForm
            kwargs['form'].user = request.user
            kwargs['form'].request = request
        return super(InvitationAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Invitation, InvitationAdmin)
