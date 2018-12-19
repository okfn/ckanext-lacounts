import json
import logging
from ckan.common import config
from ckan.plugins import toolkit
import ckan.lib.uploader as uploader
log = logging.getLogger(__name__)


def validate_editable_regions(value):
    # value: the client send us only changed regions as a dict

    # Parse/update/stringify
    try:
        regions = json.loads(value or '{}')
        is_patch = regions.pop('is_patch', False)
        if is_patch:
            old_value = config.get('ckanext.lacounts.editable_regions')
            old_regions = json.loads(old_value or '{}')
            regions = dict(old_regions.items() + regions.items())
        value = json.dumps(regions, indent=4)
    except Exception:
        raise toolkit.Invalid('Homepage regions can\'t be parsed/updated/stringified')

    # Validate
    for region_name, region in regions.items():
        # We check if region is set it should contain tags
        if '<' not in region or '>' not in region:
            raise toolkit.Invalid('Homepage region %s is invalid' % region_name)

    return value


def set_default_publisher_title(key, data, errors, context):
    data[('title',)] = data.get(('title',)) or data.get(('display_title',))


def convert_to_list(value, context):
    if not value:
        return None

    if isinstance(value, list):
        value = [v.strip().lower() for v in value]
    else:
        value = [v.strip().lower() for v in value.split('\n')]

    return json.dumps(value)


def convert_from_list(value, context):

    if not value:
        return []
    else:
        return json.loads(value)
