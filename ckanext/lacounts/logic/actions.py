import logging

import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import ckan.lib.uploader as uploader
import ckan.logic.action.create as create_core
import ckan.logic.action.update as update_core
from ckan.logic import validate

from ckanext.lacounts.logic import schema
from ckanext.lacounts.model import Event, VolunteeringOpportunity

from ckan.model.meta import Session


log = logging.getLogger(__name__)


# Create Actions

@validate(schema.event_create_schema)
def event_create(context, data_dict):
    '''Create an Event'''
    toolkit.check_access('ckanext_lacounts_event_create', context, data_dict)

    event = Event.create(**data_dict)

    return event


@validate(schema.volunteering_create_schema)
def volunteering_create(context, data_dict):
    '''Create a Volunteering Opportunity'''
    toolkit.check_access('ckanext_lacounts_volunteering_create',
                         context, data_dict)

    volunteering = VolunteeringOpportunity.create(**data_dict)

    return volunteering


# Delete Actions

@validate(schema.event_delete_schema)
def event_delete(context, data_dict):
    '''Delete an Event'''
    toolkit.check_access('ckanext_lacounts_event_delete', context, data_dict)

    event = Event.get(id=data_dict['id'])

    if event is None:
        raise toolkit.ObjectNotFound

    event.delete()


@validate(schema.volunteering_delete_schema)
def volunteering_delete(context, data_dict):
    '''Delete a Volunteering Opportunity'''
    toolkit.check_access('ckanext_lacounts_volunteering_delete',
                         context, data_dict)

    volunteering = VolunteeringOpportunity.get(id=data_dict['id'])

    if volunteering is None:
        raise toolkit.ObjectNotFound

    volunteering.delete()


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
@validate(schema.volunteering_show_schema)
def volunteering_show(context, data_dict):
    '''Show a Volunteering Opportunity'''
    toolkit.check_access('ckanext_lacounts_volunteering_show',
                         context, data_dict)

    volunteering = VolunteeringOpportunity.get(id=data_dict['id'])

    if volunteering is None:
        raise toolkit.ObjectNotFound

    return volunteering.as_dict()


@toolkit.side_effect_free
@validate(schema.event_list_schema)
def event_list(context, data_dict):
    '''List of Events'''
    toolkit.check_access('ckanext_lacounts_event_show', context, data_dict)

    events = Event.list(**data_dict)

    return events


@toolkit.side_effect_free
@validate(schema.volunteering_list_schema)
def volunteering_list(context, data_dict):
    '''List of Volunteering Opportunities.'''
    toolkit.check_access('ckanext_lacounts_volunteering_show', context,
                         data_dict)

    volunteering = VolunteeringOpportunity.list(**data_dict)

    return volunteering


@toolkit.side_effect_free
@validate(schema.publishers_list_schema)
def publishers_list(context, data_dict):
    '''List of Publishers suitable for home page visualization.

    [
        {
            "id": 8ba00479-47ec-4dc0-9f10-dc9619302c03,
            "slug": "county-of-los-angeles",
            "title": "County of Los Angeles",
            "value": 84,
            "package": "county",
            "url": "/publisher/county-of-los-angeles"
        },
        ...
    ]
    '''
    res = Session.execute("""
SELECT public.group.title, public.group.name AS slug,
       public.group.id, public.group_extra.value AS package,
       (SELECT count(*) FROM public.package
        WHERE public.package.owner_org=public.group.id
        AND public.package.private=False) AS value
FROM public.group
INNER JOIN public.group_extra ON public.group_extra.group_id=public.group.id
WHERE public.group_extra.key='publisher_type'
AND public.group.state='active'
AND public.group.type='publisher'
""").fetchall()
    out = [dict(r, url='/publisher/{}'.format(r.slug)) for r in res]

    for item in out:
        item['package'] = item['package'].capitalize()
    return out


# Update Actions

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


@validate(schema.volunteering_update_schema)
def volunteering_update(context, data_dict):
    '''Update an Volunteering Opportunities'''
    toolkit.check_access('ckanext_lacounts_volunteering_create',
                         context, data_dict)

    volunteering = VolunteeringOpportunity.get(id=data_dict['id'])

    if volunteering is None:
        raise toolkit.ObjectNotFound

    ignored_keys = ['id']

    for k, v in data_dict.items():
        if k not in ignored_keys:
            setattr(volunteering, k, v)

    updated_volunteering = volunteering.save()

    return updated_volunteering


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
