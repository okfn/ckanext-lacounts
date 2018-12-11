from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers

from ckanext.lacounts.model import create_tables, tables_exist


class TestEventCreateAuth(helpers.FunctionalTestBase):

    def setup(self):
        '''Reset the database and clear the search indexes.'''
        super(TestEventCreateAuth, self).setup()

        # set up lacounts tables
        if not tables_exist():
            create_tables()

    def test_event_create_no_user(self):
        '''
        Calling event create with no user raises NotAuthorized.
        '''
        context = {'user': None, 'model': None}
        nosetools.assert_raises(toolkit.NotAuthorized, helpers.call_auth,
                                'ckanext_lacounts_event_create',
                                context=context)

    def test_event_create_correct_creds(self):
        '''
        Calling event create by a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': None}
        helpers.call_auth('ckanext_lacounts_event_create', context=context)


class TestEventDeleteAuth(helpers.FunctionalTestBase):

    def setup(self):
        '''Reset the database and clear the search indexes.'''
        super(TestEventDeleteAuth, self).setup()

        # set up lacounts tables
        if not tables_exist():
            create_tables()

    def test_event_delete_no_user(self):
        '''
        Calling event delete with no user raises NotAuthorized.
        '''
        context = {'user': None, 'model': None}
        nosetools.assert_raises(toolkit.NotAuthorized, helpers.call_auth,
                                'ckanext_lacounts_event_delete',
                                context=context)

    def test_event_delete_correct_creds(self):
        '''
        Calling event delete by a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': None}
        helpers.call_auth('ckanext_lacounts_event_delete', context=context)


class TestEventShowAuth(helpers.FunctionalTestBase):

    def setup(self):
        '''Reset the database and clear the search indexes.'''
        super(TestEventShowAuth, self).setup()

        # set up lacounts tables
        if not tables_exist():
            create_tables()

    def test_event_show_no_user(self):
        '''
        Calling event show with no user doesn't raise NotAuthorized.
        '''
        context = {'user': '', 'model': None}
        helpers.call_auth('ckanext_lacounts_event_show', context=context)

    def test_event_show_sysadmin(self):
        '''
        Calling event show by a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': None}
        helpers.call_auth('ckanext_lacounts_event_show', context=context)
