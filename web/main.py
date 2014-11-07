#!/usr/bin/env python
# coding=utf-8

import os
import StringIO
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import urllib2

import webapp2
from google.appengine.api import files
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import jinja2

from PIL import Image

from icons import make_images, supported_types


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),
                                   'template')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

    def post(self):
        image_type = self.request.get('type', 'icon')
        if image_type not in supported_types():
            image_type = 'icon'
        file = StringIO.StringIO(self.request.get('file'))
        zip_file = StringIO.StringIO()
        with closing(ZipFile(zip_file, 'w', ZIP_DEFLATED)) as tmp:
            image = Image.open(file)
            make_images(image, image_type, tmp, image_type,
                        None, 3)
        zip_file.seek(0)
        file_name = files.blobstore.create(mime_type=
                                           'application/x-zip-compressed',
                                           _blobinfo_uploaded_filename=
                                           image_type)
        with files.open(file_name, 'a') as f:
            f.write(zip_file.read())
        files.finalize(file_name)
        blob_key = files.blobstore.get_blob_key(file_name)
        self.response.write('/downloads/' + str(blob_key))


class DownloadPage(blobstore_handlers.BlobstoreDownloadHandler):

    def get(self, blob_key):
        resource = str(urllib2.unquote(blob_key))
        blob_info = blobstore.BlobInfo.get(resource)
        self.response.content_type = 'application/x-zip-compressed'
        filename = blob_info.filename
        if not isinstance(filename, str):
            filename = filename.encode('utf-8')
        self.response.headers.add('Content-Disposition',
                                  'attachment; filename=' +
                                  filename + '.zip')
        self.send_blob(blob_info)


application = webapp2.WSGIApplication([
    (r'/', MainPage),
    (r'/downloads/([^/]+)', DownloadPage),
], debug=os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'))
