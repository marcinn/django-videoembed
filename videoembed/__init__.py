from registry import wrappers


def match_wrapper(url):
    """
    Return video embedding wrapper instance for specified url.
    """
    for wrapper in wrappers.get_all():
        if wrapper.match_url(url):
            return wrapper
    return None


def embed(url, **options):
    """
    Generate embed HTML code for specified video URL.
    Options are passed to renderer as template context.

    Arguments:
        `url`   - url of the movie
        `options`  - optional parameters dictionary
    """
    wrapper = match_wrapper(url)
    if wrapper:
        return wrapper.render(wrapper.clean_url(url), options)
    return ''

