##Django-invitations - Invitation integration for django-allauth

[![Build Status](https://travis-ci.org/bee-keeper/django-invitations.svg?branch=devel)](https://travis-ci.org/bee-keeper/django-invitations)

###About
A Django invite app for the excellent [django-allauth](https://github.com/pennersr/django-allauth).  All emails and messages are fully customisable.

Invitation flow:

* Priviledged user invites prospective user by email (either via Django admin or via dedicated form post)
* User receives invitation email with confirmation link
* User clicks link, their email is confirmed and they are redirected to signup
* Confirmed email is prefilled, and upon signing up with their password they are logged into the site


###Installation

```
pip install django-invitations

# Add to settings.py (after all-auth), INSTALLED_APPS
'invitations',

# Add to settings.py, django-allauth setting
ACCOUNT_ADAPTER = 'invitations.models.InvitationsAdapter'

# Append to urls.py
url(r'^invitations/', include('invitations.urls', namespace='invitations')),
```

###Testing

`python manage.py test` or `tox`

###Additional Configuration

**INVITATIONS_INVITATION_EXPIRY** (default=3)

Integer.  How many days before the invitation expires.

**INVITATIONS_INVITATION_ONLY** (default=False)

Boolean.  If the site is invite only, or open to all.

**ALLOW_JSON_INVITES** (default=False)

Expose a URL for authenticated posting of invitees

**INVITATIONS_SIGNUP_REDIRECT** (default='account_signup')

URL name of your signup URL.


###Signals

The following signals are emitted:

* `invite_url_sent`
* `invite_accepted`


###Management Commands
Expired and accepted invites can be cleared as so:

`python manage.py clear_expired_invitations`


###Roadmap

* Add json endpoints
* Add more error messages when sending invitations
* Refactor to make an generic invitations app with pluggable backends
