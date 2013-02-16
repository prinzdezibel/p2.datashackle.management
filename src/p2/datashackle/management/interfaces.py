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
        
class IPlan(Interface):
    """Represents different views onto objects. The objects has different properties.
    The ´Plan´ does not only represent the values of the objects itself
    (the instances), but also the blueprint (e.g. which properties does it have)
    of the object (the type). The ´Plan's´ different views are manifested
    through a collection of ´Forms´ it holds. The ´Plan´ is wired with a table
    in a relational database.
    """

class IFormType(Interface):
    """IFormType represents a visualization of a table record as form.
    Represents a ´Form´ in "type mode" that works on the fields (or a subset) of
    a table in the relational database. A ´Form´ is a domain thing that is
    composed out of ´Widgets´. In "design mode", the form may be changed
    in layout and function by authorized users. E.g. new fields may be added to the form.
    In "setobject mode", new instances of
    the form may be created which can be filled out by the user which are eventually saved in db.
    """
class IWidgetType(Interface):
    pass

class ISpanType(Interface):
    pass

