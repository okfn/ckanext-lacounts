# -*- coding: utf-8 -*-
import sys
import csv

import ckanapi
from slugify import slugify


INPUT_CSV = 'harvest_sources.csv'


def create_harvest_sources(url, api_key):

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
                org = ckan.action.organization_create(
                    name=pub_name,
                    type='publisher',
                    title=row['publisher'],
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
                if row['type'] == 'esri_geoportal' and not row['url'].endswith('data.json'):
                    row['url'] = row['url'].rstrip('/') + '/data.json'

                source = ckan.action.harvest_source_create(
                    name=source_name,
                    title=source_title,
                    url=row['url'],
                    source_type=row['type'],
                    owner_org=org['id'],
                )
                print('Created harvest source "{}"'.format(source_name))

            # Create and start a job
            job = ckan.action.harvest_job_create(source_id=source['id'])
            print('Created harvest job "{}"'.format(job['id']))

if __name__ == '__main__':

    url = sys.argv[1]
    api_key = sys.argv[2]

    create_harvest_sources(url, api_key)
