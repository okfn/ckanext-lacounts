import logging
from ckan import model
from ckan.plugins import toolkit
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic

from ckanext.showcase.controller import ShowcaseController

from ckanext.lacounts.admin import create_topics_csv

log = logging.getLogger(__name__)
_ = toolkit._

tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params


class BlogController(ShowcaseController):

    def search(self):
        posts = []
        context = {'model': model}
        showcases = toolkit.get_action('ckanext_showcase_list')(context, {})
        for showcase in showcases:
            showcase = \
                toolkit.get_action('package_show')(context,
                                                   {'id': showcase['id']})
            if showcase.get('story_type') == 'Blog Post':
                posts.append(showcase)
        return toolkit.render(self._search_template('blog'),
                              extra_vars={'posts': posts})

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
        volunteering = \
            toolkit.get_action('volunteering_list')(data_dict={})
        toolkit.c.volunteering = [v for v in volunteering
                                  if not v['is_filled']]
        return toolkit.render('getinvolved/getinvolved.html')

    def manage_get_involved(self):
        '''
        A ckan-admin page to list and add Get Involved events and volunteering
        opportunity.
        '''
        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user or toolkit.c.author}

        try:
            toolkit.check_access('sysadmin', context, {})
        except toolkit.NotAuthorized:
            toolkit.abort(401, _('User not authorized to view page'))

        toolkit.c.events = toolkit.get_action('event_list')(data_dict={})
        toolkit.c.volunteering = \
            toolkit.get_action('volunteering_list')(data_dict={})

        return toolkit.render('getinvolved/manage_get_involved.html')

    # Events

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
            return toolkit.redirect_to(
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

    def new_event(self, data=None, errors=None, error_summary=None):

        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user}
        try:
            toolkit.check_access('sysadmin', context)
        except toolkit.NotAuthorized:
            toolkit.abort(401, _('User not authorized to create event'))

        if toolkit.request.method == 'POST' and not data:
            return self._save_event(context)

        data = data or {}
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors,
                'error_summary': error_summary}

        return toolkit.render("getinvolved/event_form.html",
                              extra_vars=vars)

    def edit_event(self, data=None, errors=None, error_summary=None):

        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user}
        data_dict = {'id': toolkit.request.params['id']}

        try:
            toolkit.check_access('sysadmin', context)
        except toolkit.NotAuthorized:
            toolkit.abort(403, _('Not authorized to edit event'))

        if toolkit.request.method == 'POST' and not data:
            return self._save_event(context, 'update')

        try:
            old_data = toolkit.get_action('event_show')(context, data_dict)
            data = data or old_data
        except (toolkit.ObjectNotFound, toolkit.NotAuthorized):
            toolkit.abort(404, _('Event not found'))

        errors = errors or {}
        vars = {'data': data, 'errors': errors, 'form_style': 'edit',
                'error_summary': error_summary, 'action': 'edit'}

        return toolkit.render("getinvolved/event_form.html",
                              extra_vars=vars)

    def _save_event(self, context, type="create"):
        try:
            data_dict = clean_dict(dict_fns.unflatten(
                tuplize_dict(parse_params(toolkit.request.params))))

            # If only one topic, it is a string, so make it a list.
            if not isinstance(data_dict.get('topic_tags', []), list):
                data_dict['topic_tags'] = [data_dict['topic_tags'], ]
            elif data_dict.get('topic_tags') is None:
                data_dict['topic_tags'] = []

            context['message'] = data_dict.get('log_message', '')

            if type == 'create':
                toolkit.get_action('event_create')(context, data_dict)
                toolkit.h.flash_success(_('The event has been created.'))
            elif type == 'update':
                toolkit.get_action('event_update')(context, data_dict)
                toolkit.h.flash_success(_('The event has been updated.'))
        except (toolkit.ObjectNotFound, toolkit.NotAuthorized) as e:
            toolkit.abort(404, _('Event not found'))
        except toolkit.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            if type == 'create':
                return self.new_event(data_dict, errors, error_summary)
            elif type == 'update':
                return self.edit_event(data_dict, errors, error_summary)

        return toolkit.redirect_to(
            controller='ckanext.lacounts.controller:GetInvolvedController',
            action='manage_get_involved')

    # Volunteering Opportunites

    def remove_volunteering(self):
        '''
        Remove an volunteering.
        '''
        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user or toolkit.c.author}

        try:
            toolkit.check_access('sysadmin', context, {})
        except toolkit.NotAuthorized:
            toolkit.abort(401, _('User not authorized to view page'))

        if 'cancel' in toolkit.request.params:
            return toolkit.redirect_to(
                controller='ckanext.lacounts.controller:GetInvolvedController',
                action='manage_get_involved')

        volunteering_id = toolkit.request.params['id']
        if toolkit.request.method == 'POST' and volunteering_id:
            try:
                toolkit.get_action('volunteering_delete')(
                                   data_dict={'id': volunteering_id})
            except toolkit.NotAuthorized:
                toolkit.abort(401, _('Unauthorized to perform that action'))
            except toolkit.ObjectNotFound:
                toolkit.h.flash_error(
                    _('The volunteering opportunity was not found.'))
            else:
                toolkit.h.flash_success(
                    _('The volunteering opportunity has been removed.'))
        elif not volunteering_id:
            toolkit.h.flash_error(
                _('The volunteering opportunity was not found.'))

        return toolkit.redirect_to(
            controller='ckanext.lacounts.controller:GetInvolvedController',
            action='manage_get_involved')

    def new_volunteering(self, data=None, errors=None, error_summary=None):

        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user}
        try:
            toolkit.check_access('sysadmin', context)
        except toolkit.NotAuthorized:
            toolkit.abort(
                401,
                _('User not authorized to create volunteering opportunity'))

        if toolkit.request.method == 'POST' and not data:
            return self._save_volunteering(context)

        data = data or {}
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors,
                'error_summary': error_summary}

        return toolkit.render("getinvolved/volunteering_form.html",
                              extra_vars=vars)

    def edit_volunteering(self, data=None, errors=None, error_summary=None):
        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user}
        data_dict = {'id': toolkit.request.params['id']}

        try:
            toolkit.check_access('sysadmin', context)
        except toolkit.NotAuthorized:
            toolkit.abort(
                403, _('Not authorized to edit volunteering opportunity'))

        if toolkit.request.method == 'POST' and not data:
            return self._save_volunteering(context, 'update')

        try:
            old_data = toolkit.get_action('volunteering_show')(context,
                                                               data_dict)
            data = data or old_data
        except (toolkit.ObjectNotFound, toolkit.NotAuthorized):
            toolkit.abort(404, _('Event not found'))

        errors = errors or {}
        vars = {'data': data, 'errors': errors, 'form_style': 'edit',
                'error_summary': error_summary, 'action': 'edit'}

        return toolkit.render("getinvolved/volunteering_form.html",
                              extra_vars=vars)

    def _save_volunteering(self, context, type="create"):
        try:
            data_dict = clean_dict(dict_fns.unflatten(
                tuplize_dict(parse_params(toolkit.request.params))))

            # If only one topic, it is a string, so make it a list.
            if not isinstance(data_dict.get('topic_tags', []), list):
                data_dict['topic_tags'] = [data_dict['topic_tags'], ]
            elif data_dict.get('topic_tags') is None:
                data_dict['topic_tags'] = []

            context['message'] = data_dict.get('log_message', '')

            if type == 'create':
                toolkit.get_action('volunteering_create')(context, data_dict)
                toolkit.h.flash_success(
                    _('The volunteering opportunity has been created.'))
            elif type == 'update':
                toolkit.get_action('volunteering_update')(context, data_dict)
                toolkit.h.flash_success(
                    _('The volunteering opportunity has been updated.'))
        except (toolkit.ObjectNotFound, toolkit.NotAuthorized) as e:
            toolkit.abort(404, _('Volunteering Opportunity not found'))
        except toolkit.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            if type == 'create':
                return self.new_volunteering(data_dict, errors, error_summary)
            elif type == 'update':
                return self.edit_volunteering(data_dict, errors, error_summary)

        return toolkit.redirect_to(
            controller='ckanext.lacounts.controller:GetInvolvedController',
            action='manage_get_involved')


class AdminController(toolkit.BaseController):

    def download_terms_sources_csv(self):

        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user or toolkit.c.author}

        try:
            toolkit.check_access('sysadmin', context, {})
        except toolkit.NotAuthorized:
            toolkit.abort(401, _('User not authorized to access this resource'))

        output_csv = create_topics_csv()

        toolkit.response.headers['Content-type'] = 'text/csv'
        toolkit.response.headers['Content-disposition'] = 'attachment;filename=topic_terms_sources.csv'

        return output_csv


class RedirectController(toolkit.BaseController):

    def redirect_url(self, url):
        return toolkit.redirect_to(url)
