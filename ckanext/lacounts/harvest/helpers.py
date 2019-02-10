import json
import logging
import inflect
from ckanext.lacounts.helpers import toolkit, model
log = logging.getLogger(__name__)


def process_package(package, existing_package, harvest_object):
    from ckanext.lacounts.harvest import processors
    package = processors.before_processor(package, existing_package, harvest_object)
    processor = getattr(processors, '%s_processor' % harvest_object.source.type)
    if processor:
        package = processor(package, existing_package, harvest_object)
    package = processors.after_processor(package, existing_package, harvest_object)
    return package


def map_package(package, mapping):
    # mapping: in form of `{'lacounts_field_name: ['key_1', 'key_2', ...], ...}`
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


def normalize_frequency(value):
    options = ['never', 'daily', 'weekly', 'biweekly', 'monthly', 'annually', 'irregular']
    if value:
        value = value.lower()
        if value not in options:
            value = 'unknown'
    return value or None
