import logging
from functools import partial
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from routes.mapper import SubMapper

from ckanext.lacounts import helpers, validators, jobs, actions

log = logging.getLogger(__name__)
_ = toolkit._


class LacountsPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IGroupController, inherit=True)
    plugins.implements(plugins.IActions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'lacounts')

    def update_config_schema(self, schema):
        schema.update({
            'ckanext.lacounts.editable_regions': [
                toolkit.get_validator('ignore_missing'),
                validators.validate_editable_regions,
            ],
            'ckanext.lacounts.featured_image': [
                toolkit.get_validator('ignore_missing'),
            ],
        })

        return schema

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'get_image_for_group': helpers.get_image_for_group,
            'get_related_datasets_for_form': helpers.get_related_datasets_for_form,
            'get_related_datasets_for_display': helpers.get_related_datasets_for_display,
            'get_metadata_completion_rate': helpers.get_metadata_completion_rate,
            'get_recent_data_stories': helpers.get_recent_data_stories,
            'get_featured_image_url': helpers.get_featured_image_url,
            'get_editable_region': helpers.get_editable_region,
            'get_package_stories': helpers.get_package_stories,
            'get_topics': helpers.get_topics,
            'update_url_query': helpers.update_url_query,
            'get_spatial_value': helpers.get_spatial_value,
            'get_temporal_value': helpers.get_temporal_value,
            'get_story_related_stories': helpers.get_story_related_stories,
            'get_dataset_and_stories_counts': helpers.get_dataset_and_stories_counts,
            'sort_facet_items': helpers.sort_facet_items,
            'get_publisher_type': helpers.get_publisher_type,
            'get_organization_display_title': helpers.get_organization_display_title,
        }

    # IRoutes

    def before_map(self, map):
        # These named routes are used for custom dataset forms which will use
        # the names below based on the dataset.type ('dataset' is the default
        # type)
        with SubMapper(map, controller='ckanext.lacounts.controller:BlogController') as m:
            m.connect('blog_search', '/blog', action='search')
            m.connect('blog_read', '/blog/{id}', action='read')

        with SubMapper(map, controller='ckanext.lacounts.controller:StaticController') as m:
            m.connect('privacypolicy', '/privacy', action='privacypolicy')
            m.connect('termsofservice', '/terms', action='termsofservice')
            m.connect('faqs', '/faqs', action='faqs')
            m.connect('about', '/about', action='about')
            m.connect('resources', '/resources', action='resources')
            m.connect('getinvolved', '/getinvolved', action='getinvolved')

        map.redirect('/why-la-counts', '/about', _redirect_code='301 Moved Permanently')
        return map

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        facets_dict.clear()
        facets_dict['type_label'] = _('Type')
        facets_dict['story_type'] = _('Story Type')
        facets_dict['groups'] = _('Topic')
        facets_dict['organization'] = _('Publisher')
        facets_dict['res_format'] = _('Format')

        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        facets_dict.clear()
        facets_dict['type_label'] = _('Type')
        facets_dict['organization'] = _('Publisher')
        facets_dict['res_format'] = _('Format')

        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        facets_dict.clear()
        facets_dict['type_label'] = _('Type')
        facets_dict['groups'] = _('Topic')
        facets_dict['res_format'] = _('Format')

        return facets_dict

    # IPackageController

    def before_index(self, pkg_dict):
        TYPE_LABELS = {'dataset': _('Data'), 'showcase': _('Story')}
        if pkg_dict['type'] in TYPE_LABELS:
            pkg_dict['type_label'] = TYPE_LABELS[pkg_dict['type']]
        return pkg_dict

    # IGroupController

    def create(self, entity):
        if getattr(entity, 'type') == 'topic' and not getattr(toolkit.c, 'job'):
            toolkit.enqueue_job(jobs.update_groups, [entity.name])

    def edit(self, entity):
        if getattr(entity, 'type') == 'topic' and not getattr(toolkit.c, 'job'):
            toolkit.enqueue_job(jobs.update_groups, [entity.name])

    # IActions

    def get_actions(self):
        return {
            'config_option_update': actions.config_option_update,
        }
