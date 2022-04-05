Configuration
=============


General settings
----------------

INVITATION_EXPIRY
*****************

Setting name: ``INVITATIONS_INVITATION_EXPIRY``

Type: Integer

Default: 3

How many days before the invitation expires.

----

CONFIRM_INVITE_ON_GET
*********************

Setting name: ``INVITATIONS_CONFIRM_INVITE_ON_GET``

Type: Boolean

Default: True

If confirmations can be accepted via a `GET` request.

----

ACCEPT_INVITE_AFTER_SIGNUP
**************************

Setting name: ``INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP``

Type: Boolean

Default: False

If ``True``, invitations will be accepted after users finish signup.
If ``False``, invitations will be accepted right after the invitation link is clicked.
Note that this only works with Allauth for now, which means `ACCOUNT_ADAPTER` has to be
``invitations.models.InvitationsAdapter``.

----

GONE_ON_ACCEPT_ERROR
********************

Setting name: ``INVITATIONS_GONE_ON_ACCEPT_ERROR``

Type: Boolean

Default: True

If `True`, return an HTTP 410 GONE response if the invitation key
is invalid, or the invitation is expired or previously accepted when
accepting an invite. If `False`, display an error message and redirect on
errors:

* Redirects to `INVITATIONS_SIGNUP_REDIRECT` on an expired key
* Otherwise, redirects to `INVITATIONS_LOGIN_REDIRECT` on other errors.

----

ALLOW_JSON_INVITES
******************

Setting name: ``INVITATIONS_ALLOW_JSON_INVITES``

Type: Boolean

Default: False

Expose a URL for authenticated posting of invitees

----

SIGNUP_REDIRECT
***************

Setting name: ``INVITATIONS_SIGNUP_REDIRECT``

Type: String

Default: "account_signup"

URL name of your signup URL.

----

LOGIN_REDIRECT
**************

Setting name: ``INVITATIONS_LOGIN_REDIRECT``

Type: String

Default: ``LOGIN_URL`` from Django settings

URL name of your login URL.

----

ADAPTER
*******

Setting name: ``INVITATIONS_ADAPTER``

Type: String

Default: "invitations.adapters.BaseInvitationsAdapter"

Used for custom integrations. Set this to `ACCOUNT_ADAPTER` if using django-allauth.

----

EMAIL_MAX_LENGTH
****************

Setting name: ``INVITATIONS_EMAIL_MAX_LENGTH``

Type: Integer

Default: 254

If set to `None` (the default), invitation email max length will be set up to 254. Set this to an integer value to set up a custome email max length value.

----

EMAIL_SUBJECT_PREFIX
********************

Setting name: ``INVITATIONS_EMAIL_SUBJECT_PREFIX``

Type: String or None

Default: None

If set to `None` (the default), invitation email subjects will be prefixed with the name of the current Site in brackets (such as `[example.com]`). Set this to a string to for a custom email subject prefix, or an empty string for no prefix.

----

INVITATION_MODEL
****************

Setting name: ``INVITATIONS_INVITATION_MODEL``

Type: String

Default: ``invitations.Invitation``

App registry path of the invitation model used in the current project, for customization purposes.

----

INVITE_FORM
***********

Setting name: ``INVITATIONS_INVITE_FORM``

Type: String

Default: ``invitations.forms.InviteForm``

Form class used for sending invites outside admin.

----

ADMIN_ADD_FORM
**************

Setting name: ``INVITATIONS_ADMIN_ADD_FORM``

Type: String

Default: ``invitations.forms.InvitationAdminAddForm``

Form class used for sending invites in admin.

----

ADMIN_CHANGE_FORM
*****************

Setting name: ``INVITATIONS_ADMIN_CHANGE_FORM``

Type: String

Default: ``invitations.forms.InvitationAdminChangeForm``

Form class used for updating invites in admin.

----

CONFIRMATION_URL_NAME
*********************
Setting name: ``INVITATIONS_CONFIRMATION_URL_NAME``

Type: String

Default: "invitations:accept-invite"

Invitation confirmation URL

Allauth related settings
------------------------

INVITATION_ONLY
***************

Setting name: ``INVITATIONS_INVITATION_ONLY``

Type: Boolean

Default: False

If the site is invite only, or open to all (only relevant when using allauth).
