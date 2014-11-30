from distutils.core import setup
from setuptools import setup, find_packages

setup(
  name = 'django-invitations',
  packages=find_packages(),
  package_data={'invitations': ['templates/*.*']},
  include_package_data=True,
  zip_safe=False,
  version = '0.12',
  description = 'Django invitation integration for django-allauth',
  author = 'https://github.com/bee-keeper',
  author_email = 'none@none.com',
  url = 'https://github.com/bee-keeper/django-invitations.git',
  download_url = 'https://github.com/bee-keeper/django-invitations/tarball/0.12',
  keywords = ['django', 'invitation', 'django-allauth', 'invite'],
  classifiers = [],
  install_requires=[
    'django-allauth>=0.18.0',
    'django-braces>=1.4.0',
  ],
)
