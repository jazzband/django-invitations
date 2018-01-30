from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.utils import timezone

from .app_settings import app_settings


class BaseInvitationManager(models.Manager):

    def all_expired(self):
        return self.filter(self.expired_q())

    def all_valid(self):
        return self.exclude(self.expired_q())

    def expired_q(self):
        sent_threshold = timezone.now() - timedelta(
            days=app_settings.INVITATION_EXPIRY)
        q = Q(accepted=True) | Q(sent__lt=sent_threshold)
        return q

    def delete_expired_confirmations(self):
        self.all_expired().delete()
