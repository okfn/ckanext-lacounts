# -*- coding: utf-8 -*-

from ckan.common import OrderedDict
from ckan.plugins import toolkit
import ckanapi


groups = OrderedDict([
    ('education', 'Education'),
    ('environment', 'Environment'),
    ('well-being', 'Well Being'),
    ('housing', 'Housing'),
    ('immigration', 'Immigration'),
    ('transportation', 'Transportation')
])


class CreateFeaturedTopics(toolkit.CkanCommand):
    '''Create featured topics

    Usage:
      create_featured_topics             - create featured topics
    '''

    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 0
    min_args = 0

    def command(self):
        self._load_config()

        local_ckan = ckanapi.LocalCKAN()

        for name, title in groups.items():
            try:
                local_ckan.action.group_create(
                    name=name,
                    title=title,
                    type='topic'
                )
                print('Created group %s ' % name)
            except ckanapi.ValidationError as e:
                if 'Group name already exists in database' \
                   in e.error_dict['name']:
                    print('Group %s already exists' % name)
