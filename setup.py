from distutils.core import setup
from setuptools import setup

setup(
  name = 'django-invitations',
  packages=['invitations'],
  include_package_data=True,
  package_data={'invitations': ['templates/invitations/*.*']},
  zip_safe=False,
  version = '0.1',
  description = 'Django invitation integration for django-allauth',
  author = 'https://github.com/bee-keeper',
  author_email = 'none@none.com',
  url = 'https://github.com/bee-keeper/django-invitations.git',
  download_url = 'https://github.com/bee-keeper/django-invitations/tarball/0.1',
  keywords = ['django', 'invitation', 'django-allauth', 'invite'],
  classifiers = [],
  install_requires=[
    'django-allauth>=0.18.0',
    'django-braces>=1.4.0',
  ],
)
