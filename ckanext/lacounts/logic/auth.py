import ckan.plugins.toolkit as toolkit


def event_create(context, data_dict):
    '''Only sysadmins can create events.'''
    return {'success': False}


def event_delete(context, data_dict):
    '''Only sysadmins can delete events.'''
    return {'success': False}


@toolkit.auth_allow_anonymous_access
def event_show(context, data_dict):
    '''All can show events.'''
    return {'success': True}
