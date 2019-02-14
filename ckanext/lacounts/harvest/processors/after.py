import logging
from ckanext.lacounts import tagging
from ckanext.lacounts.harvest import helpers
log = logging.getLogger(__name__)
toolkit = helpers.toolkit


def after_processor(package, existing_package, harvest_object):

    # If a field name is an extra in dataset_dict, promote it to the top level
    schema = toolkit.h.scheming_get_dataset_schema('dataset')
    # Add some core ones not explicitly defined in our schema
    field_names = [i['field_name'] for i in schema['dataset_fields']]
    core_names = ['tags', 'groups', 'harvest_object_id']
    field_names = field_names + core_names
    for name in field_names:
        val = _remove_pkg_dict_extra(package, name)
        if val and not name in core_names:
            package[name] = val

    # Frequency
    package['frequency'] = helpers.normalize_frequency(
        package.get('frequency'))

    # Terms
    package['harvest_dataset_terms'] = tagging.normalize_terms(
            package.get('harvest_dataset_terms', []))

    # For all harvesters, extract nouns from titles as terms as well
    title_terms = tagging.extract_terms_from_text(package.get('title'))
    for term in title_terms:
        if term not in package['harvest_dataset_terms']:
            package['harvest_dataset_terms'].append(term)

    return package


def _remove_pkg_dict_extra(pkg_dict, key):
    '''Remove the dataset extra with the provided key, and return its
    value.
    '''
    extras = pkg_dict['extras'] if 'extras' in pkg_dict else []
    for extra in extras:
        if extra['key'] == key:
            val = extra['value']
            pkg_dict['extras'] = \
                [e for e in extras if not e['key'] == key]
            return val
    return None
