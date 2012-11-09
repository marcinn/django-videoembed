import re
from django.template.loader import render_to_string
from django.conf import settings
from registry import wrappers
import urlparse


class VideoMeta(object):
    def __init__(self, wrapper, url, thumbnail_url=None):
        self._wrapper = wrapper
        self.url = url
        self.thumbnail_url = thumbnail_url

    def __unicode__(self):
        return self.url

    def __len__(self):
        return len(self.url)

    def embed(self, options=None):
        return self._wrapper.render(self, options=options)


class BaseWrapper(object):
    template_name = None

    def match_url(self, url):
        raise NotImplementedError

    def clean_url(self, url):
        if url:
            return VideoMeta(self, url)

    def get_template_name(self, videometa):
        return self.template_name

    def get_context(self, videometa):
        return {
            'url': videometa.url, # backward compatibility
            'video': videometa,
            'MEDIA_URL': settings.MEDIA_URL,
        }

    def render(self, videometa, options=None):
        ctx = {}
        ctx.update(options or {})
        ctx.update(self.get_context(videometa))
        template_name = self.get_template_name(videometa)
        return render_to_string(template_name, ctx)


class YoutubeWrapper(BaseWrapper):
    re_urls = (
        re.compile(r'https?://(www.)?youtube.com/watch\?v=(?P<id>[^&]+).*$'),
        re.compile(r'https?://(www.)?youtu.be/(?P<id>.+)'),
    )
    template_name = 'videoembed/embed_youtube.html'

    def match_url(self, url):
        return any([pattern.match(url) for pattern in self.re_urls])

    def clean_url(self, url):
        for pattern in self.re_urls:
            match = pattern.match(url)
            parsed_url = urlparse.urlparse(url)
            if match:
                params = match.groupdict()
                params['scheme'] = parsed_url.scheme
                return VideoMeta(self, '%(scheme)s://www.youtube.com/embed/%(id)s' % params,
                        '%(scheme)s://img.youtube.com/vi/%(id)s/0.jpg' % params)
        return None


class FlowplayerWrapper(BaseWrapper):
    template_name = 'videoembed/embed_flowplayer.html'

    def match_url(self, url):
        return url.endswith('.flv')


def register_default_wrappers():
    wrappers.register(YoutubeWrapper)
    wrappers.register(FlowplayerWrapper)


