import logging

import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import ckan.lib.uploader as uploader
import ckan.logic.action.update as update_core
from ckan.logic import validate

from ckanext.lacounts.logic import schema
from ckanext.lacounts.model import Event

log = logging.getLogger(__name__)


# Create Actions

@validate(schema.event_create_schema)
def event_create(context, data_dict):
    '''Create an Event'''
    toolkit.check_access('ckanext_lacounts_event_create', context, data_dict)

    event = Event.create(**data_dict)

    return event


@validate(schema.event_update_schema)
def event_update(context, data_dict):
    '''Update an Event'''
    toolkit.check_access('ckanext_lacounts_event_create', context, data_dict)

    event = Event.get(id=data_dict['id'])

    if event is None:
        raise toolkit.ObjectNotFound

    ignored_keys = ['id']

    for k, v in data_dict.items():
        if k not in ignored_keys:
            setattr(event, k, v)

    updated_event = event.save()

    return updated_event


# Delete Actions

@validate(schema.event_delete_schema)
def event_delete(context, data_dict):
    '''Delete an Event'''
    toolkit.check_access('ckanext_lacounts_event_delete', context, data_dict)

    event = Event.get(id=data_dict['id'])

    if event is None:
        raise toolkit.ObjectNotFound

    event.delete()


# Show Actions

@toolkit.side_effect_free
@validate(schema.event_show_schema)
def event_show(context, data_dict):
    '''Show an Event'''
    toolkit.check_access('ckanext_lacounts_event_show', context, data_dict)

    event = Event.get(id=data_dict['id'])

    if event is None:
        raise toolkit.ObjectNotFound

    return event.as_dict()


@toolkit.side_effect_free
@validate(schema.event_list_schema)
def event_list(context, data_dict):
    '''List of Events'''
    toolkit.check_access('ckanext_lacounts_event_show', context, data_dict)

    events = Event.list(**data_dict)

    return events


# Update Actions

def config_option_update(context, data_dict):
    # https://github.com/ckan/ckan/blob/master/ckan/logic/action/update.py#L1198

    # Handle featured image
    if 'ckanext.lacounts.featured_image' in data_dict:
        upload = uploader.get_uploader('admin')
        upload.update_data_dict(
            data_dict,
            'ckanext.lacounts.featured_image',
            'featured_image_upload',
            'clear_featured_image_upload')
        upload.upload(uploader.get_max_image_size())
        value = data_dict['ckanext.lacounts.featured_image']
        if value \
           and not value.startswith('http') \
           and not value.startswith('/'):
            image_path = 'uploads/admin/'
            value = h.url_for_static('{0}{1}'.format(image_path, value))
        data_dict['ckanext.lacounts.featured_image'] = value

    return update_core.config_option_update(context, data_dict)
