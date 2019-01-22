import os
import csv
import urllib
import collections
import StringIO


from ckan.plugins import toolkit
from ckan import model


BASE_URL = toolkit.config.get('ckan.site_url', 'http://localhost:5000').rstrip('/')


def _link(url, text):
    return '=HYPERLINK("{}", "{}")'.format(url, text)


def _search_url(params):
    qs = []
    for key in params.keys():
        qs.append('{}:"{}"'.format(key, params[key]))

    qs = ' AND '.join(qs)

    return '{}/dataset?{}'.format(BASE_URL, urllib.urlencode({'q': qs}))


def create_topics_csv():

    res = model.Session.execute(
        'SELECT * FROM topic_terms_sources ORDER BY count DESC')

    headers = ['term', 'count', 'topic1', 'topic2', 'topic3']
    for i in range(1, 7):
        headers.append('source{}'.format(i))
        headers.append('source{}_count'.format(i))


    terms = collections.OrderedDict()
    for record in res:
        if not record['term'] in terms:
            terms[record['term']] = {
                'term': record['term'],
                'count': record['count'],
                'source1': _link(record['source_url'], record['source_title']),
                'source1_count': _link(
                    _search_url(
                        {'tags': record['term'],
                         'harvest_source_title': record['source_title']}),
                    record['count']
                )
            }
        else:
            # Duplicate, add new source and update global count
            for i in range(2, 7):
                if 'source{}'.format(i) in terms[record['term']]:
                    continue
                else:
                    terms[record['term']].update({
                        'count': terms[record['term']]['count'] + record['count'],
                        'source{}'.format(i): _link(
                            record['source_url'], record['source_title']),
                        'source{}_count'.format(i): _link(
                            _search_url(
                                {'tags': record['term'],
                                 'harvest_source_title': record['source_title']}),
                            record['count']
                        )
                    })
                    break

    rows = []
    for term, row in terms.iteritems():
        # Add link to global count
        row['count'] = _link(_search_url({'tags': row['term']}), row['count'])
        rows.append(row)

    f = StringIO.StringIO()
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

    return f.getvalue()
