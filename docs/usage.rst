Usage
=====

There are two primary ways to use `django-invitations` described below.

Generic Invitation flow:

* Privileged user invites prospective user by email (via either Django admin, form post, JSON post or programmatically)
* User receives invitation email with confirmation link
* User clicks link and is redirected to a preconfigured url (default is accounts/signup)

Allauth Invitation flow:

* As above but..
* User clicks link, their email is confirmed and they are redirected to signup
* The signup URL has the email prefilled and upon signing up the user is logged into the site

The user can enter any email address they wish when they sign up.
They are not obligated to enter the same email address listed in the invitation.
If ``allauth`` is being used under its default settings, then two ``EmailAddress`` instances will be created for that user, one for the email address used in the invitation, and one for the email address entered by the user.

Further details can be found in the following sections.

Allauth Integration
-------------------

As above but note that invitations must come after allauth in the INSTALLED_APPS

Set the allauth ``ACCOUNT_ADAPTER`` setting

.. code-block:: python

    ACCOUNT_ADAPTER = 'invitations.models.InvitationsAdapter'

Sending Invites
---------------

First import the model:

.. code-block:: python

    from invitations.utils import get_invitation_model
    Invitation = get_invitation_model()

In this version of ``django-invitations``, the ``email`` field in the ``Invitation`` model must be unique.
(Even though email addresses are generally considered case *insensitive*, the unique constraint is case *sensitive*.)
Because of this constraint, it is not possible to create two invitations to the exact same email address, even if the inviters are different users.
We need to handle this case in our code.

.. code-block:: python

    email_address = "Example@example.com"
    invitation = (Invitation.objects
        .filter(email__iexact=email_address)
        .order_by('created')
        .last()
    )
    if invitation is None:
        # Do not use Invitation.objects.create or
        # Invitation.objects.update_or_create, but use Invitation.create
        # instead, because it sets the key to a secure random value
        invitation = Invitation.create(email=email_address)

Then finally send the email out.

.. code-block:: python

    invitation.send_invitation()

To send invites via django admin, just add an invite and save.


Bulk Invites
------------

Bulk invites are supported via JSON.  Post a list of comma separated emails to the dedicated URL and Invitations will return a data object containing a list of valid and invalid invitations.

Signals
-------

The following signals are emitted:

* ``invite_url_sent``
* ``invite_accepted``


Management Commands
-------------------

Expired and accepted invites can be cleared with the ``clear_expired_invitations`` management command:

.. code-block:: sh

    python manage.py clear_expired_invitations
