import json
import logging
from ckanext.harvest.harvesters import CKANHarvester
from ckanext.lacounts.harvest import helpers
log = logging.getLogger(__name__)


class LacountsCKANHarvester(CKANHarvester):

    def import_stage(self, harvest_object):
        log.debug('In LacountsCKANHarvester import_stage')
        package = json.loads(harvest_object.content)
        package = helpers.process_package(package, harvest_object)
        harvest_object.content = json.dumps(package)
        return super(LacountsCKANHarvester, self).import_stage(harvest_object)
