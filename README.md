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

