# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
from dolmen.app.container.listing import FolderListing
from dolmen.app.layout import Add, Edit, Delete, ContextualMenu
import dolmen.forms.base as form
from dolmen.forms.crud.utils import getSchemaFields
from dolmen.menu import menuentry
from zope.cachedescriptors.property import CachedProperty


import dolmen.app.layout as layout
import dolmen.content
from grokcore import view, viewlet
from dolmen.app.content import icon
from dolmen.forms.crud.crudforms import Edit
from dolmen.forms.crud.interfaces import IFactoryAdding
from megrok import resource
from sqlalchemy import String, Column, Table
from zope.catalog.interfaces import ICatalog
from zope.component import getUtility
from zope.schema import TextLine
from zope.schema.fieldproperty import FieldProperty

from p2.datashackle.core.app.exceptions import *
from p2.datashackle.core.app.setobjectreg import setobject_table_registry, setobject_type_registry
from p2.datashackle.core.sql import table_exists
from p2.datashackle.core.globals import metadata
from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.core.models import identity
from p2.datashackle.core.models.setobject_types import create_setobject_type
from p2.datashackle.management.interfaces import IGenericSet, IDatashackleContentFactory
from p2.datashackle.management.content.factoring import DatashackleContentFactory
from p2.datashackle.management.form.form import FormType
from p2.datashackle.management.plan.plan import fetch_plan, Plan
   



class GenericSetFactory(DatashackleContentFactory):
    """Custom genericset factory allows to specify a custom addform."""
    dolmen.content.name('GenericSet')
    addform = u'addmodelview'   
    addtraversal = u'addmodel'

 
class GenericSet(dolmen.content.Container):
    """An user defined collection type."""
    grok.implements(IGenericSet)
    dolmen.content.name(u"Objektverwaltung")
    dolmen.content.schema(IGenericSet)
    dolmen.content.factory(GenericSetFactory)
    icon('generic_set.png')
    plan_identifier = FieldProperty(IGenericSet['plan_identifier'])


    @property    
    def plan(self):
        # Create plan
        plan = fetch_plan(self)
        # I was thinking that the next assignment triggers the Catalog index implictly. But that's obviously not 
        # the case, therefore we update the index manually thereafter.
        self.plan_identifier = str(plan.plan_identifier) # Comes as unicode from database, but schema is ASCIILine
        # Indexing our updated plan_identifier value:
        catalog = getUtility(ICatalog)
        catalog.updateIndex(catalog['plan_identifier'])
        self._v_plan = plan
        return self._v_plan

class GenericSetTraverser(grok.Traverser):
    grok.context(IGenericSet)
    
    def traverse(self, name):
        return self.context.plan.traverse(name)


@grok.subscribe(GenericSet, grok.IObjectAddedEvent)
def genericset_added(genericset, event):
    """A new GenericSet was added. Create the setobject type for it.
    """
 
    plan_identifier = genericset.plan_identifier
    table_identifier = genericset.table_identifier
    
    # update the genericset index
    catalog = getUtility(ICatalog)
    catalog.updateIndex(catalog['plan_identifier'])
    
    if not table_exists(table_identifier): 
        # Create SA table type
        table_type = Table(
            table_identifier,
            metadata,
            Column(genericset.table_key_field, String(10), primary_key=True, autoincrement=False),
            mysql_engine='InnoDB'
        )    
    
        # Register table type
        setobject_table_registry.register_type(genericset.klass,
                                               table_identifier,
                                               table_type)
        
        # Even if the user gives a specialized class and module we create a 
        # generic klass first, because the specialized class definition will not exist until the
        # user defines it in the source code and restarts the server.
        setobject_type = create_setobject_type(genericset.klass, table_identifier)
        
        # DDL
        table_type.create()
    #else:
    #    # find klass class for table
    #    so = setobject_type_registry.lookup_by_table(table_identifier)
    #    klass = so.__name__

    #session = getUtility(IDbUtility).Session()
    #plan = Plan(plan_identifier, klass, table_identifier)
    ##plan.klass = klass
    #form = FormType(
    #    plan=plan,
    #    form_name='default_form'
    #)
    #plan.register_form(form)
    #plan.set_default(form)
    #session.add(plan)
    #session.commit()
    



@menuentry(ContextualMenu, order=30)
class EditView(Edit):
    grok.context(IGenericSet)
 
    @CachedProperty
    def fields(self):
        return getSchemaFields(
            self, self.getContentData().getContent(),
            '__parent__', 'plan_identifier', 'description')


@menuentry(ContextualMenu, order=40)
class DeleteView(Delete):
    grok.context(IGenericSet)
    grok.name('delete')
    grok.title(u"Delete")

@menuentry(ContextualMenu, order=50)
class ListingView(FolderListing):
    grok.name('folderlisting')
    grok.context(IGenericSet)



