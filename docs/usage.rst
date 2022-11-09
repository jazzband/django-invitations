Usage
=====

There are two primary ways to use `django-invitations` described below.

Generic Invitation flow:

* Privileged user invites prospective user by email (via either Django admin, form post, JSON post or programmatically)
* User receives invitation email with confirmation link
* User clicks link and is redirected to a preconfigured url (default is accounts/signup)
    * This should take the form off 

.. code-block:: python
        re_path(
        r"^accounts/signup/(?P<key>\w+)/?$",
        views.signup,
        name="account_signup",
    ),
    

Allauth Invitation flow:

* As above but..
* User clicks link, their email is confirmed and they are redirected to signup
* The signup URL has the email prefilled and upon signing up the user is logged into the site

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

Make an instance of the model:

.. code-block:: python

    Invitation = get_invitation_model()

Then finally pass the recipient to the model and send.

.. code-block:: python

    # inviter argument is optional
    invite = Invitation.create('email@example.com', inviter=request.user)
    invite.send_invitation(request)

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
