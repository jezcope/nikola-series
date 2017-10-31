from nikola.plugin_categories import SignalHandler
from nikola import utils
from nikola.utils import LOGGER

from blinker import signal
from collections import defaultdict, namedtuple

from pprint import pformat, pprint

SeriesDescription = namedtuple('SeriesDescription', 'description posts')

class Series(SignalHandler):

    name = 'series'

    conf_vars = ['SERIES']
    conf_defaults = {'SERIES': dict}

    def set_site(self, site):
        LOGGER.debug('in Series.set_site!')

        ready = signal('scanned')
        ready.connect(self.after_scan)

    def after_scan(self, site):
        LOGGER.debug('in Series.after_scan')
        series_posts = defaultdict(list)
        series_descs = defaultdict(lambda x: x, site.config['SERIES_DESCRIPTIONS'])

        for post in sorted(site.posts, key=lambda p: p.date):
            series_tag = post.meta[site.default_lang]['series']
            if series_tag:
                series_posts[series_tag].append(post)

        series_data = {tag: SeriesDescription(description=series_descs[tag], posts=posts)
                        for tag, posts in series_posts.items()}
        LOGGER.debug(pformat(series_data))

        site._GLOBAL_CONTEXT['series'] = series_data
