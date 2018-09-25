import logging
from dateutil.parser import parse
from ckanext.lacounts.harvest import helpers
log = logging.getLogger(__name__)


def base_processor(package, harvest_object):
    package.setdefault('extras', [])

    # Pre-map
    package['harvest_source_id'] = harvest_object.job.source.id
    package['harvest_source_url'] = harvest_object.job.source.url.strip('/')
    package['harvest_source_title'] = harvest_object.job.source.title

    # Map
    package = helpers.map_package(package, {
        # Dataset
        'harvest_dataset_created': ['metadata_created', 'source_created_at'],
        'harvest_dataset_modified': ['metadata_modified', 'source_updated_at'],
    })

    # Post-map
    for field in ['harvest_dataset_created', 'harvest_dataset_modified']:
        value = package.get(field)
        if value:
            try:
                package[field] = parse(value).isoformat()
            except Exception:
                package[field] = None

    return package
