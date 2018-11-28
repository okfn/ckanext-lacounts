import logging
from operator import itemgetter
log = logging.getLogger(__name__)


def _get_coordinates(package):
    coordinates = package.pop('spatial_text', None)
    if not coordinates:
        new_extras = []
        for extra in package.get('extras', []):
            if extra['key'] == 'spatial_text':
                coordinates = extra['value']
            else:
                new_extras.append(extra)

    if coordinates:
        coordinates = coordinates.split(',')
        if len(coordinates) != 4:
            return

    package['extras'] = new_extras
    return coordinates


def esri_geoportal_processor(package, harvest_object):

    # Url
    for extra in package.get('extras', []):
        if extra['key'] == 'identifier':
            package['harvest_dataset_url'] = extra['value']

    # Spatial
    coordinates = _get_coordinates(package)
    try:
        min_x, min_y, max_x, max_y = map(float, coordinates)
        package['spatial'] = {
            'type': 'Polygon',
            'coordinates': [
                [
                    [min_x, min_y],
                    [min_x, max_y],
                    [max_x, max_y],
                    [max_x, min_y],
                    [min_x, min_y],
                ]
            ],
        }
    except ValueError as e:
        log.error('Could not parse coordinates {}: {}'.format(coordinates, e))
        pass

    # Terms
    terms = []
    terms.extend(map(itemgetter('name'), package.get('tags', [])))
    package['harvest_dataset_terms'] = terms

    return package
