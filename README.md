# ckanext-lacounts

CKAN extension for the LA Counts project

## Requirements

This extension is being developed against CKAN 2.8.x

## Installation

To install ckanext-lacounts for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/okfn/ckanext-lacounts.git
    cd ckanext-lacounts
    python setup.py develop
    pip install -r requirements.txt


## API (*Get Involved* page actions)

Actions for the *Get Involved* page are available in the CKAN Action API.

**Event** actions:

Available parameters:

- `id`: a uuid (required for some actions, see below)
- `name`: a string (required)
- `date`: a date string e.g. "2019-01-21" (required)
- `free`: a boolean-like, e.g. "yes" or true (required)
- `url`: a string url
- `location`: a string
- `topic_tags`: a list of strings, e.g. ["Housing", "Employment"]

A full example for `event_create`:

```sh
$ curl -X POST http://127.0.0.1:5000/api/3/action/event_create -H "Authorization:{YOUR-API-KEY}" -d '{"name": "My New Event", "free": "yes", "date": "2019-01-21", "url": "http://example.com/event-details", "location": "Downton, Los Angeles", "topic_tags": ["Housing", "Employment"]}'
```

All Event actions:

```sh
# create a new event (sysadmins only)
curl -X POST http://127.0.0.1:5000/api/3/action/event_create -H "Authorization:{YOUR-API-KEY}" -d '{"name": "My New Event", "free": "yes", "date": "2019-01-21"}'

# update an existing event (sysadmins only)
curl -X POST http://127.0.0.1:5000/api/3/action/event_update -H "Authorization:{YOUR-API-KEY}" -d '{"id": "my-event-id", "name": "My Updated Event", "free": "no", "date": "2020-01-21"}'

# delete an event (sysadmins only)
curl -X POST http://127.0.0.1:5000/api/3/action/event_delete -H "Authorization:{YOUR-API-KEY}" -d '{"id": "my-event-id"}'

# show an event
curl http://127.0.0.1:5000/api/3/action/event_show -d '{"id": "my-event-id"}'

# list events ``limit`` and ``offset`` are optional.
curl http://127.0.0.1:5000/api/3/action/event_list -H "Authorization:{YOUR-API-KEY}" -d '{"limit":<int>, "offset":<int>}'
```


## Running the Tests

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.lacounts --cover-inclusive --cover-erase --cover-tests

## Theme development

Get dependencies with `npm install`.

CSS and JS are built from the `src` directory into the `fanstatic` directory.

CSS is built with PostCSS. Do so with `grunt postcss`.

JS is built (minified) with `grunt uglify`.

You can watch both for changes with `grunt`.

## Create initial data

There are scripts defined in the `scripts` folder that create initial objects:
* topics (groups)
* harvest sources + publishers (organizations)

To run them you'll need a sysadmin API key and the URL of the site to update (dev, staging or production). For instance:

    python create_topics.py http://localhost:5000 API-KEY

    python create_source.py https://lacounts-staging.l3.ckan.io/ API-KEY

Note: Some of them require extra libraries (eg slugify)


## Initialize 'Get Involved' database tables

The 'Get Involved' pages require additional database tables to be initialized: `events` and `volunteering`. These are created with the following paster command:

### In development

```sh
docker-compose -f docker-compose.dev.yml run --rm ckan-dev bash -c "cd src_extensions/ckanext-lacounts && python setup.py develop && paster get_involved init-db -c ../../production.ini"
```

### In production & staging

```sh
deis run "paster --plugin=ckanext-lacounts get_involved init-db -c production.ini"
```

## Database

Apart from the tables defined in the application, the following view is used to generate reports and can be created manually:

    CREATE VIEW topic_terms_sources
        AS SELECT t.name AS term, s.url AS source_url, s.title as source_title, COUNT(*)
        FROM tag t
            JOIN package_tag pt ON t.id = pt.tag_id
            JOIN package_extra pe ON pt.package_id = pe.package_id
            JOIN harvest_object ho ON pe.package_id = ho.package_id
            JOIN harvest_source s ON s.id = ho.harvest_source_id
        WHERE pe.key = 'harvest_source_id'
        GROUP BY s.url, s.title, t.name
        ORDER BY COUNT(*) DESC;
