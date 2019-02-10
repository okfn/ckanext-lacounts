import time
import logging
from ckan import model
import ckan.plugins.toolkit as toolkit
import ckan.logic.action.update as update_core
from ckanext.lacounts import helpers, tagging
log = logging.getLogger(__name__)


# Module API

def update_groups_for_all_datasets():
    # This job re-calculate all harvested dataset groups from scratch
    # It makes actual update call only on changed packages
    time.sleep(3)

    # Get groups
    groups = helpers.get_groups_with_extras()

    # Get packages
    offset = 0
    limit = 1000
    packages = []
    while True:
        page = toolkit.get_action('package_search')(
            {'model': model}, {
                'start': offset,
                'rows': limit,
                'fq': 'dataset_type:dataset',
                })['results']
        if not page:
            break
        packages.extend(page)
        offset += limit

    # Update packages
    for package in packages:
        old_group_names = _extract_group_names(package)
        package = tagging.recalculate_dataset_groups(package, groups=groups)
        new_group_names = _extract_group_names(package)
        if old_group_names != new_group_names:
            # We don't want to recalculate groups twice
            # (see ckanext.lacounts.logic.actions.package_create/udpate)
            context = {'model': model, 'user': toolkit.c.user}
            package = update_core.package_update(context, package)
            log.debug('Updated groups for package: %s' % package['name'])


# Internal

def _extract_group_names(package):
    group_names = set()
    for group in package.get('groups', []):
        group_names.add(group['name'])
    return group_names
