import sys
import csv
import shutil
from tempfile import NamedTemporaryFile

tmp_file_name = 'tmp_topic_terms.csv'
tmp_file = NamedTemporaryFile(delete=False)

field_names = [
    'term',
    'count',
    'topic1',
    'topic2',
    'topic3',
    'source1',
    'source1_count',
    'source2',
    'source2_count',
    'source3',
    'source3_count',
    'source4',
    'source4_count',
    'source5',
    'source5_count',
    'source6',
    'source6_count',
]


def include_topics(from_csv, to_csv):

    from_terms = {}
    with open(from_csv, 'r') as f_from:
        from_reader = csv.DictReader(f_from, fieldnames=field_names)
        from_reader.next()
        for row in from_reader:
            from_terms[row['term']] = []
            for topic_field in ('group1', 'group2', 'topic1', 'topic2', 'topic3'):
                if row.get(topic_field):
                    from_terms[row['term']].append(row[topic_field])

    from_terms.pop('', None)

    with open(to_csv, 'r') as f_to:
        headers = ['term', 'count', 'topic1', 'topic2', 'topic3']
        for i in range(1, 7):
            headers.append('source{}'.format(i))
            headers.append('source{}_count'.format(i))

        to_reader = csv.DictReader(f_to, fieldnames=headers)

        to_writer = csv.DictWriter(tmp_file, fieldnames=headers)
        to_writer.writeheader()

        to_reader.next()
        dest_fields = ['topic1', 'topic2', 'topic3']
        for row in to_reader:
            if row.get('term') in from_terms:
                for index, topic in enumerate(from_terms[row['term']]):
                    row[dest_fields[index]] = topic
            to_writer.writerow(row)

    shutil.move(tmp_file.name, to_csv)


if __name__ == '__main__':

    from_csv = sys.argv[1]
    to_csv = sys.argv[2]

    include_topics(from_csv, to_csv)
