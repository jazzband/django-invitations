Contributing
============

JazzBand project
----------------
As we are members of a [JazzBand project](https://jazzband.co/projects), `django-invitations` contributors should adhere to the [Contributor Code of Conduct](https://jazzband.co/about/conduct).


Testing
-------

It's important that any new code is tested before submission. To quickly test code in your active development environment, you should first install all of the requirements by running:

.. code-block:: bash

    source .venv/bin/activate
    pip install -e '.[testing]' -U

Then, run the following command to execute tests:

.. code-block:: bash

    pytest --cov-report term --cov=invitations  --ignore=tests/allauth/  --ds=tests.settings tests

To test the integration with django-allauth, first make sure you have it installed. Then run:

.. code-block:: bash

    pytest --cov-report term --cov=invitations  --ignore=tests/basic/  --ds=tests.settings_allauth tests

Testing in a single environment is a quick and easy way to identify obvious issues with your code. However, it's important to test changes in other environments too, before they are submitted. In order to help with this, django-invitations is configured to use tox for multi-environment tests. They take longer to complete, but can be triggered with a simple command:

.. code-block:: bash

    tox
