import logging
from ckanext.harvest.harvesters import CKANHarvester
from ckanext.lacounts.harvest.hooks import before_import
log = logging.getLogger(__name__)


class LacountsCKANHarvester(CKANHarvester):

    def import_stage(self, harvest_object):
        log.debug('In LacountsCKANHarvester import_stage')
        harvest_object = before_import(harvest_object)
        return super(LacountsCKANHarvester, self).import_stage(harvest_object)
