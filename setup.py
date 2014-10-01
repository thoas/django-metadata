# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

version = __import__('metadata').__version__

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, 'README.rst')) as f:
    README = f.read()

setup(
    name='django-metadata',
    version=version,
    description='Attach metadata to any Django models using redis',
    long_description=README,
    author='Florent Messa',
    author_email='florent.messa@gmail.com',
    url='http://github.com/thoas/django-metadata',
    zip_safe=False,
    include_package_data=True,
    keywords='django libraries settings redis metadata'.split(),
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
    ],
    extras_require={
        'redis': ['redis'],
    },
    install_requires=['six'],
    tests_require=['coverage', 'exam', ],
    packages=find_packages(exclude=['tests']),
)
