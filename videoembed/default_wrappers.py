import re
from django.template.loader import render_to_string
from django.conf import settings
from registry import wrappers



class YoutubeWrapper(object):
    re_urls = (
        re.compile(r'http://(www.)?youtube.com/watch\?v=(?P<id>[^&]+).*$'),
        re.compile(r'http://(www.)?youtu.be/(?P<id>.+)'),
    )

    def match_url(self, url):
        return bool(self.clean_url(url))

    def clean_url(self, url):
        for pattern in self.re_urls:
            match = pattern.match(url)
            if match:
                return 'http://www.youtube.com/embed/%(id)s' % match.groupdict()
        return None

    def render(self, url, opts=None):
        ctx = {}
        ctx.update(opts or {})
        ctx.update({
            'url': self.clean_url(url),
            'MEDIA_URL': settings.MEDIA_URL,
            })

        return render_to_string('videoembed/embed_youtube.html', ctx)


class FlowplayerWrapper(object):
    def match_url(self, url):
        return url.endswith('.flv')

    def render(self, url, opts=None):
        ctx = {}
        ctx.update(opts or {})
        ctx.update({
            'url': url,
            'MEDIA_URL': settings.MEDIA_URL,
            })

        return render_to_string('videoembed/embed_flowplayer.html', ctx)




def register_default_wrappers():
    wrappers.register(YoutubeWrapper)
    wrappers.register(FlowplayerWrapper)


