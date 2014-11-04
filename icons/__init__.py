#!/usr/bin/env python
# coding=utf-8

import os
import json
from zipfile import ZipFile
try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO

from PIL import Image


_image_format_ = ('png', '.png')


def _resize_image_(image, to_object, to_path, to_size):
    to_size = (int(to_size[0]), int(to_size[1]))
    if to_size == image.size:
        temp = image
    else:
        temp = image.copy()
        temp.thumbnail(to_size, Image.ANTIALIAS)
    if isinstance(to_object, ZipFile):
        f = BytesIO()
        temp.save(f, _image_format_[0])
        f.seek(0)
        to_object.writestr(to_path, f.read())
    else:
        with open(to_path, 'wb') as f:
            temp.save(f, _image_format_[0])
    del temp

_configs_ = {'favicon': '''<head>
    <link rel="icon" type="image/png" sizes="196x196" href="/favicon-196.png">
    <link rel="icon" type="image/png" sizes="160x160" href="/favicon-160.png">
    <link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
    <link rel="icon" type="image/png" sizes="64x64" href="/favicon-64.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/favicon-76@2x.png">
    <link rel="apple-touch-icon" sizes="76x76" href="/favicon-76.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/favicon-60@3x.png">
    <link rel="apple-touch-icon" sizes="120x120" href="/favicon-60@2x.png">
    <link rel="apple-touch-icon" sizes="60x60" href="/favicon-60.png">
    <link rel="apple-touch-icon" href="/favicon-60.png">
</head>
''',
             '.imageset': [{'idiom': 'universal', 'scale': '1x'},
                           {'idiom': 'universal', 'scale': '2x'},
                           {'idiom': 'universal', 'scale': '3x'}],
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
             '.launchimage': [{'scale': '3x',
                               'orientation': 'portrait',
                               'subtype': '736h',
                               'minimum-system-version': '8.0',
                               'idiom': 'iphone',
                               'extent': 'full-screen'},
                              {'scale': '3x',
                               'orientation': 'landscape',
                               'subtype': '736h',
                               'minimum-system-version': '8.0',
                               'idiom': 'iphone',
                               'extent': 'full-screen'},
                              {'scale': '2x',
                               'orientation': 'portrait',
                               'subtype': '667h',
                               'minimum-system-version': '8.0',
                               'idiom': 'iphone',
                               'extent': 'full-screen'},
                              {'scale': '2x',
                               'orientation': 'portrait',
                               'minimum-system-version': '7.0',
                               'idiom': 'iphone',
                               'extent': 'full-screen'},
                              {'scale': '2x',
                               'orientation': 'portrait',
                               'subtype': 'retina4',
                               'minimum-system-version': '7.0',
                               'idiom': 'iphone',
                               'extent': 'full-screen'},
                              {'idiom': 'ipad',
                               'minimum-system-version': '7.0',
                               'orientation': 'portrait',
                               'extent': 'full-screen',
                               'scale': '1x'},
                              {'idiom': 'ipad',
                               'minimum-system-version': '7.0',
                               'orientation': 'landscape',
                               'extent': 'full-screen',
                               'scale': '1x'},
                              {'idiom': 'ipad',
                               'minimum-system-version': '7.0',
                               'orientation': 'portrait',
                               'extent': 'full-screen',
                               'scale': '2x'},
                              {'idiom': 'ipad',
                               'minimum-system-version': '7.0',
                               'orientation': 'landscape',
                               'extent': 'full-screen',
                               'scale': '2x'},
                              {'idiom': 'iphone',
                               'scale': '1x',
                               'orientation': 'portrait',
                               'extent': 'full-screen'},
                              {'idiom': 'iphone',
                               'scale': '2x',
                               'orientation': 'portrait',
                               'extent': 'full-screen'},
                              {'idiom': 'iphone',
                               'scale': '2x',
                               'orientation': 'portrait',
                               'extent': 'full-screen',
                               'subtype': 'retina4'},
                              {'idiom': 'ipad',
                               'scale': '1x',
                               'orientation': 'portrait',
                               'extent': 'to-status-bar'},
                              {'idiom': 'ipad',
                               'scale': '1x',
                               'orientation': 'portrait',
                               'extent': 'full-screen'},
                              {'idiom': 'ipad',
                               'scale': '1x',
                               'orientation': 'landscape',
                               'extent': 'to-status-bar'},
                              {'idiom': 'ipad',
                               'scale': '1x',
                               'orientation': 'landscape',
                               'extent': 'full-screen'},
                              {'idiom': 'ipad',
                               'scale': '2x',
                               'orientation': 'portrait',
                               'extent': 'to-status-bar'},
                              {'idiom': 'ipad',
                               'scale': '2x',
                               'orientation': 'portrait',
                               'extent': 'full-screen'},
                              {'idiom': 'ipad',
                               'scale': '2x',
                               'orientation': 'landscape',
                               'extent': 'to-status-bar'},
                              {'idiom': 'ipad',
                               'scale': '2x',
                               'orientation': 'landscape',
                               'extent': 'full-screen'}]}


