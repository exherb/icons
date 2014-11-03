#!/usr/bin/env python
# coding=utf-8

import sys
import os
from setuptools import setup

mainscript = 'icons/gui.py'

name = "Icons"
if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        options={'py2app': {'argv_emulation': False,
                            'iconfile': 'images/icon.icns',
                            'plist': {
                                'CFBundleName': name,
                                'CFBundleShortVersionString': '1.0.0',
                                'CFBundleVersion': '1.0.0',
                                'NSHumanReadableCopyright': '@Herb Brewer 2014'
                                }
                            }})
elif sys.platform == 'win32':
    import py2exe
    extra_options = dict(
        setup_requires=['py2exe'],
        windows=[{'script': mainscript,
                  'icon_resources': [(0, 'images/icon.ico')]}]
    )
setup(
    name=name,
    **extra_options
)

if sys.platform == 'win32':
    os.rename('dist/gui.exe', 'dist/{}.exe'.format(name))
