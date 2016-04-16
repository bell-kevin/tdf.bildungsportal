from tdf.bildungsportal import MessageFactory as _
from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema
from Products.Five import BrowserView
from Acquisition import aq_inner
from plone import api
from plone.directives import form
from zope import schema
from plone.app.layout.viewlets import ViewletBase
from plone.app.multilingual.dx import directives


class IBCenter(model.Schema):



    title= schema.TextLine(
        title=_(u"Name des Bildungsportals"),
    )

    description=schema.Text(
        description=_(u"Beschreibung des Bildungsportals"),
    )


    available_schoolsubjects = schema.List(title=_(u"Schulfach"),
                                           default=['Deutsch',
                                                    'Mathematik',],
                                           value_type=schema.TextLine())


    available_licenses =schema.List(title=_(u"Available Licenses"),
        default=['CC-by-sa-v3 (Creative Commons Attribution-ShareAlike 3.0)',
                 'CC-by-sa-v4 (Creative Commons Attribution-ShareAlike 4.0)',],
        value_type=schema.TextLine())

    available_versions = schema.List(title=_(u"Available Versions"),
        default=['LibreOffice 3.3',
                 'LibreOffice 3.4',
                 'LibreOffice 3.5',
                 'LibreOffice 3.6',
                 'LibreOffice 4.0',
                 'LibreOffice 4.1',
                 'LibreOffice 4.2',
                 'LibreOffice 4.3',
                 'LibreOffice 4.4',
                 'LibreOffice 5.0',
                 'LibreOffice 5.1'],
        value_type=schema.TextLine())




    title_legaldisclaimer = schema.TextLine(
        title=_(u"Title for Legal Disclaimer and Limitations"),
        default=_(u"Legal Disclaimer and Limitations"),
        required=False
    )


    legal_disclaimer = schema.Text(
        title=_(u"Text of the Legal Disclaimer and Limitations"),
        description=_(u"Enter the text of the legal disclaimer and limitations that should be displayed to the project creator and should be accepted by the owner of the project."),
        default=_(u"Fill in the legal disclaimer, that had to be accepted by the project owner"),
        required=False
    )


    title_legaldownloaddisclaimer = schema.TextLine(
        title=_(u"Title of the Legal Disclaimer and Limitations for Downloads"),
        default=_(u"Legal Disclaimer and Limitations for Downloads"),
        required=False
    )

    form.primary('legal_downloaddisclaimer')
    legal_downloaddisclaimer = RichText(
        title=_(u"Text of the Legal Disclaimer and Limitations for Downlaods"),
        description=_(u"Enter any legal disclaimer and limitations for downloads that should appear on each page for dowloadable files."),
        default=_(u"Fill in the text for the legal download disclaimer"),
        required=False
    )

    releaseAllert=schema.ASCIILine(
        title=_(u"EMail address for the messages about new releases"),
        description=_(u"Enter a email address to which information about a new release should be send"),
        required=False
    )



class IBCenterView(BrowserView):
    pass
