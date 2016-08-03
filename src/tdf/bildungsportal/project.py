from tdf.bildungsportal import MessageFactory as _
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
        raise Invalid(u'Please choose at least one school subject.')
    return True


def vocabSchoolsubjects(context):
    # For add forms

    # For other forms edited or displayed
    from tdf.bildungsportal.center import IBCenter
    while context is not None and not IBCenter.providedBy(context):
        # context = aq_parent(aq_inner(context))
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
        raise Invalid(u'Please choose at least one class level.')
    return True


def vocabClasslevel(context):
    # For add forms

    # For other forms edited or displayed
    from tdf.bildungsportal.center import IBCenter
    while context is not None and not IBCenter.providedBy(context):
        # context = aq_parent(aq_inner(context))
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
        # context = aq_parent(aq_inner(context))
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
        # context = aq_parent(aq_inner(context))
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
    __doc__ = _(u"It is necessary that you accept the Legal Declaration")


class ProvideScreenshotLogo(Invalid):
    __doc__ = _(u"Please add a Screenshot or a Logo to your project")


class IBProject(model.Schema):
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"Project Title - minimum 5 and maximum 50 characters"),
        min_length=5,
        max_length=50
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u"Project Summary"),
    )

    dexteritytextindexer.searchable('details')
    form.primary('details')
    details = RichText(
        title=_(u"Full Project Description"),
        required=False
    )

    dexteritytextindexer.searchable('schoolsubjects_choice')
    form.widget(schoolsubjects_choice=CheckBoxFieldWidget)
    schoolsubjects_choice = schema.List(
        title=_(u"School Subject"),
        description=_(u"Please choose an appropriate school subject (multiple selections possible)."),
        value_type=schema.Choice(source=vocabSchoolsubjects),
        constraint=isNotEmptySchoolsubject,
        required=True
    )

    dexteritytextindexer.searchable('classlevel_choice')
    form.widget(classlevel_choice=CheckBoxFieldWidget)
    classlevel_choice = schema.List(
        title=_(u"Class Level"),
        description=_(u"Please choose an appropriate class level (multiple selections possible)."),
        value_type=schema.Choice(source=vocabClasslevel),
        constraint=isNotEmptyClasslevel,
        required=True
    )

    contactAddress = schema.ASCIILine(
        title=_(u"Contact email-address"),
        description=_(u"Contact email-address for the project."),
        constraint=validateEmail
    )

    homepage = schema.URI(
        title=_(u"Homepage"),
        description=_(
            u"If the project has an external home page, enter its URL (example: 'http://www.mysite.org')."),
        required=False
    )

    project_logo = NamedBlobImage(
        title=_(u"Logo"),
        description=_(u"Add a logo for the project (or organization/company) by clicking the 'Browse' button."),
        required=False,
    )

    screenshot = NamedBlobImage(
        title=_(u"Screemshot of the Project"),
        description=_(u"Add a screenshot by clicking the 'Browse' button."),
        required=False,
    )

    form.mode(title_declaration_legal='display')
    title_declaration_legal = schema.TextLine(
        title=_(u""),
        required=False,
        defaultFactory=legal_declaration_title
    )

    form.mode(declaration_legal='display')
    declaration_legal = schema.Text(
        title=_(u""),
        required=False,
        defaultFactory=legal_declaration_text

    )

    accept_legal_declaration = schema.Bool(
        title=_(u"Accept the above legal disclaimer"),
        description=_(u"Please declare that you accept the above legal disclaimer"),
        required=True
    )

    form.widget(licenses_choice=CheckBoxFieldWidget)
    licenses_choice = schema.List(
        title=_(u'License of the uploaded files'),
        description=_(u"Please mark one or more licenses you publish your files"),
        value_type=schema.Choice(source=vocabAvailLicenses),
        required=True,
    )

    form.widget(compatibility_choice=CheckBoxFieldWidget)
    compatibility_choice = schema.List(
        title=_(u"Compatible with versions of LibreOffice"),
        description=_(u"Please mark one or more program versions with which this files are compatible with."),
        value_type=schema.Choice(source=vocabAvailVersions),
        required=True,
    )

    file = NamedBlobFile(
        title=_(u"The first file you want to upload"),
        description=_(u"Please upload your file."),
        required=True,
    )

    form.mode(information_further_file_uploads='display')
    model.primary('information_further_file_uploads')
    information_further_file_uploads = RichText(
        title=_(u"Further Fields for File uploads to this project"),
        description=_(
            u"If you want to upload further project files, you find the appropriate fields on the "
            u"register 'Further Files'."),
        required=False
    )

    form.fieldset('fileset1',
                  label=u"Further Files",
                  fields=['file1', 'file2', 'file3', 'file4']
                  )

    file1 = NamedBlobFile(
        title=_(u"The second file you want to upload"),
        description=_(u"Please upload your file."),
        required=False,
    )

    file2 = NamedBlobFile(
        title=_(u"The third file you want to upload"),
        description=_(u"Please upload your file"),
        required=False,
    )

    file3 = NamedBlobFile(
        title=_(u"The fourth file you want to upload"),
        description=_(u"Please upload your file."),
        required=False,
    )

    file4 = NamedBlobFile(
        title=_(u"The fifth file you want to upload"),
        description=_(u"Please upload your file."),
        required=False,
    )

    @invariant
    def legaldeclarationaccepted(data):
        if data.accept_legal_declaration is not True:
            raise AcceptLegalDeclaration(_(u"Please accept the Legal Declaration about "
                                           u"the files you'll upload"))

    @invariant
    def missingScreenshotOrLogo(data):
        if not data.screenshot and not data.project_logo:
            raise ProvideScreenshotLogo(_(u'Please add a Screenshot or a Logo to your project page'))


    @invariant
    def licensenotchoosen(value):
        if not value.licenses_choice:
            raise Invalid(_(u"Please choose a license for your file(s)."))


    @invariant
    def compatibilitynotchoosen(data):
        if not data.compatibility_choice:
            raise Invalid(_(u"Please choose one or more compatible LibreOffice versions for your file(s)"))




class ValidateBProjectUniqueness(validator.SimpleFieldValidator):
    # Validate site-wide uniqueness of project titles.

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
