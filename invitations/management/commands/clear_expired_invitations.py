from django.core.management.base import BaseCommand

from ...utils import get_invitation_model

Invitation = get_invitation_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        Invitation.objects.delete_expired_confirmations()
