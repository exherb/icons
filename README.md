# icons

generate icons and config file (e.g. Contents.json) required by app in ios or android, inspired by http://makeappicon.com

## web version

[iconographys](http://iconographys.appspot.com/)

## cli version

### install

just run `pip install icons`. if you are using pyenv, then run `pyenv rehash`

### usage

```bash
icons [-o TARGET_PATH] [--baseline BASELINE]
      [--type {launch,notification,image,tab,webclip,toolbar,icon}]
      [--devices {ios,android} [{ios,android} ...]] [--zip]
      icon_path
```

* icon_path - the source image path
* target_path(optional) - the target path
* baseline(optional) - baseline scale. the default is 3, and it's mean the source image is at @3x scale
* type(optional) - icon type, the default is icon
* devices(optional) - including only devices

## destop version

Working on it...
