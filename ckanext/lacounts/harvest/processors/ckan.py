from urlparse import urljoin
from ckanext.lacounts.harvest import helpers


def ckan_processor(package, harvest_object):
    source_domain = helpers.extract_source_domain(harvest_object)

    # all sources
    package['harvest_dataset_url'] = '{harvest_source_url}/dataset/{id}'.format(**package)

    # data.chhs.ca.gov
    if source_domain == 'data.chhs.ca.gov':
        # TODO: implement, remove example
        package['extras'].append({'key': 'CHHS', 'value': True, 'state': 'active'})

    # data.cnra.ca.gov
    if source_domain == 'data.cnra.ca.gov':
        # TODO: implement
        pass

    return package
