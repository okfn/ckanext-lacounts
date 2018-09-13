from functools import partial
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from routes.mapper import SubMapper

from ckanext.lacounts import helpers


class LacountsPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes, inherit=True)

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
            'get_metadata_completion_rate': helpers.get_metadata_completion_rate,
        }

    # IRoutes

    def before_map(self, map):
        # These named routes are used for custom dataset forms which will use
        # the names below based on the dataset.type ('dataset' is the default
        # type)
        with SubMapper(map, controller='ckanext.lacounts.controller:BlogController') as m:
            m.connect('blog_search', '/blog', action='search')
            m.connect('blog_read', '/blog/{id}', action='read')
        return map
