import logging
import ckan.logic.action.create as create_core
import ckan.logic.action.update as update_core
log = logging.getLogger(__name__)


def package_create(context, data_dict):
    log.debug(data_dict)
    return create_core.package_create(context, data_dict)


def package_update(context, data_dict):
    log.debug(data_dict)
    return update_core.package_update(context, data_dict)
