from django.contrib import admin

from .models import Invitation
from .forms import InviteModelForm

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'sent', 'accepted')
    form = InviteModelForm

    def get_form(self, request, obj=None, **kwargs):
		form = super(InvitationAdmin, self).get_form(request, **kwargs)
		form.user = request.user
		form.request = request
		return form

admin.site.register(Invitation, InvitationAdmin)