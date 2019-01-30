from ckanext.socrata.plugin import SocrataHarvester
from ckanext.lacounts.harvest import helpers


class LacountsSocrataHarvester(SocrataHarvester):

    def process_package(self, package, harvest_object):
        existing_package = self._get_existing_dataset(harvest_object.guid)
        package = helpers.process_package(package, existing_package, harvest_object)
        return package
