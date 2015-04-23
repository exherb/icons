#!/usr/bin/env python
# coding=utf-8

import os
import sys
import json
from collections import OrderedDict
import struct
import subprocess
from zipfile import ZipFile
try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO

from PIL import Image


_MAGIC = b"\0\0\1\0"


def _save_to_ico(image, fp,
                 sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64),
                        (128, 128), (255, 255)]):
    fp.write(_MAGIC)  # (2+2)
    width, height = image.size
    filter(lambda x: False if (x[0] > width or x[1] > height or
                               x[0] > 255 or x[1] > 255) else True, sizes)
    sizes = sorted(sizes, key=lambda x: x[0], reverse=True)
    fp.write(struct.pack('H', len(sizes)))  # idCount(2)
    offset = fp.tell() + len(sizes)*16
    for size in sizes:
        width, height = size
        fp.write(struct.pack('B', width))  # bWidth(1)
        fp.write(struct.pack('B', height))  # bHeight(1)
        fp.write(b'\0')  # bColorCount(1)
        fp.write(b'\0')  # bReserved(1)
        fp.write(struct.pack('H', 0))  # wPlanes(2)
        fp.write(struct.pack('H', 32))  # wBitCount(2)

        image_io = BytesIO()
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(image_io, 'png')
        image_io.seek(0)
        image_bytes = image_io.read()
        bytes_len = len(image_bytes)
        fp.write(struct.pack('I', bytes_len))  # dwBytesInRes(4)
        fp.write(struct.pack('I', offset))  # dwImageOffset(4)
        current = fp.tell()
        fp.seek(offset)
        fp.write(image_bytes)
        offset = offset + bytes_len
        fp.seek(current)
    fp.close()


def _resize_image_(image, to_object, to_path, to_size):
    to_size = (int(to_size[0]), int(to_size[1]))
    if to_size == image.size:
        temp = image
    else:
        temp = image.copy()
        temp.thumbnail(to_size, Image.ANTIALIAS)
    _, ext = os.path.splitext(to_path)
    ext = ext.lstrip('.')
    if isinstance(to_object, ZipFile):
        f = BytesIO()
        temp.save(f, ext)
        f.seek(0)
        to_object.writestr(to_path, f.read())
    else:
        with open(to_path, 'wb') as f:
            temp.save(f, ext)
    del temp

