from setuptools import setup, find_packages

setup(
    name='django-invitations',
    packages=find_packages(),
    package_data={'invitations': ['templates/*.*']},
    include_package_data=True,
    zip_safe=False,
    version='1.8',
    description='Generic invitations app with support for django-allauth',
    author='https://github.com/bee-keeper',
    author_email='none@none.com',
    url='https://github.com/bee-keeper/django-invitations.git',
    download_url='https://github.com/'
                 'bee-keeper/django-invitations/tarball/1.8',
    keywords=['django', 'invitation', 'django-allauth', 'invite'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
    ],
    install_requires=[
        'django-braces>=1.8.0'
    ]
)
