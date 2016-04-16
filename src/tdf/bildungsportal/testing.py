# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import tdf.bildungsportal


class TdfBildungsportalLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=tdf.bildungsportal)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'tdf.bildungsportal:default')


TDF_BILDUNGSPORTAL_FIXTURE = TdfBildungsportalLayer()


TDF_BILDUNGSPORTAL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TDF_BILDUNGSPORTAL_FIXTURE,),
    name='TdfBildungsportalLayer:IntegrationTesting'
)


TDF_BILDUNGSPORTAL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TDF_BILDUNGSPORTAL_FIXTURE,),
    name='TdfBildungsportalLayer:FunctionalTesting'
)


TDF_BILDUNGSPORTAL_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        TDF_BILDUNGSPORTAL_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='TdfBildungsportalLayer:AcceptanceTesting'
)
