# -*- coding: utf-8 -*-
import sys
import urllib
import json
from urlparse import urlparse

import requests
import ckanapi


def _get_expected_datasets(source):

    expected = None
    try:
        if source['source_type'] == 'ckan':
            params = source.get('config', {}).get('query_params')
            url = '{}/api/action/package_search?rows=0'.format(source['url'])
            if params:
                url = url + '&' + urllib.urlencode(params)
            result = requests.get(url).json()
            expected = result['result']['count']
        elif source['source_type'] == 'socrata':
            search_context = urlparse(source['url']).hostname
            if source.get('config', {}).get('domains'):
                domain = ','.join(source['config']['domains'])
            else:
                domain = search_context

            url = 'http://api.us.socrata.com/api/catalog/v1?domains={}&search_context={}&only=datasets'.format(domain, search_context)
            q = source.get('config', {}).get('q')
            if q:
                url = url + '&q={}&min_should_match=1'.format(' '.join(q))
            result = requests.get(url).json()
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
        if source.get('config'):
            source['config'] = json.loads(source['config'])
        else:
            source['config'] = {}

        print('{}, {}, {}, {}'.format(
            source['name'],
            source['status']['total_datasets'],
            _get_expected_datasets(source),
            source['config']
            )
        )

if __name__ == '__main__':

    url = sys.argv[1]

    check_harvest_sources(url)
