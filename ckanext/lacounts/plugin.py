import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation


class LacountsPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)

    @staticmethod
    def get_image_for_group(group_name):
        '''
        Render an inline svg snippet for the named group (topic). These groups
        correlate with those created by the `create_featured_topics` command.
        '''
        jinja_env = toolkit.config['pylons.app_globals'].jinja_env
        groups = {
            'education': 'icons/book.svg',
            'environment': 'icons/leaf.svg',
            'health': 'icons/heart.svg',
            'housing': 'icons/keys.svg',
            'immigration': 'icons/passport.svg',
            'transportation': 'icons/bus.svg'
        }
        svg = jinja_env.get_template(groups[group_name])
        img = toolkit.literal("<span class='image %s'>" % group_name
                              + svg.render() + "</span>")
        return img

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'lacounts')

    # ITemplateHelpers
    def get_helpers(self):
        return {'get_image_for_group': self.get_image_for_group}
