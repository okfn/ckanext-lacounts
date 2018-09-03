def base_processor(package, harvest_object):

    # General
    package['harvest_source_id'] = harvest_object.job.source.id
    package['harvest_source_url'] = harvest_object.job.source.url.strip('/')
    package['harvest_source_title'] = harvest_object.job.source.title
    package['harvest_timestamp'] = harvest_object.fetch_started.isoformat()

    # Extras
    package.setdefault('extras', [])

    return package
