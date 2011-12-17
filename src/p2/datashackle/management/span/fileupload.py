# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2011
# Author: Michael Jenny

from sqlalchemy import orm
from zope.component import getUtility

from p2.datashackle.core import model_config
from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.core.models.setobject_types import SetobjectType, setobject_table_registry
from p2.datashackle.core.models.linkage import Linkage
from p2.datashackle.core.models.media import Media
from p2.datashackle.core.models.relation import Relation
from p2.datashackle.management.span.span import SpanType


@model_config(tablename='p2_span_fileupload', maporder=3)
class Fileupload(SpanType):
   
    fileupload_label_width = 50
    fileupload_label_height = 50
    
    @classmethod
    def map_computed_properties(cls):
        cls.sa_map_dispose()
        fileupload_table = setobject_table_registry.lookup_by_class(cls.__module__, cls.__name__)
        inherits = SpanType._sa_class_manager.mapper
        orm.mapper(Fileupload,
                   fileupload_table,
                   inherits=inherits,
                   polymorphic_identity='fileupload',
                   properties=Fileupload.mapper_properties,
                  )

    def __init__(self, span_name=None):
        self.css_style = "left:" + str(self.label_width) + "px; width:" + str(self.fileupload_label_width) + "px; height:" + str(self.fileupload_label_height) + "px; "
        
        self.relation = Relation('MANY_TO_ONE')
        self.linkage = Linkage()
        # Set the linkage's relation to this form's relation
        self.linkage.relation = self.relation
        super(Fileupload, self).__init__(span_name)
    
    def post_order_traverse(self, mode):
        if mode == 'save':
            source_type = self.op_setobject_type
            self.relation.source_table = source_type.get_table_name()
            self.relation.target_table = Media.get_table_name()
            self.relation.create_relation('LIST')
    
    def _get_info(self):
        info = {}
        if self.operational:
            info['media_id'] = None
            info['has_thumbnail'] = False
            info['file_name'] = None
            info['collection_id'] = self.setobject.collections[self.linkage.attr_name]['collection_id']
            info['attr_name'] = self.linkage.attr_name
            if self.media != None:
                info['has_thumbnail'] = self.media.thumbnail and True or False
                info['media_id'] = self.media.id
                info['file_name'] = self.media.filename
        return info
    
    def make_operational(self, setobject):
        super(Fileupload, self).make_operational(setobject)
        self.media = getattr(setobject, self.linkage.attr_name)

    @property
    def get_media_id(self):
        try:
            return self.media.id
        except AttributeError:
            return 0
    media_id = get_media_id
