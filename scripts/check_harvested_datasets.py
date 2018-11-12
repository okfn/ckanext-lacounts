# -*- coding: utf-8 -*-
import sys
from urlparse import urlparse

import requests
import ckanapi


def _get_expected_datasets(source):

    expected = None
    try:
        if source['source_type'] == 'ckan':
            result = requests.get(
                '{}/api/action/package_search?rows=0'.format(source['url'])).json()
            expected = result['result']['count']
        elif source['source_type'] == 'socrata':
            domain = urlparse(source['url']).netloc
            result = requests.get('http://api.us.socrata.com/api/catalog/v1?domains={}&search_context={}&only=datasets'.format(domain, domain)).json()
            expected = result['resultSetSize']
        elif source['source_type'] == 'esri_geoportal':
            result = requests.get(source['url']).json()
            expected = len(result['dataset'])

        return expected
    except Exception, e:
        print('{}'.format(e))
        return None


def check_harvest_sources(url):

    ckan = ckanapi.RemoteCKAN(url)

    sources = ckan.action.harvest_source_list()

    for item in sources:
        if not item['active']:
            continue

        source = ckan.action.harvest_source_show(id=item['id'])

        print('{},{},{}'.format(
            source['name'],
            source['status']['total_datasets'],
            _get_expected_datasets(source)
            )
        )

if __name__ == '__main__':

    url = sys.argv[1]

    check_harvest_sources(url)
