from __future__ import unicode_literals

import json

from ckanext.dcat.harvesters import DCATRDFHarvester
from ckanext.dcat.profiles import EuropeanDCATAPProfile
from ckanext.lacounts.helpers import toolkit
from ckanext.lacounts.harvest import helpers

import logging
log = logging.getLogger(__name__)


class LacountsESRIGeoportalHarvester(DCATRDFHarvester):
    '''
    A CKAN Harvester for ESRI Geoportals.
    '''

    def modify_package_dict(self, package_dict, dcat_dict, harvest_object):
        '''
        Subclasses can override this method to perform additional processing on
        package dicts during import_stage.
        '''
        package = helpers.process_package(package_dict, harvest_object)
        return package_dict

    def info(self):
        return {
            'name': 'esri_geoportal',
            'title': 'ESRI Geoportal',
            'description': 'Harvest from an ESRI Geoportal'
        }

    def validate_config(self, source_config):
        '''
        Source format should always be application/ld+json.
        '''
        conf = \
            super(LacountsESRIGeoportalHarvester, self) \
            .validate_config(source_config)
        if not conf:
            conf = {}
        else:
            conf = json.loads(conf)
        conf['rdf_format'] = "application/ld+json"
        return json.dumps(conf)


class LacountsESRIGeoportalProfile(EuropeanDCATAPProfile):
    '''
    An RDF profile for the Lacounts ESRI Geoportal harvester.
    '''

    def parse_dataset(self, dataset_dict, dataset_ref):

        def _remove_pkg_dict_extra(pkg_dict, key):
            '''Remove the dataset extra with the provided key, and return its
            value.
            '''
            extras = pkg_dict['extras'] if 'extras' in pkg_dict else []
            for extra in extras:
                if extra['key'] == key:
                    val = extra['value']
                    pkg_dict['extras'] = \
                        [e for e in extras if not e['key'] == key]
                    return val
            return None

        dataset_dict = super(LacountsESRIGeoportalProfile, self) \
            .parse_dataset(dataset_dict, dataset_ref)

        schema = toolkit.h.scheming_get_dataset_schema('dataset')
        field_names = [i['field_name'] for i in schema['dataset_fields']]
        # If a field name is an extra in dataset_dict, promote to the top level
        for name in field_names:
            val = _remove_pkg_dict_extra(dataset_dict, name)
            if val:
                dataset_dict[name] = val

        return dataset_dict
