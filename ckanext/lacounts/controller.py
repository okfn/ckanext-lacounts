import logging
from ckan import model
from ckan.plugins import toolkit
from ckanext.showcase.controller import ShowcaseController
log = logging.getLogger(__name__)
_ = toolkit._


class BlogController(ShowcaseController):

    def search(self):
        posts = []
        context = {'model': model}
        showcases = toolkit.get_action('ckanext_showcase_list')(context, {})
        for showcase in showcases:
            for extra in showcase.get('extras', []):
                if extra['key'] == 'story_type' and extra['value'] == 'Blog post':
                    posts.append(showcase)
        return toolkit.render(self._search_template('blog'), extra_vars={'posts': posts})

    def _search_template(self, package_type):
        return 'blog/search.html'

    def _read_template(self, package_type):
        return 'blog/read.html'
