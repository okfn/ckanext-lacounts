import sys

import ckanapi


topics = [
    # name, title, featured
    ('administrative-boundaries', 'Administrative Boundaries', False),
    ('arts-culture', 'Arts + Culture', False),
    ('census', 'Census', False),
    ('community-economic-development', 'Community + Economic Development',
        False),
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


def create_topics(url, api_key):

    ckan = ckanapi.RemoteCKAN(url, api_key)

    for name, title, featured in topics:
        featured = 'yes' if featured else 'no'

        # Check
        try:
            ckan.action.group_show(id=name)
            print('Existed topic "%s"' % name)
            continue
        except ckanapi.errors.NotFound:
            pass

        # Create
        try:
            ckan.action.group_create(
                name=name, title=title, type='topic', featured=featured)
            print('Created topic "%s"' % name)
        except ckanapi.ValidationError as error:
            print('Error: %s' % error)

if __name__ == '__main__':

    url = sys.argv[1]
    api_key = sys.argv[2]

    create_topics(url, api_key)
