import json
import logging
import inflect
from ckan import model
from textblob import TextBlob
from ckan.plugins import toolkit
from ckanext.lacounts import helpers
log = logging.getLogger(__name__)


# Dataset tagging is based on two factors:
# - dataset and topic's terms (auto tagging)
# - dataset's groups_override field (manual tagging)


# Module API

def recalculate_dataset_groups(package, groups=None):
    # package: we look for package['harvest_dataset_terms']
    # groups: groups with extras (if not passed will be queried)

    # Get groups if None
    if groups is None:
        groups = helpers.get_groups_with_extras()

    # Auto-tagging
    package['groups'] = []
    dataset_terms = _pluralize(normalize_terms(package.get('harvest_dataset_terms', [])))
    if dataset_terms:
        for group in groups:
            group_terms = _pluralize(normalize_terms(group.get('harvest_terms', [])))
            if set(dataset_terms).intersection(group_terms):
                package['groups'].append(group)

    # Manual-tagging
    groups_override = json.loads(package.get('groups_override') or '{"add": [], "del" : []}')
    for group in groups:
        if group['id'] in groups_override['add'] and group not in package['groups']:
            package['groups'].append(group)
    for group in list(package['groups']):
        if group['id'] in groups_override['del']:
            package['groups'].remove(group)

    return package


def extract_terms_from_text(text):
    blob = TextBlob(text)
    exclude = ['[', ']']
    tags = normalize_terms([
        t[0] for t in blob.tags
        if t[1].startswith('NN') and not t[0][0] in exclude])
    noun_phrases = [
        np for np in normalize_terms(blob.noun_phrases)
        if np not in tags and not np[0] in exclude]
    return tags + noun_phrases


def normalize_terms(terms):
    return map(_normalize_term, terms)


# Internal

def _pluralize(terms):
    p = inflect.engine()
    plurals = []
    for term in terms:
        plurals.append(p.plural(term))
    return terms + plurals


def _normalize_term(term):
    return term.strip().lower()
