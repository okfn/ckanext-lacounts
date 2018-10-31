import json
import urllib
import logging
import urlparse
from ckan import model
from ckan.common import config
from ckan.plugins import toolkit
log = logging.getLogger(__name__)


def get_image_for_group(group_name, return_path=False):
    '''
    Render an inline svg snippet for the named group (topic). These groups
    correlate with those created by the `create_featured_topics` command.
    '''
    jinja_env = toolkit.config['pylons.app_globals'].jinja_env
    groups = {
        'education': 'icons/book.svg',
        'environment': 'icons/leaf.svg',
        'health': 'icons/heart.svg',
        'housing': 'icons/keys.svg',
        'immigration': 'icons/passport.svg',
        'transportation': 'icons/bus.svg'
    }

    # Fetch svg template if there is one, otherwise return empty string.
    try:
        path = groups[group_name]
        if return_path:
            return path
        svg = jinja_env.get_template(path)
    except KeyError as e:
        return ""

    img = toolkit.literal("<span class='image %s'>" % group_name
                          + svg.render() + "</span>")
    return img


def get_related_datasets_for_form(selected_ids=[], exclude_ids=[]):
    context = {'model': model}

    # Get search results
    search_datasets = toolkit.get_action('package_search')
    search = search_datasets(context, {
        'fq': 'dataset_type:dataset',
        'include_private': False,
        'sort': 'organization asc, title asc',
    })

    # Get orgs
    orgs = []
    current_org = None
    selected_ids = selected_ids if isinstance(selected_ids, list) else selected_ids.strip('{}').split(',')
    for package in search['results']:
        if package['id'] in exclude_ids:
            continue
        if package['owner_org'] != current_org:
            current_org = package['owner_org']
            orgs.append({'text': package['organization']['title'], 'children': []})
        dataset = {'text': package['title'], 'value': package['id']}
        if package['id'] in selected_ids:
            dataset['selected'] = 'selected'
        orgs[-1]['children'].append(dataset)

    return orgs


def get_related_datasets_for_display(value):
    context = {'model': model}

    # Get datasets
    datasets = []
    ids = value if isinstance(value, list) else value.strip('{}').split(',')
    for id in ids:
        try:
            dataset = toolkit.get_action('package_show')(context, {'id': id})
            href = toolkit.url_for('dataset_read', id=dataset['name'], qualified=False)
            datasets.append({'text': dataset['title'], 'href': href})
        except toolkit.ObjectNotFound:
            pass

    return datasets


def get_metadata_completion_rate(package):
    # Item could be a field name or a list of field names (any match counts)
    # The result is a dict: {rate, count, total}
    GROUPS = [
        'title',
        'owner_org',
        'notes',
        'metadata_created',
        'metadata_modified',
        'contact_email',
        'identifier',
        'access_rights',
        'license_title',
        ['spatial_text', 'spatial'],
        ['temporal_text', 'temporal_start', 'temporal_end'],
        'frequency',
    ]

    # Count
    count = 0
    for group in GROUPS:
        fields = group if isinstance(group, list) else [group]
        for field in fields:
            value = package.get(field)
            if field == 'license_title' and value == 'License not specified':
                value = None
            if value:
                count += 1
                break

    # Compose
    completion = {
        'count': count,
        'total': len(GROUPS),
        'percentage': int(100 * (count/float(len(GROUPS)))),
    }

    return completion


def get_recent_data_stories(limit=4):
    showcases = []
    items = toolkit.get_action('ckanext_showcase_list')({'model': model}, {})
    for item in items:
        showcase = toolkit.get_action('package_show')({'model': model}, {'id': item['id']})
        if (not showcase.get('image_display_url') or
                showcase.get('story_type') == 'Blog post'):
            continue
        showcases.append(showcase)
        if len(showcases) == limit:
            continue
    return showcases


def get_featured_image_url(default):
    return config.get('ckanext.lacounts.featured_image') or default


