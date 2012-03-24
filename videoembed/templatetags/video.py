from django import template
from videoembed import embed
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
    def __init__(self, url, opts):
        self.opts = dict([(key, template.Variable(opt)) for key,opt in opts.items()])
        self.url = template.Variable(url)

    def render(self, context):
        opts = []
        for key, value in self.opts.items():
            opts.append((key, value.resolve(context)))
        return embed(self.url.resolve(context), **dict(opts))
        

@register.tag
def embed_movie(parser, token):
    bits = token.split_contents()
    url = bits[1]
    kwargs_bits = bits[2:]

    opts = {}
    for bit in kwargs_bits:
        match = kwarg_re.match(bit)
        if match:
            key,val=match.groups()
            opts[key]=val
    return EmbedMovieNode(url, opts)


