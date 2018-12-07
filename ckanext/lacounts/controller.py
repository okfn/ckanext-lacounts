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
            showcase = toolkit.get_action('package_show')(context, {'id': showcase['id']})
            if showcase.get('story_type') == 'Blog post':
                posts.append(showcase)
        return toolkit.render(self._search_template('blog'), extra_vars={'posts': posts})

    def _search_template(self, package_type):
        return 'blog/search.html'

    def _read_template(self, package_type):
        return 'blog/read.html'


class StaticController(toolkit.BaseController):

    def faqs(self):
        return toolkit.render('static/faqs.html')

    def aboutus(self):
        return toolkit.render('static/about.html')

    def termsofservice(self):
        return toolkit.render('static/termsofservice.html')

    def privacypolicy(self):
        return toolkit.render('static/privacypolicy.html')

    def resources(self):
        return toolkit.render('static/resources.html')


class GetInvolvedController(toolkit.BaseController):

    def index(self):
        toolkit.c.events = toolkit.get_action('event_list')(data_dict={})
        return toolkit.render('getinvolved/getinvolved.html')

    def manage_get_involved(self):
        '''
        A ckan-admin page to list and add Get Involved events.
        '''
        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user or toolkit.c.author}

        try:
            toolkit.check_access('sysadmin', context, {})
        except toolkit.NotAuthorized:
            toolkit.abort(401, _('User not authorized to view page'))

        toolkit.c.events = toolkit.get_action('event_list')(data_dict={})

        return toolkit.render('getinvolved/manage_get_involved.html')

    def remove_event(self):
        '''
        Remove an event.
        '''
        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user or toolkit.c.author}

        try:
            toolkit.check_access('sysadmin', context, {})
        except toolkit.NotAuthorized:
            toolkit.abort(401, _('User not authorized to view page'))

        if 'cancel' in toolkit.request.params:
            toolkit.redirect_to(
                controller='ckanext.lacounts.controller:GetInvolvedController',
                action='manage_get_involved')

        event_id = toolkit.request.params['id']
        if toolkit.request.method == 'POST' and event_id:
            try:
                toolkit.get_action('event_delete')(
                                   data_dict={'id': event_id})
            except toolkit.NotAuthorized:
                toolkit.abort(401, _('Unauthorized to perform that action'))
            except toolkit.ObjectNotFound:
                toolkit.h.flash_error(_('The event was not found.'))
            else:
                toolkit.h.flash_success(_('The event has been removed.'))
        elif not event_id:
            toolkit.h.flash_error(_('The event was not found.'))

        return toolkit.redirect_to(
            controller='ckanext.lacounts.controller:GetInvolvedController',
            action='manage_get_involved')
