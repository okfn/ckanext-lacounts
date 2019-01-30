import logging
from urlparse import urljoin
from operator import itemgetter
from ckanext.lacounts.harvest import helpers
log = logging.getLogger(__name__)


def ckan_processor(package, existing_package, harvest_object):

    # Url
    package['harvest_dataset_url'] = '{harvest_source_url}/dataset/{id}'.format(**package)

    # Metadata
    package = helpers.map_package(package, {
        # Contact
        'contact_name': ['contact_name'],
        'contact_email': ['contact_email'],
        # Temporal
        'temporal_text': ['temporal_coverage'],
        'temporal_start': [],
        'temporal_end': [],
        # Spatial
        'spatial_text': ['geo_coverage', 'spatial_coverage'],
        'spatial': [],
        # Frequency
        'frequency': ['accrual_periodicity', 'frequency'],
        # Provenance
        'provenance': ['author', 'program'],
    })

    # Terms
    terms = []
    terms.extend(map(itemgetter('name'), package.get('tags', [])))
    terms.extend(map(itemgetter('name'), package.get('groups', [])))
    package['harvest_dataset_terms'] = terms

    return package
