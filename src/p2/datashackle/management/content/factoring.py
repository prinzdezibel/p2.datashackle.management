# -*- coding: utf-8 -*-
import dolmen.content
import grok
from p2.datashackle.management.interfaces import IDatashackleContentFactory
from zope.schema.fieldproperty import FieldProperty


class DatashackleContentFactory(dolmen.content.Factory):
    grok.implements(IDatashackleContentFactory)

    addtraversal = FieldProperty(IDatashackleContentFactory['addtraversal'])

