from django.db import models

from invitations.models import Invitation


class ExampleSwappableInvitation(Invitation):
    additonal_field = models.CharField(max_length=255, blank=True)
