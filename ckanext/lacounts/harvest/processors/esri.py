import logging
from ckanext.lacounts.harvest import helpers
log = logging.getLogger(__name__)


def esri_geoportal_processor(package, harvest_object):

    # Pre-map
    package['harvest_dataset_url'] = package.get('identifier')

    # Map
    # ...

    # Post-map
    coordinates = package.pop('spatial_text', '').split(',')
    if len(coordinates) == 4:
        min_x, min_y, max_x, max_y = coordinates
        package['spatial'] = {
            'type': 'Polygon',
            'coordinates': [
                [min_x, min_y],
                [min_x, max_y],
                [max_x, max_y],
                [max_x, min_y],
                [min_x, min_y],
            ],
        }

    return package
