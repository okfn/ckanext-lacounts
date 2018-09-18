import json
import logging
from ckan.plugins import toolkit
log = logging.getLogger(__name__)


def validate_editable_regions(value):
    valid = True

    # Parse
    try:
        regions = json.loads(value)
    except Exception:
        valid = False

    # Check
    if valid:
        names = ['hero']
        for name in names:
            region = regions.get(name, '')
            # We check that region is set and has tags inside
            if '<' not in region or '>' not in region:
                valid = False
                break

    # Raise
    if not valid:
        raise toolkit.Invalid('Homepage regions config is not valid')

    return value
