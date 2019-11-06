from setuptools import setup, find_packages

setup(
    name='django-invitations',
    packages=find_packages(),
    package_data={'invitations': ['templates/*.*']},
    include_package_data=True,
    zip_safe=False,
    version='1.9.2',
    description='Generic invitations app with support for django-allauth',
    author='https://github.com/bee-keeper',
    author_email='none@none.com',
    url='https://github.com/bee-keeper/django-invitations.git',
    download_url='https://github.com/'
                 'bee-keeper/django-invitations/tarball/1.9.2',
    keywords=['django', 'invitation', 'django-allauth', 'invite'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
    ],
)
