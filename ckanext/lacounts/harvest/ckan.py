import json
import logging
from ckanext.harvest.harvesters import CKANHarvester
log = logging.getLogger(__name__)


class LacountsCKANHarvester(CKANHarvester):

    def import_stage(self, harvest_object):
        log.debug('In LacountsCKANHarvester import_stage')

        # Decompose
        error = False
        try:
            package = json.loads(harvest_object.content)
            config = json.loads(harvest_job.source.config)
            source_id=harvest_object.job.source.id
            source_url=harvest_object.job.source.url.strip('/')
            source_title=harvest_object.job.source.title
            job_id=harvest_object.job.id
            object_id=harvest_object.id
            # TODO:
            # dataset_url
            # last_modified
        except Exception:
            error = True

        # Transform
        if not error:
            pass

        return super(LacountsCKANHarvester, self).import_stage(harvest_object)
