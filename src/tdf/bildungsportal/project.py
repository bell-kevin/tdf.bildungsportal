from tdf.extensionuploadcenter import MessageFactory as _
from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema
from plone.autoform import directives as form
from plone.dexterity.browser.view import DefaultView
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import directlyProvides

from zope.security import checkPermission
from zope.interface import invariant, Invalid
from Acquisition import aq_inner, aq_parent, aq_get, aq_chain
from plone.namedfile.field import NamedBlobFile
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.directives import form
from zope import schema

from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from Products.validation import V_REQUIRED
from plone import api
from collective import dexteritytextindexer
from Products.Five import BrowserView
import re
from plone.namedfile.field import NamedBlobImage






checkEmail = re.compile(
    r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}").match

def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u"Invalid email address"))
    return True



class IBProject(model.Schema):

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Titel"),
        description=_(u"Projekt Titel - Minimum 5 und Maximum 50 Zeichen"),
        min_length=5,
        max_length=50
    )

    dexteritytextindexer.searchable('Beschreibung')
    description = schema.Text(
        title=_(u"Projekt Kurzbeschreibung"),
    )

    dexteritytextindexer.searchable('details')
    form.primary('details')
    details = RichText(
        title=_(u"Projekt-Beschreibung"),
        required=False
    )






    contactAddress=schema.ASCIILine(
        title=_(u"Kontakt E-Mail-Adresse"),
        description=_(u"Kontakt E-Mail-Adresse zum Projekt."),
        constraint=validateEmail
    )

    homepage=schema.URI(
        title=_(u"Homepage"),
        description=_(u"Falls das Projekt eine externe Homepage hat, tragen Sie die URL (Beispiel: 'http://www.mysite.org') hier ein."),
        required=False
    )

    project_logo = NamedBlobImage(
        title=_(u"Logo"),
        description=_(u"Verwenden Sie den Durchsuchen-Knopf, um das Projekt-Logo auszusuchen."),
        required=False,
    )

    screenshot = NamedBlobImage(
        title=_(u"Bildschirmfoto des Projekts"),
        description=_(u"Verwenden Sie den Durchsuchen-Knopt, um die Datei mit einem Bildschirmfoto auszusuchen."),
        required=False,
    )



    file = NamedBlobFile(
        title=_(u"Erste hochzuladende Datei"),
        description=_(u"Bitte laden Sie Ihre Datei hoch."),
        required=True,
    )



    form.mode(information_further_file_uploads='display')
    model.primary('information_further_file_uploads')
    information_further_file_uploads = RichText(
        title = _(u"Weitere Felder zum Hochladen von Projekt-Dateien"),
        description = _(u"Falls Sie weitere Projekt-Dateien hochladen wollen, finden Sie entsprechende Felder auf dem Register 'Datei Hochladen 1'."),
        required = False
     )

    form.fieldset('fileset1',
        label=u"Datei Hochladen 1",
        fields=['file1', 'file2', 'file3', 'file4']
    )

    file1 = NamedBlobFile(
        title=_(u"Zweite hochzuladende Datei"),
        description=_(u"Bitte laden Sie Ihre Datei hoch."),
        required=True,
    )


    file2 = NamedBlobFile(
        title=_(u"Dritte hochzuladende Datei"),
        description=_(u"Bitte laden Sie Ihre Datei hoch."),
        required=True,
    )


    file3 = NamedBlobFile(
        title=_(u"Vierte hochzuladende Datei"),
        description=_(u"Bitte laden Sie Ihre Datei hoch."),
        required=True,
    )


    file4 = NamedBlobFile(
        title=_(u"Fuenfte hochzuladende Datei"),
        description=_(u"Bitte laden Sie Ihre Datei hoch."),
        required=True,
    )








class BProjectView(BrowserView):
    pass
