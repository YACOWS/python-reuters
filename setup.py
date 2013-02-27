#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='python-reuters',
    version='0.2',
    description='Python library to consume Reuters Soap Web services',
    author='Rael Max',
    author_email='contato@raelmax.com',
    url='https://github.com/YACOWS/python-reuters',
    packages=['reuters'],
    package_data={
        'reuters': ['templates/*.xml'],
    },
    test_suite='tests.suite',
    install_requires=['Jinja2'],
    tests_require=['Mock'],
)

