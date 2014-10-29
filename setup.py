#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

setup(name='icons',
      version='1.0',
      description='generate icons and config file (e.g. Contents.json) ' +
                  'required by iOS or Android app, inspired by ' +
                  'http://makeappicon.com',
      url='http://github.com/exherb/icons',
      author='Herb Brewer',
      author_email='i@4leaf.me',
      license='MIT',
      packages=['icons'],
      install_requires=['pillow>=2.6.1'],
      keywords='icon ios android',
      entry_points={'console_scripts': ['icons = icons:_main_'],
                    'gui_scripts': []})