_configs_ = {'favicon': '''<head>
    <link rel="icon" type="image/x-icon" href="web/favicon.ico" />
    <link rel="icon" type="image/png" sizes="196x196" href="web/favicon-196.png">
    <link rel="icon" type="image/png" sizes="160x160" href="web/favicon-160.png">
    <link rel="icon" type="image/png" sizes="64x64" href="web/favicon-64.png">
    <link rel="icon" type="image/png" sizes="32x32" href="web/favicon-32.png">
    <link rel="icon" type="image/png" sizes="24x24" href="web/favicon-24.png">
    <link rel="icon" type="image/png" sizes="16x16" href="web/favicon-16.png">
    <link rel="apple-touch-icon" sizes="152x152" href="ios/apple-touch-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="76x76" href="ios/apple-touch-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="180x180" href="ios/apple-touch-icon-180x180.png">
    <link rel="apple-touch-icon" sizes="120x120" href="ios/apple-touch-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="60x60" href="ios/apple-touch-icon-60x60.png">
    <link rel="icon" type="image/png" sizes="96x96" href="googletv/favicon-96.png">
    <meta name="msapplication-TileImage" content="windows8/pinned.png">
    <meta name="msapplication-TileColor" content="#ff0000">
</head>
''',
             '.imageset': [{'idiom': 'universal', 'scale': '1x'},
                           {'idiom': 'universal', 'scale': '2x'},
                           {'idiom': 'universal', 'scale': '3x'}],
             '.iconset': None,
             '.appiconset': [{'idiom': 'iphone', 'scale': '1x',
                              'size': '29x29'},
                             {'idiom': 'iphone', 'scale': '2x',
                              'size': '29x29'},
                             {'idiom': 'iphone', 'scale': '3x',
                              'size': '29x29'},
                             {'idiom': 'iphone', 'scale': '2x',
                              'size': '40x40'},
                             {'idiom': 'iphone', 'scale': '3x',
                              'size': '40x40'},
                             {'idiom': 'iphone', 'scale': '1x',
                              'size': '57x57'},
                             {'idiom': 'iphone', 'scale': '2x',
                              'size': '57x57'},
                             {'idiom': 'iphone', 'scale': '2x',
                              'size': '60x60'},
                             {'idiom': 'iphone', 'scale': '3x',
                              'size': '60x60'},
                             {'idiom': 'ipad', 'scale': '1x',
                              'size': '29x29'},
                             {'idiom': 'ipad', 'scale': '2x',
                              'size': '29x29'},
                             {'idiom': 'ipad', 'scale': '1x',
                              'size': '40x40'},
                             {'idiom': 'ipad', 'scale': '2x',
                              'size': '40x40'},
                             {'idiom': 'ipad', 'scale': '1x',
                              'size': '50x50'},
                             {'idiom': 'ipad', 'scale': '2x',
                              'size': '50x50'},
                             {'idiom': 'ipad', 'scale': '1x',
                              'size': '72x72'},
                             {'idiom': 'ipad', 'scale': '2x',
                              'size': '72x72'},
                             {'idiom': 'ipad', 'scale': '1x',
                              'size': '76x76'},
                             {'idiom': 'ipad', 'scale': '2x',
                              'size': '76x76'},
                             {'idiom': 'car', 'scale': '1x',
                              'size': '120x120'}],
             '.launchimage': [{'extent': 'full-screen',
                               'idiom': 'iphone',
                               'subtype': '736h',
                               'filename': 'Default-800-Portrait-736h.png',
                               'minimum-system-version': '8.0',
                               'orientation': 'portrait',
                               'scale': '3x'
                               },
                              {'extent': 'full-screen',
                               'idiom': 'iphone',
                               'subtype': '736h',
                               'filename': 'Default-800-Landscape-736h.png',
                               'minimum-system-version': '8.0',
                               'orientation': 'landscape',
                               'scale': '3x'
                               },
                              {'extent': 'full-screen',
                               'idiom': 'iphone',
                               'subtype': '667h',
                               'filename': 'Default-800-667h.png',
                               'minimum-system-version': '8.0',
                               'orientation': 'portrait',
                               'scale': '2x'
                               },
                              {'orientation': 'portrait',
                               'idiom': 'iphone',
                               'extent': 'full-screen',
                               'minimum-system-version': '7.0',
                               'filename': 'Default@2x.png',
                               'scale': '2x'
                               },
                              {'extent': 'full-screen',
                               'idiom': 'iphone',
                               'subtype': 'retina4',
                               'filename': 'Default-700-568h@2x.png',
                               'minimum-system-version': '7.0',
                               'orientation': 'portrait',
                               'scale': '2x'
                               },
                              {'orientation': 'portrait',
                               'idiom': 'ipad',
                               'extent': 'full-screen',
                               'minimum-system-version': '7.0',
                               'filename': 'Default-700-Portrait~ipad.png',
                               'scale': '1x'
                               },
                              {'orientation': 'landscape',
                               'idiom': 'ipad',
                               'extent': 'full-screen',
                               'minimum-system-version': '7.0',
                               'filename': 'Default-Landscape~ipad.png',
                               'scale': '1x'
                               },
                              {'orientation': 'portrait',
                               'idiom': 'ipad',
                               'extent': 'full-screen',
                               'minimum-system-version': '7.0',
                               'filename': 'Default-700-Portrait@2x~ipad.png',
                               'scale': '2x'
                               },
                              {'orientation': 'landscape',
                               'idiom': 'ipad',
                               'extent': 'full-screen',
                               'minimum-system-version': '7.0',
                               'filename': 'Default-Landscape@2x~ipad.png',
                               'scale': '2x'
                               }]}


