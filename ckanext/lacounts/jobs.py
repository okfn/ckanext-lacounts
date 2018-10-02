import ast
import time
import logging
from ckan import model
import ckan.plugins.toolkit as toolkit
from ckanext.lacounts.harvest import helpers
log = logging.getLogger(__name__)


def update_groups(group_name):
    # This job re-calculate all harvested dataset groups from scratch
    # It makes actual update call only on changed packages
    time.sleep(3)

    # Get groups
    groups = helpers.list_groups_with_extras()

    # Get extras
    extras = (model.Session
        .query(model.PackageExtra)
        .filter(model.PackageExtra.key == 'harvest_dataset_terms')
        .filter(model.PackageExtra.value != '[]')
        .all())

    # Get packages
    offset = 0
    limit = 1000
    packages = []
    while True:
        page = toolkit.get_action('package_search')(
            {'model': model}, {'start': offset, 'rows': limit})['results']
        if not page:
            break
        packages.extend(page)
        offset += limit

    # Update packages
    for package in packages:
        old_group_names = _extract_group_names(package)
        package = helpers.update_groups(package, groups=groups)
        new_group_names = _extract_group_names(package)
        if old_group_names != new_group_names:
            package = toolkit.get_action('package_update')({'model': model}, package)
            log.debug('Updated package: %s' % package['name'])


def _extract_group_names(package):
    group_names = set()
    for group in package.get('groups', []):
        group_names.add(group['name'])
    return group_names
