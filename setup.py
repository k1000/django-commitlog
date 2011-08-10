# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license. 
# See the NOTICE for more information.


import os
from setuptools import setup, find_packages

setup(
    name = 'django-commitlog',
    version = "0.1",

    description = 'Preview your git commits.',
    long_description = file(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author = 'Kamil Selwa',
    author_email = 'selwak@gmail.com',
    license = 'MIT',
    url = 'http://selwa.info',

    classifiers = [
        'Development Status :: 1 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: POSIX',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe = False,
    packages = find_packages(exclude=['examples', 'tests']),
    #include_package_data = True,
    #package_data={'backfire': media_dirs},
    install_requires=['setuptools'],
)
