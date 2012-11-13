from django import template
from videoembed import embed, match_wrapper
import re

register = template.Library()

"""
kwargs tokenizer taken from Django 1.4 source
"""
kwarg_re = re.compile(r"(?:(\w+)=)?(.+)")

def token_kwargs(bits, parser):
    if not bits:
        return {}

    match = kwarg_re.match(bits[0])
    kwarg_format = match and match.group(1)

    if not kwarg_format:
        return {}

    kwargs = {}
    while bits:
        match = kwarg_re.match(bits[0])
        if not match or not match.group(1):
            return kwargs
        key, value = match.groups()
        del bits[:1]
    return kwargs


class EmbedMovieNode(template.Node):
    def __init__(self, videometa, options):
        self.options = dict([(key, template.Variable(opt)) for key,opt in options.items()])
        self.videometa = template.Variable(videometa)

    def render(self, context):
        options = []
        for key, value in self.options.items():
            options.append((key, value.resolve(context)))
        videometa = self.videometa.resolve(context)

        if isinstance(videometa, basestring):
            return embed(videometa, **dict(options)) # BC
        else:
            return videometa.embed(options=options)
        

@register.tag
def embed_movie(parser, token):
    bits = token.split_contents()
    videometa = bits[1]
    kwargs_bits = bits[2:]

    options = {}
    for bit in kwargs_bits:
        match = kwarg_re.match(bit)
        if match:
            key,val=match.groups()
            options[key]=val
    return EmbedMovieNode(videometa, options)


class GetMovieNode(template.Node):
    def __init__(self, url, variable_name):
        self.url = template.Variable(url)
        self.variable_name = variable_name

    def render(self, context):
        url = self.url.resolve(context)
        cast_as = self.variable_name
        wrapper = match_wrapper(url)
        if wrapper:
            context[cast_as] = wrapper.clean_url(url)
        return ''

@register.tag
def get_movie(parser, token):
    bits = token.split_contents()
    if len(bits)<2 or len(bits)>4 or not bits[2] == 'as':
        raise template.TemplateSyntaxError('Usage: %s <url> as <variable_name>' % bits[0])

    url = bits[1]
    variable_name = bits[3]

    return GetMovieNode(url, variable_name)
