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


def extract_source_domain(harvest_object):
    return urlparse(harvest_object.job.source.url).netloc
