def data_chhs_ca_gov_processor(package, harvest_object):
    """Source: https://data.chhs.ca.gov/
    """

    # Extras
    # TODO: remove example
    package['extras'].append({'key': 'CHHS', 'value': True, 'state': 'active'})

    return package
