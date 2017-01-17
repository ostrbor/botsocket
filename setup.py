#!/usr/bin/env python
from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


def requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()


setup(
    name='botsocket',
    version='0.2.0',
    description='socket server for bot communication',
    long_description=readme(),
    author='Boris Ostretsov',
    license='MIT',
    author_email='ostrbor@gmail.com',
    keywords='bot botnet socket server',
    url='https://github.com/ostrbor/botsocket',
    packages=['botsocket'],
    install_requires=requirements())