def _generate_icns(imageset_path):
    imageset_path = os.path.realpath(imageset_path)
    output_path = os.path.realpath(os.path.join(os.path.dirname(imageset_path),
                                                'AppIcon.icns'))
    if sys.platform == 'darwin':
        subprocess.call(['iconutil', '--convert', 'icns', '--output',
                         output_path, imageset_path])


def _modify_config_file_(type, all_contents, image_path, lookfor_image_size,
                         lookfor_image_scale,
                         lookfor_system_version=None):
    image_dir = os.path.dirname(image_path)
    image_name = os.path.basename(image_path)
    source_contents = _configs_[type]

    if type == 'favicon':
        type_config_path = os.path.join(os.path.dirname(image_dir),
                                        'configs.txt')
        if type_config_path in all_contents:
            return
        contents = source_contents
    elif type == '.iconset':
        type_config_path = os.path.join(os.path.dirname(image_dir),
                                        'AppIcon.icns')
        if os.path.exists(type_config_path):
            return
        required_icons = set(['icon_128x128.png',
                              'icon_128x128@2x.png',
                              'icon_16x16.png',
                              'icon_16x16@2x.png',
                              'icon_256x256.png',
                              'icon_256x256@2x.png',
                              'icon_32x32.png',
                              'icon_32x32@2x.png',
                              'icon_512x512.png',
                              'icon_512x512@2x.png'])
        if (required_icons - set(os.listdir(image_dir))):
            return
        _generate_icns(image_dir)
        return
    else:
        type_config_path = os.path.join(image_dir, 'Contents.json')
        if type_config_path in all_contents:
            contents = all_contents[type_config_path]
        else:
            contents = {'images': []}
        images = contents.get('images', None)
        if images is None or not isinstance(images, list):
            images = []
            contents['images'] = images
        matched_image = None
        if type == '.imageset':
            def find_image(image_contents, expected_image_scale):
                for image_content in image_contents:
                    image_scale = image_content.get('scale', '1x')
                    image_scale = image_scale.lower().rstrip('x')
                    if not image_scale or\
                       not image_scale.isdigit():
                        continue
                    image_scale = int(image_scale)
                    if image_scale == expected_image_scale:
                        return image_content
                return None
            matched_image = find_image(images, lookfor_image_scale)
            if matched_image is None:
                matched_image = find_image(source_contents,
                                           lookfor_image_scale)
                images.append(matched_image)
        elif type == '.appiconset':
            def find_image(image_contents, expected_image_size,
                           expected_image_scale):
                for image_content in image_contents:
                    image_idiom = image_content.get('idiom', '').lower()
                    if (image_idiom == 'ipad' and
                        '~ipad' not in image_name.lower()) or\
                        (image_idiom != 'ipad' and
                         '~ipad' in image_name.lower()):
                        continue
                    image_scale = image_content.get('scale', '1x')
                    image_scale = image_scale.lower().rstrip('x')
                    image_size = image_content.get('size', None)
                    if not image_scale or not image_size or\
                       not image_scale.isdigit():
                        continue
                    image_scale = int(image_scale)
                    image_size = [int(x) for x in image_size.split('x', 1)
                                  if x.isdigit()]
                    if len(image_size) != 2:
                        continue
                    if image_size[0] == expected_image_size[0] and\
                       image_scale == expected_image_scale:
                        return image_content
                return None
            matched_image = find_image(images, lookfor_image_size,
                                       lookfor_image_scale)
            if matched_image is None:
                matched_image = find_image(source_contents, lookfor_image_size,
                                           lookfor_image_scale)
                images.append(matched_image)
        elif type == '.launchimage':
            def find_image(image_contents, expected_image_size,
                           expected_image_scale,
                           expected_system_version):
                for image_content in image_contents:
                    image_scale = image_content.get('scale', '1x')
                    image_scale = image_scale.lower().rstrip('x')
                    image_idiom = image_content.get('idiom', '').lower()
                    image_orientation = image_content.get('orientation', '').\
                        lower()
                    image_extent = image_content.get('extent', '').lower()
                    if not image_scale or not image_idiom or\
                       not image_scale.isdigit() or\
                       not image_extent or not image_orientation:
                        continue
                    image_scale = int(image_scale)
                    if image_idiom == 'ipad':
                        if image_orientation == 'portrait':
                            if image_extent == 'to-status-bar':
                                image_size = (768, 1004)
                            else:
                                image_size = (768, 1024)
                        elif image_orientation == 'landscape':
                            if image_extent == 'to-status-bar':
                                image_size = (1024, 748)
                            else:
                                image_size = (1024, 768)
                    elif image_idiom == 'iphone':
                        image_subtype = image_content.get('subtype',
                                                          '').lower()
                        if image_orientation == 'portrait':
                            if image_subtype == '736h':
                                image_size = (1242/3.0, 2208/3.0)
                            elif image_subtype == '667h':
                                image_size = (750/2.0, 1334/2.0)
                            elif image_subtype == 'retina4':
                                image_size = (640*0.5, 1136*0.5)
                            else:
                                image_size = (320, 480)
                        elif image_orientation == 'landscape':
                            if image_subtype == '736h':
                                image_size = (2208/3.0, 1242/3.0)
                            else:
                                continue
                    if image_size != expected_image_size or\
                       image_scale != expected_image_scale:
                        continue
                    minimum_system_version = image_content.\
                        get('minimum-system-version', '0')
                    if minimum_system_version.isdigit():
                        minimum_system_version = float(minimum_system_version)
                    else:
                        minimum_system_version = 0
                    if minimum_system_version and\
                       expected_system_version >= minimum_system_version:
                        continue
                    return image_content
                return None
            matched_image = find_image(images, lookfor_image_size,
                                       lookfor_image_scale,
                                       lookfor_system_version)
            if matched_image is None:
                matched_image = find_image(source_contents,
                                           lookfor_image_size,
                                           lookfor_image_scale,
                                           lookfor_system_version)
                images.append(matched_image)
        matched_image['filename'] = image_name
        contents['info'] = {'version': 1, 'author': 'icons'}

    all_contents[type_config_path] = contents


