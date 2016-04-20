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


    available_licenses =schema.List(title=_(u"Lizenzen"),
        default=['CC-by-sa-v3 (Creative Commons Attribution-ShareAlike 3.0)',
                 'CC-by-sa-v4 (Creative Commons Attribution-ShareAlike 4.0)',],
        value_type=schema.TextLine())

    available_versions = schema.List(title=_(u"LibreOffice Versionen"),
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


    available_class_level = schema.List(title=_(u"Klassenstufen"),
         default=['Klassenstufe 1',
                  'Klassenstufe 2',
                  'Klassenstufe 3',
                  'Klassenstufe 4',
                  'Klassenstufe 5',
                  'Klassenstufe 6',
                  'Klassenstufe 7',
                  'Klassenstufe 8',
                  'Klassenstufe 9',
                  'Klassenstufe 10',
                  'Klassenstufe 11',
                  'Klassenstufe 12',
                  'Klassenstufe 13'],
         value_type=schema.TextLine())




    title_legaldisclaimer = schema.TextLine(
        title=_(u"Titel Haftungsausschluss und -begrenzung"),
        default=_(u"Haftungsausschluss und -begrenzung"),
        required=False
    )


    legal_disclaimer = schema.Text(
        title=_(u"Text von Haftungsausschluss und Begrenzung"),
        description=_(u"Bitte den Text von Haftungsausschluss und -begrenzung eintragen, der vom Ersteller eines Projektes akzeptiert werden musss."),
        default=_(u"Fill in the legal disclaimer, that had to be accepted by the project owner"),
        required=False
    )


    title_legaldownloaddisclaimer = schema.TextLine(
        title=_(u"Titel Hauftungsausschluss und -begrenzung zu Downloads"),
        default=_(u"Hauftungsausschluss und -begrenzung zu Downloads"),
        required=False
    )

    form.primary('legal_downloaddisclaimer')
    legal_downloaddisclaimer = RichText(
        title=_(u"Text von Haftungsausschluss und -begrenzung zu Downloads"),
        description=_(u"Bitte den Text von Haftungsausschluss und -begrenzung zu Downloads hier eintragen, der auf jeder Projektseite bei den Downloads angezeigt wird."),
        default=_(u"Bitte den Text zu Haftungsausschluss und -begrenzung bei Downloads hier eintragen."),
        required=False
    )

    releaseAllert=schema.ASCIILine(
        title=_(u"EMail address for the messages about new releases"),
        description=_(u"Enter a email address to which information about a new release should be send"),
        required=False
    )



class BCenterView(BrowserView):


    def get_latest_projects(self):
        self.catalog = api.portal.get_tool(name='portal_catalog')
        sort_on = 'created'
        contentFilter = {
                          'sort_on' : sort_on,
                          'sort_order' : 'reverse',
                          'review_state': 'published',
                          'portal_type':'tdf.bildungsportal.project'}

        results = self.catalog(**contentFilter)

        return results



    def get_most_popular_projects(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        sort_on = 'positive_ratings'
        contentFilter = {
                         'sort_on' : sort_on,
                         'sort_order': 'reverse',
                         'review_state': 'published',
                         'portal_type' : 'tdf.bildungsportal.project'}
        return catalog(**contentFilter)



    def get_latest_libreoffice_release(self):
        """Get the latest version from the vocabulary. This only
        goes by string sorting so would need to be reworked if the
        LibreOffice versions dramatically changed"""

        versions = list(self.context.available_versions)
        versions.sort(reverse=True)
        return versions[0]


