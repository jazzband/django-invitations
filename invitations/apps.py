from django.apps import AppConfig


class Config(AppConfig):
    """Config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "invitations"
    label = "invitations"
