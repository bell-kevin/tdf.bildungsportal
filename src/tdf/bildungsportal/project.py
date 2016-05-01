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
from z3c.form import validator
from plone.uuid.interfaces import IUUID
from plone.dexterity.browser.view import DefaultView






checkEmail = re.compile(
    r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}").match

def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u"Invalid email address"))
    return True



def isNotEmptySchoolsubject(value):
    if not value:
        raise Invalid(u'Bitte zumindest ein Schulfach vorgeben.')
    return True


def vocabSchoolsubjects(context):
    # For add forms

    # For other forms edited or displayed
    from tdf.bildungsportal.center import IBCenter
    while context is not None and not IBCenter.providedBy(context):
        #context = aq_parent(aq_inner(context))
        context = context.__parent__

    schoolsubjects_list = []
    if context is not None and context.available_schoolsubjects:
        schoolsubjects_list = context.available_schoolsubjects

    terms = []
    for value in schoolsubjects_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)
directlyProvides(vocabSchoolsubjects, IContextSourceBinder)



def isNotEmptyClasslevel(value):
    if not value:
        raise Invalid(u'Bitte zumindest eine Klassenstufe vorgeben.')
    return True


def vocabClasslevel(context):
    # For add forms

    # For other forms edited or displayed
    from tdf.bildungsportal.center import IBCenter
    while context is not None and not IBCenter.providedBy(context):
        #context = aq_parent(aq_inner(context))
        context = context.__parent__

    classlevel_list = []
    if context is not None and context.available_classlevel:
        classlevel_list = context.available_classlevel

    terms = []
    for value in classlevel_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)
directlyProvides(vocabClasslevel, IContextSourceBinder)

def vocabAvailVersions(context):
    """ pick up licenses list from parent """
    # For other forms edited or displayed
    from tdf.bildungsportal.center import IBCenter
    while context is not None and not IBCenter.providedBy(context):
        #context = aq_parent(aq_inner(context))
        context = context.__parent__

    versions_list = []
    if context is not None and context.available_versions:
        versions_list = context.available_versions

    terms = []
    for value in versions_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)
directlyProvides(vocabAvailVersions, IContextSourceBinder)


def vocabAvailLicenses(context):
    """ pick up licenses list from parent """
    # For other forms edited or displayed
    from tdf.bildungsportal.center import IBCenter
    while context is not None and not IBCenter.providedBy(context):
        #context = aq_parent(aq_inner(context))
        context = context.__parent__

    licenses_list = []
    if context is not None and context.available_licenses:
        licenses_list = context.available_licenses

    terms = []
    for value in licenses_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)
directlyProvides(vocabAvailLicenses, IContextSourceBinder)



@provider(IContextAwareDefaultFactory)
def legal_declaration_title(context):
    return context.title_legaldisclaimer


@provider(IContextAwareDefaultFactory)
def legal_declaration_text(context):
    return context.legal_disclaimer


class AcceptLegalDeclaration(Invalid):
    __doc__ = _(u"Bitte akzeptieren Sie den Haftungsausschluss")


class ProvideScreenshotLogo(Invalid):
    __doc__ =  _(u"Please add a Screenshot or a Logo to your project")


