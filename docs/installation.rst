Installation
============

Requirements
------------

Python 3.7 to 3.10 supported.

Django 3.2 to 4.0 supported.

Installation
------------

1. Install with **pip**:

   .. code-block:: sh

       python -m pip install django-invitations

2. Add "invitations" to INSTALLED_APPS

   .. code-block:: python

        INSTALLED_APPS = [
            ...
            "invitations",
            ...
        ]

.. note:: **Allauth support**

   For allauth support ``invitations`` must come after ``allauth`` in the INSTALLED_APPS

3. Add invitations urls to your urlpatterns:

   .. code-block:: python

        urlpatterns = [
            ...
            path("invitations/", include('invitations.urls', namespace='invitations')),
            ...
        ]

4. Run migrations

    .. code-block:: sh

        python manage.py migrate
