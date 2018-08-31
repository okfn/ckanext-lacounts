import re
import json
import logging
from urlparse import urlparse
from importlib import import_module
log = logging.getLogger(__name__)


def before_import(harvest_object):
    """This hook is used to update harvest object for all harvesters.
    """

    # Decompose
    error = False
    try:
        package = json.loads(harvest_object.content)
    except Exception as exception:
        log.exception(exception)
        error = True

    # Process
    if not error:

        # Load
        try:
            loc = urlparse(harvest_object.job.source.url).netloc
            name = re.sub(r'[^a-zA-Z0-9_]', '_', loc)
            module = import_module('ckanext.lacounts.harvest.processors.%s' % name)
            process = getattr(module, '%s_processor' % name)
        except ImportError:
            process = None

        # Process
        package = before_process(package, harvest_object)
        if process:
            package = process(package, harvest_object)

    # Compose
    harvest_object.content = json.dumps(package)

    return harvest_object


def before_process(package, harvest_object):
    """This hook is used to update package for all harvesting sources.
    """

    # General
    package['harvest_source_id'] = harvest_object.job.source.id
    package['harvest_source_url'] = harvest_object.job.source.url.strip('/')
    package['harvest_source_title'] = harvest_object.job.source.title
    package['harvest_timestamp'] = harvest_object.fetch_started.isoformat()

    # Dataset
    package['harvest_dataset_url'] = ''
    if harvest_object.source.type == 'ckan':
        package['harvest_dataset_url'] = '{0}/dataset/{1}'.format(
            package['harvest_source_url'], package['id'])

    # Heuristics
    # TODO: put here code that could work for all sources

    # Extras
    package.setdefault('extras', [])

    return package
