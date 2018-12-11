import factory

from ckantoolkit.tests import helpers

from ckanext.lacounts.model import Event


def _get_action_user_name(kwargs):
    '''Return the name of the user in kwargs, defaulting to the site user
    It can be overriden by explictly setting {'user': None} in the keyword
    arguments. In that case, this method will return None.
    '''

    if 'user' in kwargs:
        user = kwargs['user']
    else:
        user = helpers.call_action('get_site_user')

    if user is None:
        user_name = None
    else:
        user_name = user['name']

    return user_name


class Event(factory.Factory):
    '''A factory class for creating ckanext lacounts Events.'''

    FACTORY_FOR = Event

    # These are the default params that will be used to create new Events.
    name = 'Test Event'
    date = '2012-09-21'
    free = True
    url = 'http://example.com/my-event'

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        context = {'user': _get_action_user_name(kwargs)}

        dataset_dict = helpers.call_action('event_create',
                                           context=context, **kwargs)
        return dataset_dict
