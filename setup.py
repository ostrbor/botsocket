#!/usr/bin/env python
from distutils.core import setup

setup(name='botsocket',
      version='1.0',
      description='socket server for bot communication',
      author='Boris Ostretsov',
      license='MIT',
      author_email='ostrbor@gmail.com',
      keywords='bot botnet socket server simple',
      url='https://github.com/ostrbor/botsocket',
      packages=['botsocket'],
      install_requires=['cffi',
                        'cryptography',
                        'idna',
                        'py',
                        'pyasn1',
                        'pycparser',
                        'pyOpenSSL',
                        'pytest',
                        'PyYAML',
                        'six',]
      )
