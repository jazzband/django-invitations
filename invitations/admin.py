from django.contrib import admin

from .utils import (get_invitation_admin_add_form,
                    get_invitation_admin_change_form, get_invitation_model)

Invitation = get_invitation_model()
InvitationAdminAddForm = get_invitation_admin_add_form()
InvitationAdminChangeForm = get_invitation_admin_change_form()


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
