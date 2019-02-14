import json
from textblob import TextBlob

out = {}
with open('titles.txt', 'r') as f:
    for title in f.readlines():
        title = title.decode('utf8').strip()
        blob = TextBlob(title)

        out[title] = {
            'tags': [t[0] for t in blob.tags if t[1].startswith('NN')],
            'noun_phrases':  blob.noun_phrases
        }

print json.dumps(out)
