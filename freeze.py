#!/usr/bin/env python
# coding=utf-8

import os
import sys
from setuptools import setup

mainscript = 'icons/__init__.py'

if sys.platform == 'darwin':
    os.system(('cxfreeze {} --target-dir  build --target-name icons ' +
              '--include-modules PIL').format(mainscript))
elif sys.platform == 'win32':
    extra_options = dict(
        setup_requires=['py2exe'],
        console=[mainscript],
    )
    setup(
        name="icons",
        **extra_options
    )
