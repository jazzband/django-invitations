Installation
============

Requirements
------------

Python 3.8 to 3.12 supported.

Django 3.2 to 5.0 supported.

Installation
------------

1. Install with `pip <https://pip.pypa.io/>`_:

   .. code-block:: sh

       python -m pip install django-invitations

2. Add ``"invitations"`` to ``INSTALLED_APPS``:

   .. code-block:: python

        INSTALLED_APPS = [
            ...
            "invitations",
            ...
        ]

.. note:: **django-allauth support**

   For django-allauth support, ``"invitations"`` must come after ``"allauth"`` in the ``INSTALLED_APPS`` list.

3. If using `django-allauth <https://docs.allauth.org/>`_, then add this configuration to your ``settings.py`` file:

    .. code-block:: python

        # django-allauth configuration:
        ACCOUNT_ADAPTER = "invitations.models.InvitationsAdapter"

        # django-invitations configuration:
        INVITATIONS_ADAPTER = ACCOUNT_ADAPTER

4. Add invitations URLs to your ``urlpatterns``:

   .. code-block:: python

        from django.urls import include, path

        urlpatterns = [
            ...
            path("invitations/", include('invitations.urls', namespace='invitations')),
            ...
        ]

5. Run migrations:

    .. code-block:: sh

        python manage.py migrate
