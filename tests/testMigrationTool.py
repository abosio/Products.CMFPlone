#
# MigrationTool tests
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from zope.component import getUtility

from Products.CMFPlone.tests import PloneTestCase
from Products.CMFPlone.interfaces import IMigrationTool

class TestMigrationTool(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        # Some methods need an Acquistion context
        self.migration = getUtility(IMigrationTool).__of__(self.portal)

    def testMigrationFinished(self):
        self.assertEqual(self.migration.getInstanceVersion(),
                         self.migration.getFileSystemVersion(),
                         'Migration failed')

    def testMigrationNeedsUpgrading(self):
        self.failIf(self.migration.needUpgrading(),
                    'Migration needs upgrading')

    def testMigrationNeedsUpdateRole(self):
        self.failIf(self.migration.needUpdateRole(),
                    'Migration needs role update')

    def testMigrationNeedsRecatalog(self):
        self.failIf(self.migration.needRecatalog(),
                    'Migration needs recataloging')

    def testForceMigrationFromUnsupportedVersion(self):
        version = '2.0.5'
        while version is not None:
            version, msg = self.migration._upgrade(version)
        expect = 'Migration stopped at version 2.0.5.'
        self.assertEqual(msg[0], expect)

    def testForceMigration(self):
        self.setRoles(['Manager'])
        # Make sure we don't embarrass ourselves again...
        version = '2.1'
        while version is not None:
            version, msg = self.migration._upgrade(version)
        expect = 'Migration completed at version %s.' % \
                 self.migration.getFileSystemVersion()
        self.assertEqual(msg[0], expect)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMigrationTool))
    return suite

if __name__ == '__main__':
    framework()
