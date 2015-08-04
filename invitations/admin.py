from django.contrib import admin

from .models import Invitation
from .forms import InvitationAdminAddForm, InvitationAdminChangeForm


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