def _save_configs_(to_object, contents):
    for path, value in contents.items():
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value)
        if isinstance(to_object, ZipFile):
            to_object.writestr(path, value)
        else:
            with open(path, 'w') as f:
                f.write(value)


_sizes_ = {'icon': OrderedDict([('ios', {'AppIcon.appiconset/Icon-29~iPad':
                                         (29, 29, 1),
                                         'AppIcon.appiconset/Icon-29@2x~iPad':
                                         (29, 29, 2),
                                         'AppIcon.appiconset/Icon-29@2x':
                                         (29, 29, 2),
                                         'AppIcon.appiconset/Icon-29@3x':
                                         (29, 29, 3),
                                         'AppIcon.appiconset/Icon-40@2x':
                                         (40, 40, 2),
                                         'AppIcon.appiconset/Icon-40~iPad':
                                         (40, 40, 1),
                                         'AppIcon.appiconset/Icon-40@2x~iPad':
                                         (40, 40, 2),
                                         'AppIcon.appiconset/Icon-40@3x':
                                         (40, 40, 3),
                                         'AppIcon.appiconset/Icon-60@2x':
                                         (60, 60, 2),
                                         'AppIcon.appiconset/Icon-60@3x':
                                         (60, 60, 3),
                                         'AppIcon.appiconset/Icon-76~iPad':
                                         (76, 76, 1),
                                         'AppIcon.appiconset/Icon-76@2x~iPad':
                                         (76, 76, 2),
                                         'AppIcon.appiconset/Icon-120':
                                         (120, 120, 1),
                                         'iTunesArtwork': (512, 512, 1),
                                         'iTunesArtwork@2x': (512, 512, 2)}),
                                ('android', {'drawable-ldpi/ic_launcher':
                                             (48, 48, 0.75),
                                             'drawable-mdpi/ic_launcher':
                                             (48, 48, 1),
                                             'drawable-hdpi/ic_launcher':
                                             (48, 48, 1.5),
                                             'drawable-xhdpi/ic_launcher':
                                             (48, 48, 2),
                                             'drawable-xxhdpi/ic_launcher':
                                             (48, 48, 3),
                                             'drawable-xxxhdpi/ic_launcher':
                                             (48, 48, 4),
                                             'playstore': (512, 512, 1)}),
                                ('windowsphone', {'AppBar': (48, 48, 1),
                                                  'ApplicationIcon':
                                                  (90, 90, 1),
                                                  'LockIcon': (38, 38, 1),
                                                  'TileSmall': (110, 110, 1),
                                                  'TileMedium': (202, 202, 1),
                                                  'FlipTileSmall':
                                                  (159, 159, 1),
                                                  'FlipTileMedium':
                                                  (336, 336, 1),
                                                  'FlipTileLarge':
                                                  (691, 336, 1),
                                                  'TileSmallBest':
                                                  (70, 110, 1),
                                                  'TileMediumBest':
                                                  (130, 202, 1),
                                                  'Lens-Screen-WVGA':
                                                  (173, 173, 1),
                                                  'Lens-Screen-720p':
                                                  (259, 259, 1),
                                                  'Lens-Screen-WXGA':
                                                  (277, 277, 1),
                                                  'FileHandlerSmall':
                                                  (33, 33, 1),
                                                  'FileHandlerMedium':
                                                  (69, 69, 1),
                                                  'FileHandlerLarge':
                                                  (179, 179, 1),
                                                  'Store': (300, 300, 1)}),
                                ('blackberry', {'icon-90': (90, 90, 1),
                                                'icon-96': (96, 96, 1),
                                                'icon-110': (110, 110, 1),
                                                'icon-114': (114, 114, 1)}),
                                ('chromestore', {'icon16': (16, 16, 1),
                                                 'icon48': (48, 48, 1),
                                                 'icon128': (128, 128, 1)}),
                                ('osx', {'AppIcon.iconset/icon_16x16':
                                         (16, 16, 1),
                                         'AppIcon.iconset/icon_16x16@2x':
                                         (16, 16, 2),
                                         'AppIcon.iconset/icon_32x32':
                                         (32, 32, 1),
                                         'AppIcon.iconset/icon_32x32@2x':
                                         (32, 32, 2),
                                         'AppIcon.iconset/icon_128x128':
                                         (128, 128, 1),
                                         'AppIcon.iconset/icon_128x128@2x':
                                         (128, 128, 2),
                                         'AppIcon.iconset/icon_256x256':
                                         (256, 256, 1),
                                         'AppIcon.iconset/icon_256x256@2x':
                                         (256, 256, 2),
                                         'AppIcon.iconset/icon_512x512':
                                         (512, 512, 1),
                                         'AppIcon.iconset/icon_512x512@2x':
                                         (512, 512, 2)}),
                               ('windows', {'icon.ico': (256, 256, 1)})]),
           'launch': OrderedDict([('ios', {'LaunchImage.launchimage/' +
                                           'Default-800-Portrait-736h':
                                           (414, 736, 3, 8.0),
                                           'LaunchImage.launchimage/' +
                                           'Default-800-667h':
                                           (375, 667, 2, 8.0),
                                           'LaunchImage.launchimage/' +
                                           'Default-800-Landscape-736h':
                                           (736, 414, 3, 8.0),
                                           'LaunchImage.launchimage/' +
                                           'Default@2x':
                                           (320, 480, 2),
                                           'LaunchImage.launchimage/' +
                                           'Default-700-568h@2x':
                                           (320, 568, 2, 7.0),
                                           'LaunchImage.launchimage/' +
                                           'Default-700-Portrait~ipad':
                                           (768, 1024, 1, 7.0),
                                           'LaunchImage.launchimage/' +
                                           'Default-700-Portrait@2x~ipad':
                                           (768, 1024, 2, 7.0),
                                           'LaunchImage.launchimage/' +
                                           'Default-Landscape~ipad':
                                           (1024, 768, 1),
                                           'LaunchImage.launchimage/' +
                                           'Default-Landscape@2x~ipad':
                                           (1024, 768, 2)}),
                                  ('android', {'drawable-ldpi/splash':
                                               (320, 480, 0.75),
                                               'drawable-mdpi/splash':
                                               (320, 480, 1),
                                               'drawable-hdpi/splash':
                                               (320, 480, 1.5),
                                               'drawable-xhdpi/splash':
                                               (320, 480, 2),
                                               'drawable-xxhdpi/splash':
                                               (320, 480, 3),
                                               'drawable-xxxhdpi/splash':
                                               (320, 480, 4),
                                               'drawable-ldpi/' +
                                               'splash-landscape':
                                               (480, 320, 0.75),
                                               'drawable-mdpi/' +
                                               'splash-landscape':
                                               (480, 320, 1),
                                               'drawable-hdpi/' +
                                               'splash-landscape':
                                               (480, 320, 1.5),
                                               'drawable-xhdpi/' +
                                               'splash-landscape':
                                               (480, 320, 2),
                                               'drawable-xxhdpi/' +
                                               'splash-landscape':
                                               (480, 320, 3),
                                               'drawable-xxxhdpi/splash':
                                               (480, 320, 4)})]),
           'toolbar': OrderedDict([('ios', {'{filename}.imageset/{filename}':
                                            (22, None, 1),
                                            '{filename}.imageset/' +
                                            '{filename}@2x':
                                            (22, None, 2),
                                            '{filename}.imageset/' +
                                            '{filename}@3x':
                                            (22, None, 3)}),
                                   ('android', {'drawable-ldpi/{filename}':
                                                (24, 24, 0.75),
                                                'drawable-mdpi/{filename}':
                                                (24, 24, 1),
                                                'drawable-hdpi/{filename}':
                                                (24, 24, 1.5),
                                                'drawable-xhdpi/{filename}':
                                                (24, 24, 2),
                                                'drawable-xxhdpi/{filename}':
                                                (24, 24, 3),
                                                'drawable-xxxhdpi/{filename}':
                                                (24, 24, 4),
                                                'drawable-ldpi/' +
                                                '{filename}-small':
                                                (16, 16, 0.75),
                                                'drawable-mdpi/' +
                                                '{filename}-small':
                                                (16, 16, 1),
                                                'drawable-hdpi/' +
                                                '{filename}-small':
                                                (16, 16, 1.5),
                                                'drawable-xhdpi/' +
                                                '{filename}-small':
                                                (16, 16, 2),
                                                'drawable-xxhdpi/' +
                                                '{filename}-small':
                                                (16, 16, 3),
                                                'drawable-xxxhdpi/' +
                                                '{filename}-small':
                                                (16, 16, 4)})]),
           'tab': OrderedDict([('ios', {'{filename}.imageset/{filename}':
                                        (25, None, 1),
                                        '{filename}.imageset/{filename}@2x':
                                        (25, None, 2),
                                        '{filename}.imageset/{filename}@3x':
                                        (25, None, 3)}),
                               ('android', {'drawable-ldpi/{filename}':
                                            (24, 24, 0.75),
                                            'drawable-mdpi/{filename}':
                                            (24, 24, 1),
                                            'drawable-hdpi/{filename}':
                                            (24, 24, 1.5),
                                            'drawable-xhdpi/{filename}':
                                            (24, 24, 2),
                                            'drawable-xxhdpi/{filename}':
                                            (24, 24, 3),
                                            'drawable-xxxhdpi/{filename}':
                                            (24, 24, 4)})]),
           'notification': OrderedDict([('android', {'drawable-ldpi/' +
                                                     'notification':
                                                     (22, 22, 0.75),
                                                     'drawable-mdpi/' +
                                                     'notification':
                                                     (22, 22, 1),
                                                     'drawable-hdpi/' +
                                                     'notification':
                                                     (22, 22, 1.5),
                                                     'drawable-xhdpi/' +
                                                     'notification':
                                                     (22, 22, 2),
                                                     'drawable-xxhdpi/' +
                                                     'notification':
                                                     (22, 22, 3),
                                                     'drawable-xxxhdpi/' +
                                                     'notification':
                                                     (22, 22, 4)})]),
           'favicon': OrderedDict([('ios', {'apple-touch-icon-60x60':
                                            (60, 60, 1),
                                            'apple-touch-icon-120x120':
                                            (60, 60, 2),
                                            'apple-touch-icon-180x180':
                                            (60, 60, 3),
                                            'apple-touch-icon-76x76':
                                            (76, 76, 1),
                                            'apple-touch-icon-152x152':
                                            (76, 76, 2)}),
                                   ('web', {'favicon-16': (16, 16, 1),
                                            'favicon-24': (24, 24, 1),
                                            'favicon-32': (32, 32, 1),
                                            'favicon-64': (64, 64, 1),
                                            'favicon-160': (160, 160, 1),
                                            'favicon-196': (196, 196, 1),
                                            'favicon.ico': (256, 256, 1)}),
                                   ('googletv', {'favicon-96': (96, 96, 1)}),
                                   ('windows8', {'pinned': (144, 144, 1)})]),
           'image': OrderedDict([('ios', {'{filename}.imageset/{filename}':
                                          (None, None, 1),
                                          '{filename}.imageset/{filename}@2x':
                                          (None, None, 2),
                                          '{filename}.imageset/{filename}@3x':
                                          (None, None, 3)}),
                                 ('android', {'drawable-ldpi/{filename}':
                                              (None, None, 0.75),
                                              'drawable-mdpi/{filename}':
                                              (None, None, 1),
                                              'drawable-hdpi/{filename}':
                                              (None, None, 1.5),
                                              'drawable-xhdpi/{filename}':
                                              (None, None, 2),
                                              'drawable-xxhdpi/{filename}':
                                              (None, None, 3),
                                              'drawable-xxxhdpi/{filename}':
                                              (None, None, 4)})])}

