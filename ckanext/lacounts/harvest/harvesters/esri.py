from __future__ import unicode_literals

import json

from rdflib.namespace import Namespace

from ckanext.dcat.harvesters import DCATRDFHarvester
from ckanext.dcat.profiles import EuropeanDCATAPProfile
from ckanext.lacounts.harvest import helpers

import logging
log = logging.getLogger(__name__)


VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class LacountsESRIGeoportalHarvester(DCATRDFHarvester):
    '''
    A CKAN Harvester for ESRI Geoportals.
    '''

    def modify_package_dict(self, package_dict, dcat_dict, harvest_object):
        helpers.process_package(package_dict, harvest_object)
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

        dataset_dict = super(LacountsESRIGeoportalProfile, self).parse_dataset(
            dataset_dict, dataset_ref)

        # See project-open-data/project-open-data.github.io#621
        for agent in self.g.objects(dataset_ref, DCAT.contactPoint):
            email = self._without_mailto(
                self._object_value(agent, VCARD.email)
            )
            if email:
                dataset_dict['contact_email'] = email

        return dataset_dict
