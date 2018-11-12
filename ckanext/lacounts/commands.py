# -*- coding: utf-8 -*-

from ckan.common import OrderedDict
from ckan.plugins import toolkit
import ckanapi


topics = [
    # name, title, featured
    ('administrative-boundaries', 'Administrative Boundaries', False),
    ('arts-culture', 'Arts + Culture', False),
    ('census', 'Census', False),
    ('community-economic-development', 'Community + Economic Development', False),
    ('demographics', 'Demographics', False),
    ('education', 'Education', True),
    ('environment', 'Environment', True),
    ('equity', 'Equity', False),
    ('food', 'Food', False),
    ('government-services', 'Government Services', False),
    ('government-spending', 'Government Spending', False),
    ('health', 'Health + Wellbeing', True),
    ('housing', 'Housing', True),
    ('immigration', 'Immigration', True),
    ('infrastructure', 'Infrastructure', False),
    ('la-counts', 'LA Counts', False),
    ('natural-disasters', 'Natural Disasters', False),
    ('philanthropy', 'Philanthropy', False),
    ('recreation', 'Recreation', False),
    ('safety', 'Safety', False),
    ('schools', 'Schools', False),
    ('transportation', 'Transportation', True),
    ('water', 'Water', False),
]


class CreateTopics(toolkit.CkanCommand):
    '''Create featured topics

    Usage:
      create_topics             - create topics
    '''

    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 0
    min_args = 0

    def command(self):
        self._load_config()

        local_ckan = ckanapi.LocalCKAN()

        for name, title, featured in topics:
            featured = 'yes' if featured else 'no'

            # Check
            try:
                local_ckan.action.group_show(id=name)
                print('Existed topic "%s"' % name)
                continue
            except ckanapi.errors.NotFound:
                pass

            # Create
            try:
                local_ckan.action.group_create(
                    name=name, title=title, type='topic', featured=featured)
                print('Created topic "%s"' % name)
            except ckanapi.ValidationError as error:
                print('Error: %s' % error)
