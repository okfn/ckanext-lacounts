import json
import logging
from ckan import model
from ckan.common import config
from ckan.plugins import toolkit
import ckan.lib.uploader as uploader
import ckanext.lacounts.helpers as helpers
import ckanext.lacounts.harvest.helpers as harvest_helpers
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
        if '\n' in value:
            # Legacy format
            return value.split('\n')
        try:
            return json.loads(value)
        except ValueError:
            # Return as single item
            return [value]


def convert_groups_override(key, data, errors, context):
    value = data.get(('groups_override',)) or []

    # Skip if already JSON
    if '"add"' in value and '"del"' in value:
        return

    # Get group ids
    package = None
    group_ids = set()
    group_override_ids = set(helpers.normalize_list(value))
    if data.get(('id',)) and data[('id', )] is not toolkit.missing:
        context = {'model': model}
        try:
            package = toolkit.get_action('package_show')(context, {'id': data[('id',)]})
            group_ids = set(map(lambda group: group['id'], package['groups']))
        except toolkit.ObjectNotFound:
            pass

    # Form groups_override value
    groups_add = group_override_ids.difference(group_ids)
    groups_del = group_ids.difference(group_override_ids)
    groups_override = json.loads((package or {}).get('groups_override') or '{"add": [], "del" : []}')
    groups_override = {
        'add': list(set(groups_override['add']).union(groups_add).difference(groups_del)),
        'del': list(set(groups_override['del']).union(groups_del).difference(groups_add)),
    }

    # Form groups value
    groups = package['groups'] if package else []
    for group in harvest_helpers.list_groups_with_extras():
        if group['id'] in groups_override['add'] and group not in groups:
            groups.append(group)
    for group in list(groups):
        if group['id'] in groups_override['del']:
            groups.remove(group)

    # Save groups_override/groups
    # We generate data values like this:
    # data[('groups', 0, 'id)] = group-id
    # data[('groups', 1, 'id)] = None
    # data[('groups', 2, 'id)] = None
    # to ensure that groups, we want to delete, are removed
    # We use it because we don't get any input groups information in this function
    # so we can't modify it
    # len(groups) == count of desired groups
    # len(groups_is) == count of existent groups
    data[('groups_override',)] = json.dumps(groups_override)
    for index in range(max(len(groups), len(group_ids))):
        group_id = groups[index]['id'] if index < len(groups) else None
        data[('groups', index, 'id')] = group_id