def _modify_config_file_(type, all_contents, image_path, lookfor_image_size,
                         lookfor_image_scale,
                         lookfor_system_version=None):
    image_dir = os.path.dirname(image_path)
    image_name = os.path.basename(image_path)
    source_contents = _configs_[type]

    if type == 'favicon':
        contents_json_path = os.path.join(image_dir, 'configs.txt')
        if contents_json_path in all_contents:
            return
        contents = source_contents
    else:
        contents_json_path = os.path.join(image_dir, 'Contents.json')
        if contents_json_path in all_contents:
            contents = all_contents[contents_json_path]
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

    all_contents[contents_json_path] = contents


def _save_configs_(to_object, contents):
    for path, value in contents.items():
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value)
        if isinstance(to_object, ZipFile):
            to_object.writestr(path, value)
        else:
            with open(path, 'w') as f:
                f.write(value)


_sizes_ = {'icon': {'ios': {'AppIcon.appiconset/Icon-29': (29, 29, 1),
                            'AppIcon.appiconset/Icon-29@2x':
                            (29, 29, 2),
                            'AppIcon.appiconset/Icon-29@3x':
                            (29, 29, 3),
                            'AppIcon.appiconset/Icon-40': (40, 40, 1),
                            'AppIcon.appiconset/Icon-40@2x':
                            (40, 40, 2),
                            'AppIcon.appiconset/Icon-40@3x':
                            (40, 40, 3),
                            'AppIcon.appiconset/Icon-60@2x':
                            (60, 60, 2),
                            'AppIcon.appiconset/Icon-60@3x':
                            (60, 60, 3),
                            'AppIcon.appiconset/Icon-76': (76, 76, 1),
                            'AppIcon.appiconset/Icon-76@2x':
                            (76, 76, 2),
                            'iTunesArtwork': (512, 512, 1),
                            'iTunesArtwork@2x': (512, 512, 2)},
                    'android': {'drawable-ldpi/ic_launcher': (48, 48, 0.75),
                                'drawable-mdpi/ic_launcher': (48, 48, 1),
                                'drawable-hdpi/ic_launcher': (48, 48, 1.5),
                                'drawable-xhdpi/ic_launcher':
                                (48, 48, 2),
                                'drawable-xxhdpi/ic_launcher':
                                (48, 48, 3),
                                'drawable-xxxhdpi/ic_launcher':
                                (48, 48, 4),
                                'playstore': (512, 512, 1)}},
           'launch': {'ios': {'LaunchImage.launchimage/' +
                              'Default-To-Status-Bar-Portrait~ipad':
                              (768, 1004, 1),
                              'LaunchImage.launchimage/' +
                              'Default-To-Status-Bar-Portrait@2x~ipad':
                              (768, 1004, 2),
                              'LaunchImage.launchimage/' +
                              'Default-Portrait~ipad':
                              (768, 1024, 1),
                              'LaunchImage.launchimage/' +
                              'Default-Portrait@2x~ipad':
                              (768, 1024, 2),
                              'LaunchImage.launchimage/' +
                              'Default-To-Status-Bar-Landscape~ipad':
                              (1024, 748, 1),
                              'LaunchImage.launchimage/' +
                              'Default-To-Status-Bar-Landscape@2x~ipad':
                              (1024, 748, 2),
                              'LaunchImage.launchimage/' +
                              'Default-Landscape~ipad':
                              (1024, 768, 1),
                              'LaunchImage.launchimage/' +
                              'Default-Landscape@2x~ipad':
                              (1024, 768, 2),
                              'LaunchImage.launchimage/' +
                              'Default-700-Portrait~ipad':
                              (768, 1024, 1, 7.0),
                              'LaunchImage.launchimage/' +
                              'Default-700-Portrait@2x~ipad':
                              (768, 1024, 2, 7.0),
                              'LaunchImage.launchimage/' +
                              'Default-700-Landscape~ipad':
                              (1024, 768, 1, 7.0),
                              'LaunchImage.launchimage/' +
                              'Default-700-Landscape@2x~ipad':
                              (1024, 768, 2, 7.0),
                              'LaunchImage.launchimage/' +
                              'Default':
                              (320, 480, 1),
                              'LaunchImage.launchimage/' +
                              'Default@2x':
                              (320, 480, 2),
                              'LaunchImage.launchimage/' +
                              'Default-700@2x':
                              (320, 480, 2, 7.0),
                              'LaunchImage.launchimage/' +
                              'Default-568h@2x':
                              (320, 568, 2),
                              'LaunchImage.launchimage/' +
                              'Default-700-568h@2x':
                              (320, 568, 2, 7.0),
                              'LaunchImage.launchimage/' +
                              'Default-800-667h':
                              (375, 667, 2, 8.0),
                              'LaunchImage.launchimage/' +
                              'Default-800-Portrait-736h':
                              (414, 736, 3, 8.0),
                              'LaunchImage.launchimage/' +
                              'Default-800-Landscape-736h':
                              (736, 414, 3, 8.0)},
                      'android': {'drawable-ldpi/splash':
                                  (320, 480, 0.75),
                                  'drawable-mdpi/splash': (320, 480, 1),
                                  'drawable-hdpi/splash': (320, 480, 1.5),
                                  'drawable-xhdpi/splash': (320, 480, 2),
                                  'drawable-xxhdpi/splash':
                                  (320, 480, 3),
                                  'drawable-xxxhdpi/splash':
                                  (320, 480, 4),
                                  'drawable-ldpi/splash-landscape':
                                  (480, 320, 0.75),
                                  'drawable-mdpi/splash-landscape':
                                  (480, 320, 1),
                                  'drawable-hdpi/splash-landscape':
                                  (480, 320, 1.5),
                                  'drawable-xhdpi/splash-landscape':
                                  (480, 320, 2),
                                  'drawable-xxhdpi/splash-landscape':
                                  (480, 320, 3),
                                  'drawable-xxxhdpi/splash':
                                  (480, 320, 4)}},
           'toolbar': {'ios': {'{filename}.imageset/{filename}':
                               (22, None, 1),
                               '{filename}.imageset/{filename}@2x':
                               (22, None, 2),
                               '{filename}.imageset/{filename}@3x':
                               (22, None, 3)},
                       'android': {'drawable-ldpi/{filename}':
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
                                   'drawable-ldpi/{filename}-small':
                                   (16, 16, 0.75),
                                   'drawable-mdpi/{filename}-small':
                                   (16, 16, 1),
                                   'drawable-hdpi/{filename}-small':
                                   (16, 16, 1.5),
                                   'drawable-xhdpi/{filename}-small':
                                   (16, 16, 2),
                                   'drawable-xxhdpi/{filename}-small':
                                   (16, 16, 3),
                                   'drawable-xxxhdpi/{filename}-small':
                                   (16, 16, 4)}},
           'tab': {'ios': {'{filename}.imageset/{filename}':
                           (25, None, 1),
                           '{filename}.imageset/{filename}@2x':
                           (25, None, 2),
                           '{filename}.imageset/{filename}@3x':
                           (25, None, 3)},
                   'android': {'drawable-ldpi/{filename}':
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
                               (24, 24, 4)}},
           'notification': {'android': {'drawable-ldpi/{filename}':
                                        (22, 22, 0.75),
                                        'drawable-mdpi/{filename}':
                                        (22, 22, 1),
                                        'drawable-hdpi/{filename}':
                                        (22, 22, 1.5),
                                        'drawable-xhdpi/{filename}':
                                        (22, 22, 2),
                                        'drawable-xxhdpi/{filename}':
                                        (22, 22, 3),
                                        'drawable-xxxhdpi/{filename}':
                                        (22, 22, 4)}},
           'favicon': {'universal': {'favicon-60': (60, 60, 1),
                                     'favicon-60@2x': (60, 60, 2),
                                     'favicon-60@3x': (60, 60, 3),
                                     'favicon-76': (76, 76, 1),
                                     'favicon-76@2x': (76, 76, 2),
                                     'favicon-16': (16, 16, 1),
                                     'favicon-32': (32, 32, 1),
                                     'favicon-64': (64, 64, 1),
                                     'favicon-96': (96, 96, 1),
                                     'favicon-160': (160, 160, 1),
                                     'favicon-196': (196, 196, 1)}},
           'image': {'ios': {'{filename}.imageset/{filename}':
                             (None, None, 1),
                             '{filename}.imageset/{filename}@2x':
                             (None, None, 2),
                             '{filename}.imageset/{filename}@3x':
                             (None, None, 3)},
                     'android': {'drawable-ldpi/{filename}':
                                 (None, None, 0.75),
                                 'drawable-mdpi/{filename}': (None, None, 1),
                                 'drawable-hdpi/{filename}': (None, None, 1.5),
                                 'drawable-xhdpi/{filename}': (None, None, 2),
                                 'drawable-xxhdpi/{filename}': (None, None, 3),
                                 'drawable-xxxhdpi/{filename}':
                                 (None, None, 4)}
                     }}


def supported_devices():
    return ['ios', 'android']


def supported_types():
    return _sizes_.keys()


def make_images(image, image_name, to_object, type,
                allowed_devices=supported_devices(), baseline_scale=3):
    allowed_devices.append('universal')
    original_image_width, original_image_height = image.size
    if type not in _sizes_:
        raise RuntimeError('Error: no such icon type')
    devices = _sizes_[type]
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
            image_path = os.path.join(device_path,
                                      name + _image_format_[1])
            if scale > baseline_scale:
                print('Warning: {} scale {} is bigger than base line scale {}'.
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
                    print('Warning: {} is already exists'.format(image_path))
                    continue
            if width > original_image_width or height > original_image_height:
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
                        default=supported_devices(),
                        nargs='+',
                        choices=supported_devices(),
                        help='including devices')
    parser.add_argument('--zip', '-z', action='store_const', const=True)
    args = parser.parse_args()
    if not args.target_path:
        args.target_path = os.path.join(os.path.dirname(args.icon_path),
                                        args.icon_type)
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
