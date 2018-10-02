import logging
from ckanext.lacounts.harvest import helpers
log = logging.getLogger(__name__)


def after_processor(package, harvest_object):

    # Frequency
    package['frequency'] = helpers.normalize_frequency(package.get('frequency'))

    # Terms
    package['harvest_dataset_terms'] = "\n".join(map(
        helpers.normalize_term, package.get('harvest_dataset_terms', [])))

    # Groups
    package = helpers.update_groups(package, groups=helpers.list_groups_with_extras())

    return package
