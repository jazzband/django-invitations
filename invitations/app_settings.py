from django.conf import settings


class AppSettings(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        from django.conf import settings
        return getattr(settings, self.prefix + name, dflt)

    @property
    def INVITATION_EXPIRY(self):
        """ How long before the invitation expires """
        return self._setting('INVITATION_EXPIRY', 3)

    @property
    def INVITATION_ONLY(self):
        """ Signup is invite only """
        return self._setting('INVITATION_ONLY', False)

    @property
    def CONFIRM_INVITE_ON_GET(self):
        """ Simple get request confirms invite """
        return self._setting('CONFIRM_INVITE_ON_GET', True)

    @property
    def ACCEPT_INVITE_AFTER_SIGNUP(self):
        """ Accept the invitation after the user finished signup. """
        return self._setting('ACCEPT_INVITE_AFTER_SIGNUP', False)

    @property
    def GONE_ON_ACCEPT_ERROR(self):
        """
        If an invalid/expired/previously accepted key is provided, return a
        HTTP 410 GONE response.
        """
        return self._setting('GONE_ON_ACCEPT_ERROR', True)

    @property
    def ALLOW_JSON_INVITES(self):
        """ Exposes json endpoint for mass invite creation """
        return self._setting('ALLOW_JSON_INVITES', False)

    @property
    def SIGNUP_REDIRECT(self):
        """ Where to redirect on email confirm of invite """
        return self._setting('SIGNUP_REDIRECT', 'account_signup')

    @property
    def LOGIN_REDIRECT(self):
        """ Where to redirect on an expired or already accepted invite """
        return self._setting('LOGIN_REDIRECT', settings.LOGIN_URL)

    @property
    def ADAPTER(self):
        """ The adapter, setting ACCOUNT_ADAPTER overrides this default """
        return self._setting(
            'ADAPTER', 'invitations.adapters.BaseInvitationsAdapter')

    @property
    def EMAIL_MAX_LENGTH(self):
        """
        Adjust max_length of e-mail addresses
        """
        return self._setting("EMAIL_MAX_LENGTH", 254)

    @property
    def EMAIL_SUBJECT_PREFIX(self):
        """
        Subject-line prefix to use for email messages sent
        """
        return self._setting("EMAIL_SUBJECT_PREFIX", None)

    @property
    def INVITATION_MODEL(self):
        """
        Subject-line prefix to use for Invitation model setup
        """
        return self._setting("INVITATION_MODEL", "invitations.Invitation")

    @property
    def INVITE_FORM(self):
        return self._setting("INVITE_FORM", "invitations.forms.InviteForm")

    @property
    def ADMIN_ADD_FORM(self):
        return self._setting(
            "ADMIN_ADD_FORM",
            "invitations.forms.InvitationAdminAddForm"
        )

    @property
    def ADMIN_CHANGE_FORM(self):
        return self._setting(
            "ADMIN_CHANGE_FORM",
            "invitations.forms.InvitationAdminChangeForm"
        )


app_settings = AppSettings('INVITATIONS_')
