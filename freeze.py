#!/usr/bin/env python
# coding=utf-8

import sys
import os
from glob import glob
from setuptools import setup

mainscript = 'icons/gui.py'

name = "Icons"
if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        options={'py2app': {'argv_emulation': False,
                            'iconfile': 'icos/icon.icns',
                            'plist': {
                                'CFBundleName': name,
                                'CFBundleShortVersionString': '1.1',
                                'CFBundleVersion': '1.1',
                                'NSHumanReadableCopyright': '@Herb Brewer 2014'
                                }
                            }})
elif sys.platform == 'win32':
    import py2exe
    extra_options = dict(
        setup_requires=['py2exe'],
        windows=[{'script': mainscript,
                  'icon_resources': [(0, 'icos/icon.ico')]}],
        bundle_files=2
    )
setup(
    name=name,
    data_files=[('tkdnd/{}'.format(sys.platform),
                glob('icons/tkdnd/{}/*'.format(sys.platform)))],
    **extra_options
)

if sys.platform == 'win32':
    target = 'dist/{}.exe'.format(name)
    if os.path.exists(target):
        os.remove(target)
    os.rename('dist/gui.exe', target)
