# -*- coding: utf-8 -*-
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.interface import Interface
from zope.location.interfaces import ILocation
from zope.schema import TextLine, ASCII, ASCIILine, Choice
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from p2.datashackle.management import MF as _

languages = SimpleVocabulary(
    [SimpleTerm(value=u'', title=_(u'Browser default')),
    SimpleTerm(value=u'de', title=_(u'German')),
    SimpleTerm(value=u'en', title=_(u'English')),
    ])

class IDatashackle(Interface):
    """A Datashackle application."""

class ITranslatableDescriptiveProperties(IDCDescriptiveProperties):
    """Translatable properties for content objects."""

class IFolder(ITranslatableDescriptiveProperties):
    """A folderish, translatable content type."""

class IListingDefault(Interface):
    """A view whose default is the folderlisting."""

class IGenericSet(IFolder):
    """A dolmen-ish content type that wraps a plan."""
    title = TextLine(
        title = _(u"Name of the plan"),
        required = True
        )

    table_identifier = ASCIILine(
        title = _(u"Name of the underlying table"),
        description = _(u"Name of the table where the field values of this plan's forms are stored."),
        required = True,
        )

    table_key_field = ASCIILine(
        title = _(u"Primary-Key"),
        description = _(u"Name of the primary key table field."),
        required = True,
        default='id'
        )
    
    plan_identifier = ASCIILine(
        title=u"Plan identifier",
        required=False
        )
        
class IUsers(IFolder):
    """A container object that holds UserInfo objects that represent user preferences."""
        
class ILocationProvider(Interface):
    """Provides means to make a p2.plan instance locatable to address it by URL. """

class IListOnlyFolder(IFolder):
    """A translatable folder that has only the folderlisting view (for non-admins)."""

class IUserPreferences(Interface):
    """The content object that is used to set the users (prinicpals) preferrences like language and date format."""
    
    title = TextLine(
        title=_(u"User"),
        required=True
        )
    
    preferred_date = Choice(title=_(u"Date format"),
                      vocabulary=languages,
                      required=False,
                      default=u''
                      )

    preferred_lang = Choice(title=_(u"Language"),
                      vocabulary=languages,
                      required=False,
                      default=u''
                      )
        

