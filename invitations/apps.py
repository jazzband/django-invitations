from django.apps import AppConfig


class Config(AppConfig):
    """Config."""

    default_auto_field = "django.db.models.AutoField"
    name = "invitations"
    label = "invitations"
