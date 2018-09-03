import logging
from ckanext.harvest.harvesters import CKANHarvester
from ckanext.lacounts.harvest import helpers
log = logging.getLogger(__name__)


#TODO: switch to ESRIHarvester
class LacountsESRIHarvester(CKANHarvester):

    def process_package(self, package, harvest_object):
        log.debug('In LacountsESRIHarvester process_package')
        package = helpers.process_package(package, harvest_object)
        return package
