# -*- coding: utf-8 -*-
# Copyright projekt-und-partner.de, 2011
# Author: Michael Jenny

import grok
import json

from cStringIO import StringIO
from PIL import Image
from zope.interface import Interface
from zope.component import getUtility
from zope.mimetype.interfaces import IMimeTypeGetter

from p2.datashackle.core.models.media import Media
from p2.datashackle.core.models.identity import generate_random_identifier
from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.management.interfaces import IDatashackle


class Upload(grok.View):
    grok.name('upload')
    grok.context(IDatashackle)
    

    def create_thumbnail(self, original_file, size):
        if not isinstance(size, tuple) or len(size) != 2:
            raise ValueError('Size must be a (width, height) tuple.')

        original_image = Image.open(original_file)
        image = original_image.copy()
        image.thumbnail(size, Image.ANTIALIAS)
        thumbnailIO = StringIO()
        image.save(thumbnailIO, original_image.format, quality=90)
        thumbnailIO.seek(0)
        original_file.seek(0)
        return thumbnailIO
        
    def update(self):
        self.error = False
        self.response.setHeader('Content-Type', 'application/json')
        
        upload_file = self.request.form['file']
        size = self.request.getHeader('X-File-Size')
        thumbnail_width = int(self.request.getHeader('X-thumbnail-width'))
        thumbnail_height = int(self.request.getHeader('X-thumbnail-height'))
        self.filename = self.request.getHeader('X-File-Name')
        mime_type = getUtility(IMimeTypeGetter)(name=self.filename, data=upload_file)
        
        thumbnail_file = None
        if mime_type in ('image/jpeg', 'image/png', 'image/gif'):
            thumbnail_file = self.create_thumbnail(upload_file, (thumbnail_width, thumbnail_height))

        if not mime_type:
            mime_type = upload_file.headers('Content-Type')

        self.identifier = generate_random_identifier()
        media = Media()
        media.id = self.identifier
        media.mime_type = mime_type
        media.size = size
        media.filename = self.filename
        
        # Check maximum file size first:
        db_util = getUtility(IDbUtility)
        if int(media.size) > db_util.max_allowed_packet:
            # Problem: Database does not allow BLOBs of this size.
            self.error = True
            self.message = 'The selected file is too big. Please contact your system administrator.'
            self.title = 'Upload failed.'
            upload_file.close()
            if thumbnail_file:
                thumbnail_file.close()
            return    
        
        # Read data:
        chunk = upload_file.read()
        while chunk != '':
            # Initialise our data array
            if media.data == None:
                media.data = bytearray()
            # Add data
            media.data += chunk
            # Check maximum length
            if len(media.data) > int(media.size):
                # Cancel upload here so uploader cannot throw an endless stream of bytes at us
                self.error = True
                self.message = 'The selected file is bigger than specified.'
                self.title = 'Upload failed.'
                upload_file.close()
                if thumbnail_file:
                    thumbnail_file.close()
                return
            chunk = upload_file.read()
        upload_file.close()
        
        self.has_thumbnail = thumbnail_file and True or False
        if thumbnail_file:
            chunk = thumbnail_file.read()
            while chunk != '':
                if media.thumbnail == None:
                    media.thumbnail = bytearray()
                media.thumbnail += chunk
                chunk = thumbnail_file.read()
            thumbnail_file.close()       
        
        session = db_util.Session()    
        session.add(media)
        session.commit()
        
    def render(self):
        if self.error:
            response = {'error': {'message': self.message,
                                  'title': self.title
                                 }
                       }
        else:
            response = {'result': {'id': self.identifier,
                                   'has_thumbnail': self.has_thumbnail,
                                   'file_name': self.filename,
                                  }
                       }
        return json.dumps(response)
            

class Serve(grok.View):
    grok.name('media')
    grok.context(IDatashackle)

    def get(self):
        id = self.request.get('id')
        session = getUtility(IDbUtility).Session()
        return session.query(Media).filter_by(id=id).first()
        
    def update(self):
        self.thumbnail = self.request.get('thumbnail')
        self.media = self.get()
        if self.media == None:
            self.request.response.setStatus(404)
            return
        # Media found
        
        mime_type = self.media.mime_type
        self.request.response.setHeader('Content-Type', mime_type)
        
        # mime types that can't/shouldn't be handled by the browser will be offered as download
        if mime_type in ('application/octet-stream'):
            self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s"' % self.media.filename)    
       
    def render(self):
        if self.media != None:
            if self.thumbnail != None:
                return self.media.thumbnail
            else:
                return self.media.data
