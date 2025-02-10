from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .utils import (
    get_invitation_admin_add_form,
    get_invitation_admin_change_form,
    get_invitation_model,
)

Invitation = get_invitation_model()
InvitationAdminAddForm = get_invitation_admin_add_form()
InvitationAdminChangeForm = get_invitation_admin_change_form()


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("email", "sent", "accepted")
    autocomplete_fields = ["inviter"]
    actions = ["resend_invitation"]

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            kwargs["form"] = InvitationAdminChangeForm
        else:
            kwargs["form"] = InvitationAdminAddForm
            kwargs["form"].user = request.user
            kwargs["form"].request = request
        return super().get_form(request, obj, **kwargs)

    @admin.action(description=_("Resend invitation"))
    def resend_invitation(self, request, queryset):
        for invitation in queryset:
            invitation.send_invitation(request)
        self.message_user(request, _("Selected invitations have been resent."))