_device_names_ = {'ios': 'iOS', 'osx': 'OS X',
                  'googletv': 'Google TV', 'windows8': 'Widnows 8',
                  'windowsphone': 'Windows Phone', 'blackberry': 'Black Beery',
                  'chromestore': 'Chrome Web Store'}


def device_name(device):
    device_name = _device_names_.get(device, None)
    if device_name:
        return device_name
    return device[0].upper() + device[1:]


def supported_devices(icon_type):
    return _sizes_.get(icon_type, {}).keys()


def supported_types():
    return _sizes_.keys()


def make_images(image, image_name, to_object, type,
                allowed_devices=None, baseline_scale=2):
    original_image_width, original_image_height = image.size
    if type not in _sizes_:
        raise RuntimeError('Error: no such icon type')
    devices = _sizes_[type]
    if not allowed_devices:
        allowed_devices = devices.keys()
    all_contents = {}
    for device, sizes in devices.items():
        if device not in allowed_devices:
            continue
        if isinstance(to_object, ZipFile):
            device_path = device
        else:
            device_path = os.path.join(to_object, device)
            if not os.path.exists(device_path):
                os.makedirs(device_path)
            elif not os.path.isdir(device_path):
                print('Warning: can\'t make dir {} for {}'.
                      format(device_path, device))
                continue
        if not sizes:
            continue
        widths = [x[0]*x[2] for x in sizes.values()
                  if isinstance(x[0], int)]
        min_image_width = None
        if min_image_width:
            min_image_width = max(widths)
        if min_image_width:
            heights = [x[1]*x[2] for x in sizes.values()
                       if isinstance(x[1], int)]
            min_image_height = None
            if heights:
                min_image_height = max(heights)
            if min_image_height is None:
                min_image_height = min_image_width*1.0 /\
                    original_image_width*original_image_height
            scale = max(min_image_width*1.0/original_image_width,
                        min_image_height*1.0/original_image_height)
            crop_image_width = min_image_width/scale
            crop_image_height = min_image_height/scale
            if original_image_width > crop_image_width and\
               original_image_height > crop_image_height:
                x_offset = (original_image_width - crop_image_width)*0.5
                y_offset = (original_image_height - crop_image_height)*0.5
                image = image.crop((x_offset, y_offset,
                                    x_offset + crop_image_width,
                                    y_offset + crop_image_height))
        for name, size_info in sizes.items():
            width, height, scale = size_info[:3]
            if len(size_info) > 3:
                system_version = size_info[3]
            else:
                system_version = None
            if width is None:
                width = original_image_width*1.0/baseline_scale
            if height is None:
                height = width*1.0/original_image_width*original_image_height
            name = name.replace('{filename}', image_name)
            image_path = os.path.join(device_path, name)
            _, ext = os.path.splitext(name)
            if ext.lower() == '.ico':
                with open(image_path, 'wb') as f:
                    _save_to_ico(image, f)
            else:
                if not ext:
                    image_path = image_path + '.png'
                if scale > baseline_scale:
                    print(('Warning: {} scale {} is bigger than ' +
                           'base line scale {}').
                          format(image_path, scale, baseline_scale))
                    continue
                if not isinstance(to_object, ZipFile):
                    image_dir_path = os.path.dirname(image_path)
                    if not os.path.exists(image_dir_path):
                        os.makedirs(image_dir_path)
                    elif not os.path.isdir(image_dir_path):
                        print('Warning: can\'t make dir {} for {}({}x{})'.
                              format(image_dir_path, image_path, width*scale,
                                     height*scale))
                        continue
                    if os.path.exists(image_path):
                        print('Warning: {} is already exists'.
                              format(image_path))
                        continue
                if width > original_image_width or\
                   height > original_image_height:
                    print('Warning: {}x{} is too small for {}({}x{})'.
                          format(original_image_width, original_image_height,
                                 image_path, width*scale, height*scale))
                    continue
                _resize_image_(image, to_object, image_path,
                               (width*scale, height*scale))

            for type in _configs_.keys():
                if type in name:
                    _modify_config_file_(type, all_contents, image_path,
                                         (width, height),
                                         scale,
                                         system_version)
                    break
    _save_configs_(to_object, all_contents)


