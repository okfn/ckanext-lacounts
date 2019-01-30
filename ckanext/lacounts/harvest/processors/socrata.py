import logging
from operator import itemgetter
from ckanext.lacounts.harvest import helpers
log = logging.getLogger(__name__)


def socrata_processor(package, existing_package, harvest_object):

    # Url
    package['harvest_dataset_url'] = package.get('url')

    # Metadata
    package = helpers.map_package(package, {
        # Contact
        'contact_name': ['owner_display_name'],
    })

    # Terms
    terms = []
    terms.extend(map(itemgetter('name'), package.get('tags', [])))
    for item in package.get('extras', []):
        if item.get('key') == 'categories':
            terms.extend(item.get('value', []))
    package['harvest_dataset_terms'] = terms

    return package
