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
        source = harvest_object.job.source
    except Exception as exception:
        log.exception(exception)
        error = True

    # Process
    if not error:

        # Load
        try:
            name = re.sub(r'[^a-zA-Z0-9_]', '_', urlparse(source.url).netloc)
            module = import_module('ckanext.lacounts.harvest.processors.%s' % name)
            process = getattr(module, '%s_processor' % name)
        except ImportError as exception:
            log.exception(exception)
            process = None

        # Process
        package = before_process(package, source)
        if process:
            package = process(package, source)

    # Compose
    harvest_object.content = json.dumps(package)

    return harvest_object


def before_process(package, source):
    """This hook is used to update package for all harvesting sources.
    """

    # General
    package['harvest_source_id'] = source.id
    package['harvest_source_url'] = source.url.strip('/')
    package['harvest_source_title'] = source.title

    # Heuristics
    # TODO: put here code that could work for all sources

    # Extras
    package.setdefault('extras', [])

    return package
