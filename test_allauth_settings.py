from test_settings import *  # noqa: F403

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "invitations",
    "tests",
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_ADAPTER = "test_allauth_adapters.TestInvitationsAdapter"

MIDDLEWARE.append("allauth.account.middleware.AccountMiddleware")  # noqa: F405

STATIC_URL = ""
