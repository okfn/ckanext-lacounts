import os
import json
import logging
from urlparse import urlparse
from ckanext.lacounts.helpers import toolkit, model
log = logging.getLogger(__name__)


def process_package(package, harvest_object):
    from ckanext.lacounts.harvest import processors
    package = processors.before_processor(package, harvest_object)
    processor = getattr(processors, '%s_processor' % harvest_object.source.type)
    if processor:
        package = processor(package, harvest_object)
    package = processors.after_processor(package, harvest_object)
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


def update_groups(package, groups):
    # package: we look for package['harvest_dataset_terms']
    # groups: you can pass groups with extras to improve performance otherwise we query db
    package['groups'] = []
    dataset_terms = normalize_terms(package.get('harvest_dataset_terms', ''))
    if dataset_terms:
        for group in groups:
            group_terms = normalize_terms(group.get('harvest_terms', ''))
            if set(dataset_terms).intersection(group_terms):
                package['groups'].append(group)
    return package


def list_groups_with_extras():
    return toolkit.get_action('group_list')(
        {'model': model}, {'type': 'topic', 'all_fields': True, 'include_extras': True})


def normalize_frequency(value):
    options = ['never', 'daily', 'weekly', 'biweekly', 'monthly', 'annually', 'irregular']
    if value:
        value = value.lower()
        if value not in options:
            value = 'unknown'
    return value or None


def normalize_terms(value):
    return map(normalize_term, value)


def normalize_term(term):
    return term.strip().lower()
