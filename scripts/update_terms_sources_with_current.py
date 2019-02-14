import sys
import csv
import shutil
from tempfile import NamedTemporaryFile

tmp_file_name = 'tmp_topic_terms.csv'
tmp_file = NamedTemporaryFile(delete=False)


def include_topics(from_csv, to_csv):

    from_terms = {}
    with open(from_csv, 'r') as f_from:
        from_reader = csv.DictReader(f_from, fieldnames=['term', 'count', 'group1', 'group2'])
        from_reader.next()
        for row in from_reader:
            from_terms[row['term']] = []
            if row.get('group1'):
                from_terms[row['term']].append(row['group1'])
            if row.get('group2'):
                from_terms[row['term']].append(row['group2'])

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
        for row in to_reader:
            if row.get('term') in from_terms:
                if len(from_terms[row['term']]) == 2:
                    row['topic2'] = from_terms[row['term']][1]
                elif len(from_terms[row['term']]) == 1:
                    row['topic1'] = from_terms[row['term']][0]
            to_writer.writerow(row)

    shutil.move(tmp_file.name, to_csv)


if __name__ == '__main__':

    from_csv = sys.argv[1]
    to_csv = sys.argv[2]

    include_topics(from_csv, to_csv)
