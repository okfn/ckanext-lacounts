import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation

from ckanext.lacounts import actions
from ckanext.lacounts import helpers


class LacountsPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'lacounts')

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'get_image_for_group': helpers.get_image_for_group,
            'get_related_datasets_for_form': helpers.get_related_datasets_for_form,
            'get_related_datasets_for_display': helpers.get_related_datasets_for_display,
        }
