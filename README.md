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

### Create featured topics

There are pre-defined _topics_ (groups) that can be created with a paster command.

#### In development

`docker-compose -f docker-compose.dev.yml run --rm ckan-dev bash -c "cd src_extensions/ckanext-lacounts && python setup.py develop && paster create_featured_topics"`

#### In production & staging