class IBProject(model.Schema):

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Titel"),
        description=_(u"Projekt Titel - Minimum 5 und Maximum 50 Zeichen"),
        min_length=5,
        max_length=50
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u"Projekt Kurzbeschreibung"),
    )

    dexteritytextindexer.searchable('details')
    form.primary('details')
    details = RichText(
        title=_(u"Projekt-Beschreibung"),
        required=False
    )



    dexteritytextindexer.searchable('schoolsubjects_choice')
    form.widget(schoolsubjects_choice=CheckBoxFieldWidget)
    schoolsubjects_choice = schema.List(
        title=_(u"Schulfach"),
        description=_(u"Bitte ein passendes Schulfach (auch mehrere Nennungen) vorgeben."),
        value_type=schema.Choice(source=vocabSchoolsubjects),
        constraint = isNotEmptySchoolsubject,
        required=True
    )

    dexteritytextindexer.searchable('classlevel_choice')
    form.widget(classlevel_choice=CheckBoxFieldWidget)
    classlevel_choice = schema.List(
        title=_(u"Klassenstufe"),
        description=_(u"Bitte eine passende Klassenstufe (auch mehrere Nennungen) vorgeben."),
        value_type=schema.Choice(source=vocabClasslevel),
        constraint = isNotEmptyClasslevel,
        required=True
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


    form.mode(title_declaration_legal='display')
    title_declaration_legal=schema.TextLine(
        title=_(u""),
        required=False,
        defaultFactory = legal_declaration_title
    )


    form.mode(declaration_legal='display')
    declaration_legal = schema.Text(
        title=_(u""),
        required=False,
        defaultFactory = legal_declaration_text

    )

    accept_legal_declaration=schema.Bool(
        title=_(u"Akzeptieren des obigen Haftungsausschluss"),
        description=_(u"Bitte akzeptieren Sie den obigen Haftungsausschluss"),
        required=True
    )

    form.widget(licenses_choice=CheckBoxFieldWidget)
    licenses_choice= schema.List(
        title=_(u'Lizenz der hochgeladenen Dateien'),
        description=_(u"Bitte eine oder mehrere Lizenzen der hochgeladenen Dateien vorgeben."),
        value_type=schema.Choice(source=vocabAvailLicenses),
        required=True,
    )



    form.widget(compatibility_choice=CheckBoxFieldWidget)
    compatibility_choice= schema.List(
        title=_(u"Dateien sind getestet mit folgenden LibreOffice Versionen"),
        description=_(u"Bitte markieren Sie die LibreOffice Versionen, mit denen die Dateien getestet wurden."),
        value_type=schema.Choice(source=vocabAvailVersions),
        required=True,
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
        description = _(u"Falls Sie weitere Projekt-Dateien hochladen wollen, finden Sie entsprechende Felder auf dem Register 'Weitere Dateien'."),
        required = False
     )

    form.fieldset('fileset1',
        label=u"Weitere Dateien",
        fields=['file1', 'file2', 'file3', 'file4']
    )

    file1 = NamedBlobFile(
        title=_(u"Zweite hochzuladende Datei"),
        description=_(u"Bitte laden Sie Ihre Datei hoch."),
        required=False,
    )


    file2 = NamedBlobFile(
        title=_(u"Dritte hochzuladende Datei"),
        description=_(u"Bitte laden Sie Ihre Datei hoch."),
        required=False,
    )


    file3 = NamedBlobFile(
        title=_(u"Vierte hochzuladende Datei"),
        description=_(u"Bitte laden Sie Ihre Datei hoch."),
        required=False,
    )


    file4 = NamedBlobFile(
        title=_(u"Fuenfte hochzuladende Datei"),
        description=_(u"Bitte laden Sie Ihre Datei hoch."),
        required=False,
    )

    @invariant
    def legaldeclarationaccepted(data):
        if data.accept_legal_declaration is not True:
           raise AcceptLegalDeclaration(_(u"Bitte akzeptieren Sie den Haftungsausschluss zum Hochladen Ihrer Dateien"))



    @invariant
    def missingScreenshotOrLogo(data):
        if not data.screenshot and not data.project_logo:
            raise ProvideScreenshotLogo(_(u'Please add a Screenshot or a Logo to your project page'))



class ValidateBProjectUniqueness(validator.SimpleFieldValidator):
    #Validate site-wide uniqueness of project titles.


    def validate(self, value):
        # Perform the standard validation first
        super(ValidateBProjectUniqueness, self).validate(value)

        if value is not None:
            catalog = api.portal.get_tool(name='portal_catalog')
            results = catalog({'Title': value,
                               'object_provides': IBProject.__identifier__})

            contextUUID = IUUID(self.context, None)
            for result in results:
                if result.UID != contextUUID:
                    raise Invalid(_(u"The project title is already in use"))

validator.WidgetValidatorDiscriminators(
    ValidateBProjectUniqueness,
    field=IBProject['title'],
)




class BProjectView(DefaultView):

    def releaseDate(self):
        return self.context.toLocalizedTime()
