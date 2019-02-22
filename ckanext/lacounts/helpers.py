import json
import urllib
import logging
import urlparse
import hashlib
import datetime
from ckan import model
from ckan.common import config
from ckan.plugins import toolkit
log = logging.getLogger(__name__)


def get_image_for_group(group_name, return_path=False):
    '''
    Render an inline svg snippet for the named group (topic). These groups
    correlate with those created by the `create_topics` command.
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
    except KeyError:
        # TODO: provide default icon
        return ''

    img = toolkit.literal("<span class='image %s'>" % group_name
                          + svg.render() + "</span>")
    return img


def get_groups_for_form_using_id(selected_ids=[]):
    formGroups = []
    context = {'model': model}
    data_dict = {'all_fields': True, 'type': 'topic', 'include_extras': True}
    selected_ids = normalize_list(selected_ids)
    for group in toolkit.get_action('group_list')(context, data_dict):
        formGroup = {'text': group['title'], 'value': group['id']}
        if group['id'] in selected_ids:
            formGroup['selected'] = 'selected'
        formGroups.append(formGroup)
    return formGroups


# TODO: this helpers also exists in `ckanext.showcase`. Rename/merge?
def get_groups_for_form(selected_groups=[]):
    context = {'model': model}

    # Get groups
    groups = toolkit.get_action('group_list')(context, {
        'sort': 'title asc',
        'type': 'topic',
        'all_fields': True,
    })

    # Mark selected
    selected_names = map(lambda group: group['name'], selected_groups)
    for group in groups:
        if group['name'] in selected_names:
            group['selected'] = 'selected'

    return groups


# TODO: this helpers also exists in `ckanext.showcase`. Add-topic/rename/merge?
def get_related_datasets_for_form(selected_ids=[], exclude_ids=[], topic_name=None):
    context = {'model': model}

    # Get packages
    limit = 200  # ckan hard-limit is 1000
    page = 1
    packages = []
    while True:
        query = {
            'fq': 'dataset_type:dataset',
            'include_private': False,
            'sort': 'organization asc, title asc',
            'rows': limit,
            'start': limit * (page - 1),
        }
        if topic_name:
            query['q'] = 'groups:%s' % topic_name
        response = toolkit.get_action('package_search')(context, query)
        results = response.get('results', [])
        if len(results):
            packages.extend(results)
            page = page + 1
        else:
            break

    # Get orgs
    orgs = []
    current_org = None
    selected_ids = normalize_list(selected_ids)
    for package in packages:
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


# TODO: this helpers also exists in `ckanext.showcase`. Add-topic/rename/merge?
def get_related_stories_for_form(selected_ids=[], exclude_ids=[], topic_name=None):
    context = {'model': model}

    # Get packages
    limit = 200  # ckan hard-limit is 1000
    page = 1
    packages = []
    while True:
        query = {
            'fq': 'dataset_type:showcase',
            'include_private': False,
            'sort': 'organization asc, title asc',
            'rows': limit,
            'start': limit * (page - 1),
        }
        if topic_name:
            query['q'] = 'groups:%s' % topic_name
        response = toolkit.get_action('package_search')(context, query)
        results = response.get('results', [])
        if len(results):
            packages.extend(results)
            page = page + 1
        else:
            break

    # Get datasets
    datasets = []
    selected_ids = normalize_list(selected_ids)
    for package in packages:
        dataset = {'text': package['title'], 'value': package['id']}
        if package['id'] in exclude_ids:
            continue
        if package['id'] in selected_ids:
            dataset['selected'] = 'selected'
        datasets.append(dataset)

    return datasets


# TODO: this helpers also exists in `ckanext.showcase`. Rename/merge?
def get_related_datasets_for_display(value):
    context = {'model': model}

    # Get datasets
    datasets = []
    ids = normalize_list(value)
    for id in ids:
        try:
            dataset = toolkit.get_action('package_show')(context, {'id': id})
            href = toolkit.url_for('dataset_read', id=dataset['name'], qualified=False)
            datasets.append({'text': dataset['title'], 'href': href})
        except toolkit.ObjectNotFound:
            pass

    return datasets


# TODO: this helpers also exists in `ckanext.showcase`. Merge?
def get_related_stories_for_display(value):
    context = {'model': model}

    # Get datasets
    datasets = []
    ids = normalize_list(value)
    for id in ids:
        try:
            dataset = toolkit.get_action('package_show')(context, {'id': id})
            href = toolkit.url_for('ckanext_showcase_read', id=dataset['name'], qualified=False)
            datasets.append({'text': dataset['title'], 'href': href})
        except toolkit.ObjectNotFound:
            pass

    return datasets


def get_metadata_completion_rate(package):
    # Item could be a field name or a list of field names (any match counts)
    # The result is a dict: {rate, count, total}
    GROUPS = [

        # Description below the title
        'notes',

        # Metadata table
        'issued',
        'modified',
        'url',
        'contact_name',
        'contact_email',
        'identifier',
        'access_rights',
        'frequency',
        'language',
        'provenance',
        ['temporal_text', 'temporal_start', 'temporal_end'],
        ['spatial_text', 'spatial'],

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


def get_recent_data_stories(topic_name=None, limit=None):
    showcases = []
    items = toolkit.get_action('ckanext_showcase_list')({'model': model}, {})
    for item in items:
        try:
            showcase = toolkit.get_action('package_show')({'model': model}, {'id': item['id']})
        except toolkit.NotAuthorized:
            continue
        if (not showcase.get('image_display_url') or
                showcase.get('story_type') == 'Blog post'):
            continue

        if topic_name:
            has_topic = False
            for group in showcase.get('groups'):
                if group['name'] == topic_name:
                    has_topic = True
                    break
            if not has_topic:
                continue
        showcases.append(showcase)
        if len(showcases) == limit:
            break
    return showcases


def get_featured_data_stories(topic_dict, limit=None):
    context = {'model': model}
    value = topic_dict.get('featured_stories', [])

    # Get datasets
    stories = []
    ids = normalize_list(value)
    for id in ids:
        try:
            story = toolkit.get_action('package_show')(context, {'id': id, type: 'showcase'})
        except toolkit.ObjectNotFound:
            continue
        stories.append(story)
        if len(stories) == limit:
            break

    return stories


def get_featured_datasets(topic_dict, limit=None):
    context = {'model': model}
    value = topic_dict.get('featured_datasets', [])

    # Get datasets
    datasets = []
    ids = normalize_list(value)
    for id in ids:
        try:
            dataset = toolkit.get_action('package_show')(context, {'id': id})
        except toolkit.ObjectNotFound:
            continue
        datasets.append(dataset)
        if len(datasets) == limit:
            break

    return datasets


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


def get_topics(current_url='', only_featured=False):
    topics = []
    dicts = toolkit.get_action('group_list')({'model': model},
        {'all_fields': True, 'type': 'topic', 'include_extras': True})
    for topic in dicts:
        if only_featured and topic.get('featured') != 'yes':
            continue
        if topic['name'] in urlparse.parse_qs(urlparse.urlparse(current_url).query).get('groups', []):
            topic['selected'] = True
        topic['icon_path'] = get_image_for_group(topic['name'], return_path=True)
        # Change "Health + Wellbeing" to "Health"
        if topic['name'] == 'health':
            topic['title'] = 'Health'
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
            try:
                coords = ', '.join([
                    get_rounded_value(geojson['coordinates'][0][0][0]),
                    get_rounded_value(geojson['coordinates'][0][0][1]),
                    get_rounded_value(geojson['coordinates'][0][2][0]),
                    get_rounded_value(geojson['coordinates'][0][2][1]),
                ])
            except TypeError:
                pass
    if coords and text:
        return '{} ({})'.format(text, coords)
    elif text:
        return text
    elif coords:
        return coords
    return '-'


def get_temporal_value(pkg_dict):

    text = pkg_dict.get('temporal_text')
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
    ids = normalize_list(value)
    for id in ids:
        story = toolkit.get_action('package_show')(context, {'id': id})
        stories.append(story)

    return stories


def get_homepage_counts():
    datasets_count = stories_count = publishers_count = None
    q = toolkit.get_action('package_search')({}, {
        'q': '*:*',
        'facet': True,
        'facet.field': ['type_label'],
        'rows': 0,
    })
    if q.get('facets', {}).get('type_label', {}).get('Data'):
        datasets_count = q['facets']['type_label']['Data']

    if q.get('facets', {}).get('type_label', {}).get('Story'):
        stories_count = q['facets']['type_label']['Story']

    q = toolkit.get_action('organization_list')({}, {
        'type': 'publisher',
    })
    publishers_count = len(q)

    return {
        'datasets': datasets_count,
        'stories': stories_count,
        'publishers': publishers_count,
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


def get_minimum_views_for_trending():
    return int(config.get('ckanext.lacounts.trending_min') or '10') or 10


def get_frequency_period(package):
    MAPPING = {
        'daily': 'day',
        'weekly': 'week',
        'biweekly': 'two weeks',
        'monthly': 'month',
        'annually': 'year',
    }
    return MAPPING.get(package.get('frequency'))


def get_publisher_types():
    context = {'model': model}
    default = {'value': 'uncategorized', 'label': 'Uncategorized'}

    # Count publishers for types
    counter = {}
    names = toolkit.get_action('organization_list')(context, {'type': 'publisher'})
    for name in names:
        publisher = toolkit.get_action('organization_show')(context, {'id': name})
        publisher_type = publisher.get('publisher_type') or default['value']
        counter.setdefault(publisher_type, 0)
        counter[publisher_type] += 1

    # Compose type list
    types = []
    schema = toolkit.h.scheming_get_organization_schema('publisher')
    for field in schema['fields']:
        if field['field_name'] == 'publisher_type':
            for choice in toolkit.h.scheming_field_choices(field) + [default]:
                types.append({
                    'value': choice['value'],
                    'label': choice['label'],
                    'count': counter.get(choice['value'], 0),
                })

    return types


def expand_topic_package_count(topic):
    package_count = topic.get('package_count') or 0
    story_count = toolkit.get_action('package_search')({'modle': model}, {
        'fq': 'dataset_type:showcase groups:%s' % topic['name'],
    })['count'] if package_count else 0
    return {
        'package': package_count,
        'dataset': package_count - story_count,
        'story': story_count,
    }


def get_author_initials(pkg):
    initials = 'LA'
    name = None
    if pkg.get('author_profile_dict'):
        name = pkg['author_profile_dict'].get('author')
    if not name:
        name = pkg.get('author')

    if name:
        name = name.split(' ')
        if len(name) > 1:
            initials = name[0][:1] + name[1][:1]
        else:
            initials = name[0][1]
    return initials.upper()


def get_gravatar_image_url(pkg):
    email = None
    if pkg.get('author_profile_dict'):
        email = pkg['author_profile_dict'].get('author_email')
    if not email:
        email = pkg.get('author_email')
    if not email:
        return

    base_url = 'https://www.gravatar.com/avatar/{hash}?s=512i&d=mp'

    m = hashlib.md5()
    m.update(email.lower().strip())
    email_hash = m.hexdigest()

    return base_url.format(hash=email_hash)


def list_to_newlines(value):
    return '\n'.join(value)


def get_bubble_rows():
    return json.dumps(toolkit.get_action('publishers_list')({'model': model}, {}))


def normalize_list(value):
    # It takes into account that ''.split(',') == ['']
    if not value:
        return []
    if isinstance(value, list):
        return value
    return value.strip('{}').split(',')


def get_query_param(name, default=None):
    return toolkit.request.params.get(name, default)


def format_iso_date_string(string, format):
    try:
        return datetime.date(*map(int, string.split('-'))).strftime(format)
    except Exception as exception:
        log.exception(exception)
        return string


def get_groups_with_extras():
    return toolkit.get_action('group_list')(
        {'model': model}, {'type': 'topic', 'all_fields': True, 'include_extras': True})
