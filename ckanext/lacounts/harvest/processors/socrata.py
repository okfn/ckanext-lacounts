import logging
from ckanext.lacounts.harvest import helpers
log = logging.getLogger(__name__)


def socrata_processor(package, harvest_object):

    # Pre-map
    package['harvest_dataset_url'] = package.get('url')

    # Map
    package = helpers.map_package(package, {
        # Contact
        'contact_name': ['owner_display_name'],
    })

    # Post-map
    package['frequency'] = helpers.normalize_frequency(package.get('frequency'))

    return package
