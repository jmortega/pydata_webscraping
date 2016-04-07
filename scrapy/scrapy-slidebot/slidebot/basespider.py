from scrapy.spider import Spider as _Spider


class BaseSpider(_Spider):
    """Slides spider."""

    def __init__(self, *args, **kwargs):
        """Initialize start urls from input (a file) or url argument."""
        arg_input = kwargs.get('input')
        arg_url = kwargs.get('url')
        if arg_input:
            with open(arg_input) as fp:
                self.start_urls = [line.strip() for line in fp]
        elif arg_url:
            # allow to provide urls separated by |
            self.start_urls = arg_url.split('|')
        else:
            raise ValueError('missing input or url argument')
