import ckan.plugins.toolkit as toolkit


def get_image_for_group(group_name):
    '''
    Render an inline svg snippet for the named group (topic). These groups
    correlate with those created by the `create_featured_topics` command.
    '''
    jinja_env = toolkit.config['pylons.app_globals'].jinja_env
    groups = {
        'education': 'icons/book.svg',
        'environment': 'icons/leaf.svg',
        'health': 'icons/heart.svg',
        'housing': 'icons/keys.svg',
        'immigration': 'icons/passport.svg',
        'transportation': 'icons/bus.svg'
    }
    svg = jinja_env.get_template(groups[group_name])
    img = toolkit.literal("<span class='image %s'>" % group_name
                          + svg.render() + "</span>")
    return img
