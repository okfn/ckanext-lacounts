from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit
from ckantoolkit.tests.factories import Sysadmin
import ckan.tests.helpers as helpers

import ckanext.lacounts.tests.factories as factories
from ckanext.lacounts.model import Event


class TestEventCreate():

    def _make_create_data_dict(self):
        data_dict = {
            'name': 'Title',
            'date': '2012-09-21',
            'free': 'yes'
        }
        return data_dict

    def test_event_create(self):
        '''Creating an event returns a dict with expected values'''
        sysadmin = Sysadmin()

        event_result = toolkit.get_action('event_create')(
            context={'user': sysadmin['name']},
            data_dict=self._make_create_data_dict()
        )

        nosetools.assert_true(isinstance(event_result, dict))
        nosetools.assert_true(event_result['name'] == 'Title')
        nosetools.assert_true(event_result['free'])
        nosetools.assert_true(event_result['date'] == '2012-09-21 00:00:00')


class TestEventUpdate(helpers.FunctionalTestBase):

    def test_event_update(self):
        '''Sysadmins can update an existing event'''
        sysadmin = Sysadmin()

        event = factories.Event(
            name='My Test Event',
            date='2010-09-21',
            free=True
        )

        event_result = toolkit.get_action('event_show')(
            data_dict={'id': event['id']}
        )

        nosetools.assert_true(event_result['name'] == 'My Test Event')
        nosetools.assert_true(event_result['date'] == '2010-09-21')
        nosetools.assert_true(event_result['free'])

        updated_event = toolkit.get_action('event_update')(
            context={'user': sysadmin['name']},
            data_dict={
                'id': event['id'],
                'name': 'My Updated Event',
                'date': '2013-09-21',
                'free': False
            }
        )

        nosetools.assert_true(updated_event['name'] == 'My Updated Event')
        nosetools.assert_true(updated_event['date'] == '2013-09-21 00:00:00')
        nosetools.assert_false(updated_event['free'])

    def test_event_update_bad_id(self):
        '''Bad event id raises ObjectNotFound.'''
        sysadmin = Sysadmin()

        with nosetools.assert_raises(toolkit.ObjectNotFound):
            toolkit.get_action('event_update')(
                context={'user': sysadmin['name']},
                data_dict={'id': 'bad-id'}
            )


class TestEventShow(helpers.FunctionalTestBase):

    def test_event_show(self):
        '''
        All users can see an event.
        '''
        event = factories.Event()

        event_result = toolkit.get_action('event_show')(
            data_dict={'id': event['id']}
        )

        nosetools.assert_true(isinstance(event_result, dict))
        nosetools.assert_true(event_result['name'] == 'Test Event')
        nosetools.assert_true(event_result['free'])
        nosetools.assert_true(
            event_result['url'] == 'http://example.com/my-event')
        nosetools.assert_true(event_result['date'] == '2012-09-21')

    def test_event_show_bad_id(self):
        '''
        Showing event with bad id returns ObjectNotFound.
        '''
        with nosetools.assert_raises(toolkit.ObjectNotFound):
            toolkit.get_action('event_show')(
                data_dict={
                    'id': 'blah-blah'
                }
            )


class TestEventDelete(helpers.FunctionalTestBase):

    def test_event_delete(self):
        '''
        Sysadmin can delete event.
        '''
        sysadmin = Sysadmin()
        event = factories.Event()

        # one event
        nosetools.assert_equal(Event.count(), 1)

        toolkit.get_action('event_delete')(
            context={'user': sysadmin['name']},
            data_dict={'id': event['id']}
        )

        # No events
        nosetools.assert_equal(Event.count(), 0)

    def test_event_delete_invalid_id(self):
        '''
        Calling event delete with invalid id raises ObjectNotFound.
        '''
        sysadmin = Sysadmin()
        context = {'user': sysadmin['name']}

        with nosetools.assert_raises(toolkit.ObjectNotFound):
            toolkit.get_action('event_delete')(
                context=context,
                data_dict={
                    'id': 'blah-blah'
                }
            )


class TestEventList(helpers.FunctionalTestBase):

    def test_event_list(self):
        '''
        All users can list events.
        '''
        factories.Event()
        factories.Event()
        factories.Event()

        event_result = toolkit.get_action('event_list')(
            data_dict={}
        )

        nosetools.assert_true(len(event_result) == 3)

    def test_event_list_empty(self):
        '''
        All users can list events.
        '''
        event_result = toolkit.get_action('event_list')(
            data_dict={}
        )

        nosetools.assert_true(len(event_result) == 0)