def _main_():
    import argparse
    from contextlib import closing
    from zipfile import ZIP_DEFLATED

    parser = argparse.ArgumentParser(description='generate icons for devices')
    parser.add_argument('icon_path',
                        help='source icon path')
    parser.add_argument('-o',
                        default=None,
                        dest='target_path',
                        help='target path')
    parser.add_argument('--baseline', '-b', default=3,
                        type=int,
                        help='icon scale baseline')
    parser.add_argument('--type', '-t', default='icon',
                        choices=supported_types(),
                        dest='icon_type',
                        help='icon type')
    parser.add_argument('--devices', '-d',
                        default='ios',
                        choices=['ios', 'android'],
                        help='including devices')
    parser.add_argument('--zip', '-z', action='store_const', const=True)
    args = parser.parse_args()
    if not args.target_path:
        args.target_path = os.path.dirname(args.icon_path)
    if args.zip:
        ext = os.path.splitext(args.target_path)[-1].lower()
        if ext != '.zip':
            args.target_path = args.target_path + '.zip'
        if os.path.exists(args.target_path):
            raise RuntimeError('Error: {} is already exists'.
                               format(args.target_path))
    image = Image.open(args.icon_path)
    image_name, _ = os.path.splitext(os.path.basename(args.icon_path))
    if args.zip:
        with closing(ZipFile(args.target_path,
                             "w", ZIP_DEFLATED)) as zip_file:
            make_images(image, image_name, zip_file, args.icon_type,
                        args.devices, args.baseline)
    else:
        make_images(image, image_name, args.target_path, args.icon_type,
                    args.devices, args.baseline)

if __name__ == '__main__':
    _main_()
