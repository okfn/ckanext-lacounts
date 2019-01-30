import logging
from dateutil.parser import parse
from ckanext.lacounts.harvest import helpers
log = logging.getLogger(__name__)


def before_processor(package, existing_package, harvest_object):
    package.setdefault('extras', [])

    # Source/timestamp
    package['harvest_source_id'] = harvest_object.job.source.id
    package['harvest_source_url'] = harvest_object.job.source.url.strip('/')
    package['harvest_source_title'] = harvest_object.job.source.title
    package['harvest_timestamp'] = harvest_object.fetch_started.isoformat()

    # Metadata
    package = helpers.map_package(package, {
        # Dataset
        'issued': ['metadata_created', 'source_created_at', 'issued'],
        'modified': ['metadata_modified', 'source_updated_at', 'modified'],
    })

    # Issued/modified
    for field in ['issued', 'modified']:
        value = package.get(field)
        if value:
            try:
                package[field] = parse(value).isoformat()
            except Exception:
                package[field] = None

    # Manually managed fields
    names = ['related_datasets', 'groups_override']
    if existing_package:
        for name in names:
            if name in existing_package:
                package[name] = existing_package[name]

    return package
