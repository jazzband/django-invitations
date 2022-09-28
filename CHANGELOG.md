Changelog
=========

2.0.0 (2022-09-28)
----------------

- Joined Jazzband

- Removed support for Django versions below 3.2

- Added support for Django 4.0+. Thanks @saschahofmann [#169](https://github.com/jazzband/django-invitations/pull/169)

- Removed support for Python versions below 3.7

- Added documentation

- Set inviter on invitation in SendJSONInvite view. Thanks @rosexi [#151](https://github.com/jazzband/django-invitations/pull/151)

1.9 (2017-02-11)
----------------

- Added get_signup_redirect to allow custom implementations by subclasses

- Fixed invitation form displaying "None" when first displayed

- Fixed deprecation warnings

- Added get_signup_redirect to allow custom implementations by subclasses

- Fixed flake8 errors

- Import reverse from django.urls if available, otherwise fall back to old import

- Set ForeignKey field to explicitly cascade on deletion

- flake8 styling formatting

- Add email max length setting

1.8 (2016-10-19)
----------------

*TO BE ADDED*


1.7 (2016-02-10)
------------------------

- 1.7. [bee-keeper]

- Merge pull request #34 from percipient/dont-404. [bee-keeper]

  Display a message on expired/erroneous/accepted keys.

- Fix flake8 issues. [Patrick Cloke]

- Fix a formatting mistake in the README. [Patrick Cloke]

- Display a message on expired/erroneous/accepted keys. Related to #25.
  [Patrick Cloke]

- Merge pull request #33 from percipient/readme-settings. [bee-keeper]

  Fix-up the settings in the README

- Update the INVITATIONS_ADAPTER setting. [Patrick Cloke]

- Update the readme with all the settings. [Patrick Cloke]

- Removed uneeded check on send invite. [bee_keeper]

- Test new url spec. [bee_keeper]

- Merge pull request #32 from mjnaderi/patch-1. [bee-keeper]

  Remove RemovedInDjango110Warning warnings in Django 1.9

- Remove RemovedInDjango110Warning warnings in Django 1.9. [Mohammad
  Javad Naderi]

  With Django 1.9, each time I run `python manage.py runserver`, it shows 2 warnings:

  ```
  /someplace/.venv/lib/python2.7/site-packages/invitations/urls.py:15: RemovedInDjango110Warning: django.conf.urls.patterns() is deprecated and will be removed in Django 1.10. Update your urlpatterns to be a list of django.conf.urls.url() instances instead.
    name='accept-invite'),

  /someplace/.venv/lib/python2.7/site-packages/invitations/urls.py:15: RemovedInDjango110Warning: django.conf.urls.patterns() is deprecated and will be removed in Django 1.10. Update your urlpatterns to be a list of django.conf.urls.url() instances instead.
    name='accept-invite'),
  ```

  This pull request fixes it.

1.6 (2016-01-10)
----------------

- V1.6. [bee_keeper]

- Dont override inviter from create step. [bee_keeper]

- Merge pull request #30 from percipient/allauth-with-custom-adapter.
  [bee-keeper]

  Allow using custom allauth backends.

- Make flake8 happy. [Patrick Cloke]

- Don't return None from get_invitations_adapter. [Patrick Cloke]

- Merge pull request #31 from percipient/set-inviter. [bee-keeper]

  Set the inviter in the SendInvite view.

- Set the inviter in the SendInvite view. [Patrick Cloke]

- Update README.md. [bee-keeper]

1.5 (2015-12-07)
----------------

- Update README.md. [bee-keeper]

- Merge pull request #24 from bee-keeper/devel. [bee-keeper]

  Refactor as generic invite app

- Removed the dependency on django-allauth, this package is now a
  generic invite app. [bee_keeper]

1.4 (2015-11-27)
----------------

- 1.4. [bee_keeper]

- Merge pull request #23 from bee-keeper/devel. [bee-keeper]

  Coverage and exposing inviter in admin

- Coverage and exposing inviter in admin. [bee_keeper]

1.3 (2015-11-26)
----------------

- Merge pull request #22 from bee-keeper/devel. [bee-keeper]

  Added inviter to invitation

- Added inviter to invitation. [bee_keeper]

- Merge pull request #21 from bee-keeper/devel. [bee-keeper]

  Support for django1.9

- Testing for django1.9 and python 3.5. [bee_keeper]

- Merge pull request #20 from bee-keeper/devel. [bee-keeper]

  Added json endpoint for invites

- Added json endpoint for invites. [bee_keeper]

- Merge pull request #19 from bee-keeper/devel. [bee-keeper]

  Made accept trailing slash optional

- Made trailing slash optional and added flake8 to CI. [bee_keeper]

  Bumped to version 1.3

- Update models.py. [bee-keeper]

- Roadmap. [bee_keeper]

1.2 (2015-08-29)
----------------

- Test coverage done, ready for 1.2 release. [bee_keeper]

- Dropping support for python 3.2. [bee_keeper]

- Dropping support for python 3.2. [bee_keeper]

- Signal test coverage, tweaking tox. [bee_keeper]

- Coverage. [bee-keeper]

- Tox+travis. [bee-keeper]

- Tox. [bee-keeper]

- Tox+travis. [bee-keeper]

- Testing tox+travis. [bee-keeper]

- Testing tox+travis. [bee-keeper]

- Tox file. [bee_keeper]

- Py3 fix. [bee_keeper]

- Test for signup redirect. [bee_keeper]

- Update README.md. [bee-keeper]

- Py 3.2. [bee_keeper]

- Py 3.2. [bee-keeper]

- Print. [bee-keeper]

- Tests and bug fixes. [bee-keeper]

1.1 (2015-08-05)
----------------

- V 1.1. [bee_keeper]

- Readme. [bee_keeper]

- Modified PR (15) + editorconfig. [bee_keeper]

- Merge branch 'nwaxiomatic-master' [bee_keeper]

- Admin invitations. [Nic]

  sends invitations from admin on save

1.0 (2015-07-26)
----------------

- Release 1.0. [bee_keeper]

- Requirements. [bee_keeper]

- Changing travis supported versions. [bee_keeper]

- Travis. [bee_keeper]

- Travis. [bee_keeper]

- Remove 2.6 from testing. [bee_keeper]

- Requirements and changelog. [bee_keeper]

- Test settings. [bee_keeper]

- Requirements.txt. [bee_keeper]

- Travis. [bee_keeper]

- Removing uneeded imports. [bee_keeper]

- Removed ALLOWED_GROUPS setting. [bee_keeper]

- Merge pull request #12 from tbarbugli/patch-1. [bee-keeper]

  fix invite form

- Fix invite form. [Tommaso Barbugli]

- Update views.py. [bee-keeper]

- Teavis. [bee_keeper]

- Travis. [bee_keeper]

- Travis. [bee_keeper]

- Travis. [bee_keeper]

- Travis. [bee_keeper]

- Travis. [bee_keeper]

- App settings. [bee_keeper]

- Merge pull request #6 from simonv3/master. [bee-keeper]

  # Redo pull request of adding inviter to signal.

- Add reference to inviter in signal. [Simon]

- .travis.yml. [bee_keeper]

- .travis.yml. [bee_keeper]

- Readme. [bee_keeper]

- Fixing py3.2 import issues. [bee_keeper]

- Invitations/app_settings.py. [bee_keeper]

- Py3.2 issue. [bee_keeper]

- Typo with import. [bee_keeper]

- Module object has no attribute issue with 3.2. [bee_keeper]

- Fixes import issue. [bee_keeper]

- Py 3.2 unicode issue. [bee_keeper]

- Travis. [bee_keeper]

- Travis config. [bee_keeper]

- Py3.2 format. [bee_keeper]

- .travis.yml. [bee_keeper]

- .travis.yml. [bee_keeper]

- .travis.yml. [bee_keeper]

- .travs.yml. [bee_keeper]

- .travis.yml. [bee_keeper]

- .travis.yml. [bee_keeper]

- Test settings and more test coverage. [bee_keeper]

- Tests and refactoring. [bee_keeper]

- New style migrations. [bee_keeper]

- 1.7 style migrations. [bee_keeper]

0.12 (2014-11-30)
-----------------

- Release. [bee_keeper]

0.11 (2014-11-30)
-----------------

- Template paths. [bee_keeper]

- Setup.py. [bee_keeper]

- Packaging. [bee_keeper]

- Versions. [bee_keeper]

0.1 (2014-11-30)
----------------

- Packaging. [bee_keeper]

- Include templates in package. [bee_keeper]

- Packaging. [bee_keeper]

- Template path. [bee_keeper]

- Template path. [bee_keeper]

- Name changes. [bee_keeper]
