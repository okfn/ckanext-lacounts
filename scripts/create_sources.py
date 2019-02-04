# -*- coding: utf-8 -*-
import sys
import csv
import json
import argparse

import ckanapi
from slugify import slugify


INPUT_CSV = 'harvest_sources.csv'


def create_harvest_sources(url, api_key, create_jobs=False):

    ckan = ckanapi.RemoteCKAN(url, api_key)

    with open(INPUT_CSV, 'rb') as csv_file:
        reader = csv.DictReader(csv_file)
        # Skip headers
        next(reader, None)

        for row in reader:

            # Check if publisher exists and create it otherwise
            pub_name = slugify(unicode(row['publisher'], 'utf-8'))
            try:
                org = ckan.action.organization_show(id=pub_name)
            except ckanapi.errors.NotFound:
                if 'City of' in row['publisher']:
                    display_title = row['publisher'].replace('City of ', '') + ', City of'
                else:
                    display_title = row['publisher']

                org = ckan.action.organization_create(
                    name=pub_name,
                    type='publisher',
                    title=row['publisher'],
                    display_title=display_title,
                    publisher_type=row['publisher_type'],
                )
                print('Created publisher "{}"'.format(pub_name))

            # Check if harvest source exists and create it otherwise
            source_title = (row['source_name'] or
                            row['publisher'] + ' Data Portal')
            source_name = slugify(unicode(source_title, 'utf-8'))

            try:
                source = ckan.action.harvest_source_show(id=source_name)
            except ckanapi.errors.NotFound:
                if row['config']:
                    config = json.loads(row['config'])
                else:
                    config = {}

                if row['type'] == 'esri_geoportal' and not row['url'].endswith('data.json'):
                    row['url'] = row['url'].rstrip('/') + '/data.json'
                if row['type'] == 'esri_geoportal':
                    config.update({'rdf_format': 'application/ld+json'})

                config=json.dumps(config)

                source = ckan.action.harvest_source_create(
                    name=source_name,
                    title=source_title,
                    url=row['url'],
                    source_type=row['type'],
                    owner_org=org['id'],
                    config=config,
                )
                print('Created harvest source "{}", using config "{}"'.format(
                    source_name, config))

                # Create and start a job
                if create_jobs:
                    job = ckan.action.harvest_job_create(source_id=source['id'])
                    print('Created harvest job "{}"'.format(job['id']))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Create publishers and harvest source objects from the CSV')
    parser.add_argument('url', help='CKAN site to update')
    parser.add_argument('api_key', help='Sysadmin API key on that site')
    parser.add_argument('--jobs', action='store_true',
        help='Also create new jobs for the new sources straight-away (default: false)')

    args = parser.parse_args()
    create_harvest_sources(args.url, args.api_key, args.jobs)