def get_editable_region(name):
    try:
        regions = json.loads(config.get('ckanext.lacounts.editable_regions', '{}'))
        return regions[name]
    except Exception:
        return ''


def get_package_stories(package_name):
    try:
        stories = toolkit.get_action('package_search')({'model': model}, {
            'q': 'dataset_names:%s' % package_name,
            'fq': 'dataset_type:showcase',
        })['results']
        return stories
    except Exception as exception:
        log.exception(exception)
        return []


def get_topics(current_url=''):
    topics = []
    names = sorted(['education', 'environment', 'housing', 'immigration', 'transportation', 'health'])
    dicts = toolkit.get_action('group_list')({'model': model}, {'all_fields': True, 'type': 'topic'})
    for name in names:
        for topic in dicts:
            if name != topic['name']:
                continue
            if name in urlparse.parse_qs(urlparse.urlparse(current_url).query).get('groups', []):
                topic['selected'] = True
            topic['icon_path'] = get_image_for_group(name, return_path=True)
            if topic['name'] == 'health':
                topic['title'] = 'Health'  # Drop the 'Wellbeing'
            topics.append(topic)
    return topics


def update_url_query(url, params):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    query = dict((k,v) for k,v in query.iteritems() if v is not None)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)


def get_rounded_value(value):

    if isinstance(value, basestring):
        value = float(value)

    return unicode(round(value, 3))


def get_spatial_value(pkg_dict):
    text = pkg_dict.get('spatial_text')
    coords = geojson = None
    if pkg_dict.get('spatial'):
        if isinstance(pkg_dict['spatial'], basestring):
            try:
                geojson = json.loads(pkg_dict['spatial'])
            except ValueError:
                pass
        else:
            geojson = pkg_dict['spatial']
        if geojson:
            coords = ', '.join([
                get_rounded_value(geojson['coordinates'][0][0]),
                get_rounded_value(geojson['coordinates'][0][1]),
                get_rounded_value(geojson['coordinates'][2][0]),
                get_rounded_value(geojson['coordinates'][2][1]),
            ])
    if coords and text:
        return '{} ({})'.format(text, coords)
    elif text:
        return text
    elif coords:
        return coords
    return '-'


def get_temporal_value(pkg_dict):

    text = pkg_dict.get('temporal_start')
    start = pkg_dict.get('temporal_start')
    end = pkg_dict.get('temporal_end')

    if text:
        return text
    if start and end:
        return '{} - {}'.format(start, end)
    if start:
        return start
    if end:
        return end
    return '-'


def get_story_related_stories(story):
    context = {'model': model}
    value = story.get('related_stories', [])

    # Get stories
    stories = []
    ids = value if isinstance(value, list) else value.strip('{}').split(',')
    for id in ids:
        story = toolkit.get_action('package_show')(context, {'id': id})
        stories.append(story)

    return stories


def get_dataset_and_stories_counts(search_facets):
    datasets_count = stories_count = None
    for item in search_facets['items']:
        if item['name'] == 'Data':
            datasets_count = item['count']
        if item['name'] == 'Story':
            stories_count = item['count']
    return {
        'datasets': datasets_count,
        'stories': stories_count,
    }


def sort_facet_items(name):

    items = toolkit.h.get_facet_items_dict(name)

    items.sort(key=lambda it: it['display_name'].lower())

    return items


def get_publisher_type(publishers, name):
    for publisher in publishers:
        if publisher['name'] == name:
            return publisher.get('publisher_type', '')
    return ''


def get_organization_display_title(organization):
    if 'display_name' not in organization:
        organization = toolkit.get_action('organization_show')({'model': model}, {'id': organization['id']})
    return organization.get('display_title', organization['display_name'])


def get_resources_ordered(resources):
    downloadable_resources = []
    other_resources = []
    for resource in (resources or []):
        if resource.get('has_views') or resource.get('url_type') == 'upload':
            downloadable_resources.append(resource)
        else:
            other_resources.append(resource)
    return downloadable_resources + other_resources
