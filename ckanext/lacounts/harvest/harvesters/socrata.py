from ckanext.socrata.plugin import SocrataHarvester
from ckanext.lacounts.harvest import helpers


class LacountsSocrataHarvester(SocrataHarvester):

    def process_package(self, package, harvest_object):
        package = helpers.process_package(package, harvest_object)
        return package
