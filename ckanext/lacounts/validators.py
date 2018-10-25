import json
import logging
import ckan.model as model
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


def convert_group_names_into_dicts(names, context):
    # TODO: fix, these groups are just ignored on package update
    groups = []
    names = names if isinstance(names, list) else names.strip('{}').split(',')
    for name in names:
        group = toolkit.get_action('group_show')(context, {'id': name})
        groups.append(group)
    return groups
