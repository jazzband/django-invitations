from django.contrib import admin

from .models import Invitation


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'sent', 'accepted')
    model = Invitation

admin.site.register(Invitation, InvitationAdmin)
