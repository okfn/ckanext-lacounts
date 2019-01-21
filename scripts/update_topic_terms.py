# -*- coding: utf-8 -*-
import sys
import csv

import ckanapi


INPUT_CSV = 'topic_terms.csv'

from pprint import pprint

def get_terms():

    terms = {}
    with open(INPUT_CSV, 'rb') as csv_file:
        reader = csv.DictReader(csv_file)
        # Skip headers
        next(reader, None)

        for row in reader:
            if not row.get('term'):
                continue

            if row.get('group1'):
                if not row['group1'] in terms:
                    terms[row['group1']] = []

                terms[row['group1']].append(row['term'].strip().lower())

            if row.get('group2'):
                if not row['group2'] in terms:
                    terms[row['group2']] = []

                terms[row['group2']].append(row['term'].strip().lower())

    return terms


def update_topic_terms(url, api_key):

    ckan = ckanapi.RemoteCKAN(url, api_key)

    terms = get_terms()

    for topic in terms:
        if not terms[topic]:
            continue

        try:
            topic_dict = ckan.action.group_show(id=topic)
        except ckanapi.errors.NotFound:
            continue

        existing = topic_dict.get('harvest_terms')

        if not existing:
            combined = sorted(terms[topic])
        else:
            combined = sorted(list(set(terms[topic] + existing)))

        topic_dict['harvest_terms'] = combined

        try:
            ckan.action.group_update(**topic_dict)
            print('Update topic "{}" with terms {}'.format(topic, combined))
        except ckanapi.ValidationError as error:
            print('Error: %s' % error)


if __name__ == '__main__':

    if len(sys.argv) == 1:
        pprint(get_terms())
        sys.exit(0)

    url = sys.argv[1]
    api_key = sys.argv[2]

    update_topic_terms(url, api_key)
