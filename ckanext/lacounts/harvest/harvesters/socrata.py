import json

from ckanext.socrata.plugin import SocrataHarvester
from ckanext.lacounts.harvest import helpers


class LacountsSocrataHarvester(SocrataHarvester):

    def import_stage(self, harvest_object):
        try:
            package = json.loads(harvest_object.content)
        except TypeError:
            # harvest_object may not have content. For example, if set for
            # deletion.
            pass
        else:
            package = helpers.process_package(package, harvest_object)
            harvest_object.content = json.dumps(package)
        return super(LacountsSocrataHarvester, self) \
            .import_stage(harvest_object)

    def process_package(self, package, harvest_object):
        package = helpers.process_package(package, harvest_object)
        return package
