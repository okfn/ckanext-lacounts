import json
import logging
from ckan import model
from ckan.common import config
from ckan.plugins import toolkit
log = logging.getLogger(__name__)


def get_image_for_group(group_name):
    '''
    Render an inline svg snippet for the named group (topic). These groups
    correlate with those created by the `create_featured_topics` command.
    '''
    jinja_env = toolkit.config['pylons.app_globals'].jinja_env
    groups = {
        'education': 'icons/book.svg',
        'environment': 'icons/leaf.svg',
        'well-being': 'icons/heart.svg',
        'housing': 'icons/keys.svg',
        'immigration': 'icons/passport.svg',
        'transportation': 'icons/bus.svg'
    }
    # Fetch svg template if there is one, otherwise return empty string.
    try:
        svg = jinja_env.get_template(groups[group_name])
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
        dataset = toolkit.get_action('package_show')(context, {'id': id})
        href = toolkit.url_for('dataset_read', id=dataset['name'], qualified=False)
        datasets.append({'text': dataset['title'], 'href': href})

    return datasets


def get_metadata_completion_rate(package):
    GROUPS = [
        'owner_org',
        'notes',
        'metadata_modified',
        ['contact_name', 'contact_email'],
        'identifier',
        'access_rights',
        'license_title',
        ['spatial_text', 'spatial'],
        ['temporal_text', 'temporal_start', 'temporal_end'],
        # 'distribution' - we don't have this field
        # 'distribution_fields' - we don't have this field
        'frequency',
        'language',
        'url',
    ]

    # Calculate
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
    rate = int(100 * (count/float(len(GROUPS))))

    return rate


def get_editable_region(name):
    try:
        regions = json.loads(config.get('ckanext.lacounts.editable_regions', ''))
        return regions[name]
    except Exception:
        return ''
