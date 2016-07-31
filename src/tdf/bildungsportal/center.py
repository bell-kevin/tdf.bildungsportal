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
    title = schema.TextLine(
        title=_(u"Name of the educational portal"),
    )

    description = schema.Text(
        description=_(u"Description of the educational portal"),
    )

    available_schoolsubjects = schema.List(title=_(u"Scool Subjects"),
                                           default=['Deutsch',
                                                    'Englisch',
                                                    'Erdkunde',
                                                    'Geschichte',
                                                    'Mathematik',
                                                    'Religion'
                                                    ],
                                           value_type=schema.TextLine())

    available_licenses = schema.List(title=_(u"Licenses"),
                                     default=['CC-by-sa-v3 (Creative Commons Attribution-ShareAlike 3.0)',
                                              'CC-by-sa-v4 (Creative Commons Attribution-ShareAlike 4.0)', ],
                                     value_type=schema.TextLine())

    available_versions = schema.List(title=_(u"LibreOffice Versions"),
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
                                              'LibreOffice 5.1',
                                              'LibreOffice 5.2'],
                                     value_type=schema.TextLine())

    available_classlevel = schema.List(title=_(u"Class Level"),
                                       default=['Jahrgangsstufe 1',
                                                'Jahrgangsstufe 2',
                                                'Jahrgangsstufe 3',
                                                'Jahrgangsstufe 4',
                                                'Jahrgangsstufe 5',
                                                'Jahrgangsstufe 6',
                                                'Jahrgangsstufe 7',
                                                'Jahrgangsstufe 8',
                                                'Jahrgangsstufe 9',
                                                'Jahrgangsstufe 10 - Sek-I',
                                                'Jahrgangsstufe 10 - Sek-II'
                                                'Jahrgangsstufe 11',
                                                'Jahrgangsstufe 12',
                                                'Jahrgangsstufe 13'],
                                       value_type=schema.TextLine())

    title_legaldisclaimer = schema.TextLine(
        title=_(u"Title for Legal Disclaimer and Limitations"),
        default=_(u"Legal Disclaimer And Limitations"),
        required=False
    )

    legal_disclaimer = schema.Text(
        title=_(u"Text of the Legal Disclaimer and Limitations"),
        description=_(
            u"Enter the text of the legal disclaimer and limitations that should be displayed "
            u"to the project creator and should be accepted by the owner of the project."),
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
        description=_(u"Enter any legal disclaimer and limitations for downloads that should "
                      u"appear on each page for dowloadable files."),
        default=_(u"Fill in the text for the legal download disclaimer"),
        required=False
    )

    releaseAllert = schema.ASCIILine(
        title=_(u"EMail address for the messages about new releases"),
        description=_(u"Enter a email address to which information about a new release should be send"),
        required=False
    )


class BCenterView(BrowserView):
    def get_latest_projects(self):
        self.catalog = api.portal.get_tool(name='portal_catalog')
        sort_on = 'created'
        contentFilter = {
            'sort_on': sort_on,
            'sort_order': 'reverse',
            'review_state': 'published',
            'portal_type': 'tdf.bildungsportal.project'}

        results = self.catalog(**contentFilter)

        return results

    def get_most_popular_projects(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        sort_on = 'positive_ratings'
        contentFilter = {
            'sort_on': sort_on,
            'sort_order': 'reverse',
            'review_state': 'published',
            'portal_type': 'tdf.bildungsportal.project'}
        return catalog(**contentFilter)

    def get_latest_libreoffice_release(self):
        """Get the latest version from the vocabulary. This only
        goes by string sorting so would need to be reworked if the
        LibreOffice versions dramatically changed"""

        versions = list(self.context.available_versions)
        versions.sort(reverse=True)
        return versions[0]

    def schoolsubject_name(self):
        schoolsubject = list(self.context.available_schoolsubjects)
        return schoolsubject

    def classlevel_name(self):
        classlevel = list(self.context.available_class_level)
        return classlevel

    def get_products(self, schoolsubject, version, classlevel, sort_on, SearchableText=None):
        self.catalog = api.portal.get_tool(name='portal_catalog')
        sort_on = 'positive_ratings'
        contentFilter = {
            'sort_on': sort_on,

            'SearchableText': SearchableText,
            'sort_order': 'reverse',
            'portal_type': 'tdf.bildungsportal.project'}

        if version != 'any':
            contentFilter['getCompatibility'] = version

        if schoolsubject != 'any':
            contentFilter['getSchoolsubject'] = schoolsubject

        if classlevel != 'any':
            contentFilter['getClasslevel'] = classlevel

        return self.catalog(**contentFilter)
