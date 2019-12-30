#!/usr/bin/env python3
from setuptools import setup

setup(
    name='stripctl',
    version='1.0',

    description='LED Strip Control',

    author='Christian Volkmann',
    author_email='ch.volkmann@gmail.com',

    packages=['stripctl'],
    install_requires=[
        'spidev',
        'colour'
    ]
)
