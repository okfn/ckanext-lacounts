import logging
import ckan.lib.helpers as h
import ckan.lib.uploader as uploader
import ckan.logic.action.update as update_core
log = logging.getLogger(__name__)


def config_option_update(context, data_dict):
    # https://github.com/ckan/ckan/blob/master/ckan/logic/action/update.py#L1198

    # Handle featured image
    if 'ckanext.lacounts.featured_image' in data_dict:
        upload = uploader.get_uploader('admin')
        upload.update_data_dict(data_dict,
            'ckanext.lacounts.featured_image',
            'featured_image_upload', 'clear_featured_image_upload')
        upload.upload(uploader.get_max_image_size())
        value = data_dict['ckanext.lacounts.featured_image']
        if value and not value.startswith('http') and not value.startswith('/'):
            image_path = 'uploads/admin/'
            value = h.url_for_static('{0}{1}'.format(image_path, value))
        data_dict['ckanext.lacounts.featured_image'] = value

    return update_core.config_option_update(context, data_dict)
