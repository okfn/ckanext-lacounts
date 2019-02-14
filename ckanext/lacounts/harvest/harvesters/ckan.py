import json
import urllib
import logging

from ckanext.harvest.harvesters import CKANHarvester
from ckanext.harvest.harvesters.ckanharvester import (
    ContentFetchError, SearchError)
from ckanext.lacounts.helpers import toolkit
from ckanext.lacounts.harvest import helpers
log = logging.getLogger(__name__)


class LacountsCKANHarvester(CKANHarvester):

    def validate_config(self, config):
        config = super(LacountsCKANHarvester, self).validate_config(config)

        config_obj = json.loads(config)

        if ('query_params' in config_obj and
                not isinstance(config_obj['query_params'], dict)):
            raise ValueError('query_params must be an object')

        return config

    def _search_for_datasets(self, remote_ckan_base_url, fq_terms=None):
        '''
        This is the same as the base implementation but adding support for
        extra query params, eg to support filtering by search terms or bbox
        '''
        base_search_url = remote_ckan_base_url + self._get_search_api_offset()
        params = {'rows': '100', 'start': '0'}
        params['sort'] = 'id asc'
        if fq_terms:
            params['fq'] = ' '.join(fq_terms)

        # Custom code starts
        if self.config.get('query_params'):
            params.update(self.config['query_params'])
        # Custom code ends

        pkg_dicts = []
        pkg_ids = set()
        previous_content = None
        while True:
            url = base_search_url + '?' + urllib.urlencode(params)
            log.debug('Searching for CKAN datasets: %s', url)
            try:
                content = self._get_content(url)
            except ContentFetchError, e:
                raise SearchError(
                    'Error sending request to search remote '
                    'CKAN instance %s using URL %r. Error: %s' %
                    (remote_ckan_base_url, url, e))

            if previous_content and content == previous_content:
                raise SearchError('The paging doesn\'t seem to work. URL: %s' %
                                  url)
            try:
                response_dict = json.loads(content)
            except ValueError:
                raise SearchError('Response from remote CKAN was not JSON: %r'
                                  % content)
            try:
                pkg_dicts_page = response_dict.get('result', {}).get('results',
                                                                     [])
            except ValueError:
                raise SearchError('Response JSON did not contain '
                                  'result/results: %r' % response_dict)

            # Weed out any datasets found on previous pages (should datasets be
            # changing while we page)
            ids_in_page = set(p['id'] for p in pkg_dicts_page)
            duplicate_ids = ids_in_page & pkg_ids
            if duplicate_ids:
                pkg_dicts_page = [p for p in pkg_dicts_page
                                  if p['id'] not in duplicate_ids]
            pkg_ids |= ids_in_page

            pkg_dicts.extend(pkg_dicts_page)

            if len(pkg_dicts_page) == 0:
                break

            params['start'] = str(int(params['start']) + int(params['rows']))

        return pkg_dicts

    def import_stage(self, harvest_object):

        # Update config
        if harvest_object.job.source.config:
            config = json.loads(harvest_object.job.source.config)
        else:
            config = {}
        # Set `remote_groups` to be able set groups in processors
        config['remote_groups'] = 'only_local'
        harvest_object.job.source.config = json.dumps(config)

        # Update package
        package = json.loads(harvest_object.content)
        try:
            existing_package = self._find_existing_package(package)
        except toolkit.ObjectNotFound:
            existing_package = None
        package = helpers.process_package(package, existing_package, harvest_object)
        harvest_object.content = json.dumps(package)

        return super(LacountsCKANHarvester, self).import_stage(harvest_object)
