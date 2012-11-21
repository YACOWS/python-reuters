#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='reuterslib',
    version='0.1',
    description='TODO',
    url='https://github.com/YACOWS/reuterslib',
    packages=['reuters'],
    package_data={
        'reuters': ['templates/*.xml'],
    },
    install_requires=['Jinja2'],
)
