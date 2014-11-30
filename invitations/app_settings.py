class AppSettings(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        from django.conf import settings
        return getattr(settings, self.prefix + name, dflt)

    @property
    def ALLOWED_GROUPS(self):
        """ Users in this group can send invites """
        return self._setting('ALLOWED_GROUPS', None)

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
        return self._setting('CONFIRM_EMAIL_ON_GET', True)

    @property
    def SIGNUP_REDIRECT(self):
        """ Where to redirect on email confirm of invite """
        return self._setting('SIGNUP_REDIRECT', 'account_signup')


import sys
app_settings = AppSettings('INVITATIONS_')
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
