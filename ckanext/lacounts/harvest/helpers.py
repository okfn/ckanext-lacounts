import os
import json
import logging
from urlparse import urlparse
log = logging.getLogger(__name__)


def process_package(package, harvest_object):
    from ckanext.lacounts.harvest import processors
    package = processors.base_processor(package, harvest_object)
    processor = getattr(processors, '%s_processor' % harvest_object.source.type)
    if processor:
        package = processor(package, harvest_object)
    return package


def map_package(package, mapping):
    # Mapping in form of `{'lacounts_field_name: ['key_1', 'key_2', ...], ...}`
    for field_name, keys in mapping.items():
        for key in keys:
            # General
            value = package.get(key)
            if value is not None:
                package[field_name] = value
            # Extras
            for extra in package.get('extras', []):
                if extra.get('key') != key:
                    continue
                value = extra.get('value')
                if value is None:
                    continue
                package[field_name] = value
    return package


def extract_source_domain(harvest_object):
    return urlparse(harvest_object.job.source.url).netloc


def normalize_frequency(value):
    options = ['never', 'daily', 'weekly', 'biweekly', 'monthly', 'annually', 'irregular']
    if value:
        value = value.lower()
        if value not in options:
            value = 'unknown'
    return value or None
