# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
import logging
from dolmen.app.container.listing import FolderListing
from dolmen.app.layout import Add, Edit, Delete, ContextualMenu
import dolmen.forms.base as form
from dolmen.forms.crud.interfaces import IFactoryAdding
from dolmen.forms.crud.utils import getSchemaFields
from dolmen.menu import menuentry
from zope.cachedescriptors.property import CachedProperty


import dolmen.app.layout as layout
import dolmen.content
from grokcore import view, viewlet
from dolmen.app.content import icon
from dolmen.forms.crud.crudforms import Add,Edit
from dolmen.forms.crud.interfaces import IFactoryAdding
from megrok import resource
from sqlalchemy import Table, String, Column
from zope.catalog.interfaces import ICatalog
from zope.component import getUtility
from zope.schema.fieldproperty import FieldProperty

from p2.datashackle.core.app.exceptions import *
from p2.datashackle.core.app.setobjectreg import setobject_table_registry, setobject_type_registry
from p2.datashackle.core.sql import table_exists
from p2.datashackle.core.globals import metadata
from p2.datashackle.management.interfaces import IGenericSet
from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.core.models import identity
from p2.datashackle.core.models.form import FormType
from p2.datashackle.core.models.plan import fetch_plan, Plan
from p2.datashackle.core.models.setobject_types import create_setobject_type

   

class GenericSetFactory(dolmen.content.Factory):
    """Custom genericset factory allows to specify a custom addform."""
    dolmen.content.name('p2.datashackle.management.generic_set.GenericSet')
    addform = u'genericsetaddform'   

 
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
    
    if genericset.table_identifier.startswith('p2_'):
        # Don't do anything for system tables that are created on application init.
        return

    #TODO: Remove me
    if genericset.table_identifier == 'test':
        return # Test tables created at application init time. 
    
    plan_identifier = identity.generate_random_identifier()
    genericset.plan_identifier = plan_identifier
    table_identifier = genericset.table_identifier
    
    # update the genericset index
    catalog = getUtility(ICatalog)
    catalog.updateIndex(catalog['plan_identifier'])
    
    if not table_exists(table_identifier): 
        # Create SA table type
        table_type = Table(
            table_identifier,
            metadata,
            Column(genericset.table_key_field, String(8), primary_key=True, autoincrement=False),
            mysql_engine='InnoDB'
        )    
        # Newly created setobjects live always in 'p2.datashackle.core.models.setobject_types'
        # and the class name equals the table identifier.
        so_module = 'p2.datashackle.core.models.setobject_types'
        so_classname = genericset.table_identifier
        # Register table type
        setobject_table_registry.register_type(so_module, so_classname, table_identifier, table_type)
        
        # Even if the user gives a specialized class and module we create a 
        # generic so_type first, because the specialized class definition will not exist until the
        # user defines it in the source code and restarts the server.
        setobject_type = create_setobject_type(table_identifier)
        
        # DDL
        table_type.create()
    else:
        # find so_type class for table
        so_type = setobject_type_registry.lookup_by_table(table_identifier)
        so_module = so_type.__module__
        so_classname = so_type.__name__

    session = getUtility(IDbUtility).Session()
    plan = Plan(objid=plan_identifier)
    plan.so_module = so_module
    plan.so_type = so_classname
    form = FormType(objid=None,
        plan=plan,
        form_name='default_form',
        width=550,
        height=200)
    plan.register_form(form)
    plan.set_default(form)
    session.add(plan)
    session.commit()



@menuentry(ContextualMenu, order=30)
class EditView(Edit):
    grok.context(IGenericSet)
 
    @CachedProperty
    def fields(self):
        return getSchemaFields(
            self, self.getContentData().getContent(),
            '__parent__', 'plan_identifier', 'description')


class AddView(Add):
    """A custom addform to add a GenericSet. It omits the plan_identifier field.
    """
    grok.context(IFactoryAdding)
    # The name the ++add++ traversal adapter uses to lookup the add form as a named multi-adapter.
    grok.name('genericsetaddform')

    @CachedProperty
    def fields(self):
        return getSchemaFields(
            self, self.context.factory.factory, '__parent__', 'plan_identifier', 'description')


@menuentry(ContextualMenu, order=40)
class DeleteView(Delete):
    grok.context(IGenericSet)
    grok.name('delete')
    grok.title(u"Delete")

@menuentry(ContextualMenu, order=50)
class ListingView(FolderListing):
    grok.name('folderlisting')
    grok.context(IGenericSet)


