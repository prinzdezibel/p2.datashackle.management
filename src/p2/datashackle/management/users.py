# -*- coding: utf-8 -*-
# Copyright(C) projekt-und-partner, 2011
# Author: Michael Jenny 

import grok
import dolmen.content

from dolmen.content.interfaces import IContent, IContainer
from grokcore.content.interfaces import IContext
from zope.component import queryUtility, getUtility
from zope.interface import Interface
from zope.location.interfaces import ILocation, IContained
from zope.principalregistry.principalregistry import principalRegistry
from zope.publisher.interfaces.http import IHTTPRequest
from zope.schema import TextLine
from zope.schema.fieldproperty import FieldProperty
from zope.security.interfaces import IGroupAwarePrincipal

from p2.datashackle.management.folder import Folder
from p2.container.listing import FolderListing
from p2.datashackle.core import globals
from p2.datashackle.management.interfaces import IUsers, IUserPreferences
from p2.datashackle.management.userpreferences import UserPreferences



class UsersListing(FolderListing):
    """Make the user listing view the index view."""
    grok.context(IUsers)
    grok.name('index') 

     
class Users(Folder):
    dolmen.content.nofactory()
    dolmen.content.schema(IUsers)
    grok.implements(IUsers)


    def __setstate__(self, state):
        super(Users, self).__setstate__(state)
        add_users(self)
        

@grok.subscribe(Users, grok.IObjectAddedEvent)
def users_folder_added(obj, event):
    add_users(obj)    


def add_users(users_folder):
    # First, add the zope.manager user preference, if the principal exists
    for principal in principalRegistry.getPrincipals(''):
        if not IGroupAwarePrincipal.providedBy(principal):
            # Group principal
            continue

        if principal.id == 'zope.manager':
            # Delete the object and re-create it
            if users_folder.get(principal.title):
                del users_folder[principal.title]
        
            preferences = IUserPreferences(principal)
            preferences.title = principal.title

            globals.manager_preferences = users_folder[principal.title] = preferences

    # Do it again for all other principals
    for principal in principalRegistry.getPrincipals(''):
        if not IGroupAwarePrincipal.providedBy(principal):
            # Group principal
            continue
        if principal.id != 'zope.manager':
            # Delete the object and re-create it
            if users_folder.get(principal.title):
                del users_folder[principal.title]
        
            preferences = IUserPreferences(principal)
            preferences.title = principal.title
            users_folder[principal.title] = preferences





        
