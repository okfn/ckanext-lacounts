import os
import json

import sqlalchemy

from ckanext.lacounts.harvest import helpers


def add_title_terms():

    engine = sqlalchemy.create_engine(os.environ.get('CKAN_SQLALCHEMY_URL', 'postgresql://ckan:ckan@db/ckan'))
    connection = engine.connect()
    res = connection.execute('SELECT * FROM tmp_title_terms')
    for row in res:
        try:
            current_terms = json.loads(row['value'])
        except ValueError:
            continue

        title_terms = [t for t in helpers.get_terms_from_text(row['title']) if t not in current_terms]

        if title_terms:
            new_terms = json.dumps(current_terms + title_terms)
            statement = sqlalchemy.text("UPDATE package_extra SET value = :value WHERE package_id = :id AND key = 'harvest_dataset_terms'")
            res = engine.execute(statement, value=new_terms, id=row['package_id'])

            statement = sqlalchemy.text("UPDATE package_extra_revision SET value = :value WHERE package_id = :id AND key = 'harvest_dataset_terms'")
            res = engine.execute(statement, value=new_terms, id=row['package_id'])


            print('Updated package {}, new terms: {}'.format(row['package_id'], title_terms))


if __name__ == '__main__':

    add_title_terms()
