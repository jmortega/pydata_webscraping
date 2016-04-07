import re
import subprocess
import weakref

from scrapy.contrib.pipeline.files import FilesPipeline
from scrapy.exceptions import DropItem
from scrapy.utils.httpobj import urlparse_cached
from twisted.internet import threads


class SlideDefaults(object):
    """Set up defaults items."""

    def process_item(self, item, spider):
        if not item.get('id'):
            raise DropItem("item id is missing")
        item['spider'] = spider.name
        return item


class SlideImages(FilesPipeline):
    """Downloads slide images."""

    DEFAULT_FILES_URLS_FIELD = 'image_urls'
    DEFAULT_FILES_RESULT_FIELD = 'images'

    def get_media_requests(self, item, info):
        reqs = super(SlideImages, self).get_media_requests(item, info)
        self._load_keys(reqs, item)
        return reqs

    def _load_keys(self, requests, item):
        # Preload file paths into the requests because we use the item data to
        # generate the path.
        for req in requests:
            pr = urlparse_cached(req)
            # filename is last part of the URL path.
            image = pr.path.rpartition('/')[-1]
            req.meta['file_path'] = '/{slide_id}/{image}'.format(
                spider=item['spider'],
                slide_id=item['id'],
                image=image,
            )

    def file_path(self, request, response=None, info=None):
        return request.meta['file_path']


class SlidePDF(object):
    """Converts slides images to PDF."""

    def process_item(self, item, spider):
        if not item.get('images'):
            raise DropItem("no images found")
        return threads.deferToThread(self._convert, item, spider)

    def _convert(self, item, spider):
        image_paths = [im['path'] for im in item['images']]

        datapath = spider.crawler.settings['FILES_STORE']
        image_files = [datapath + path for path in image_paths]

        item['pdf_file'] = '%s.pdf' % item['id']
        dest = '{root}/{spider}/{file}'.format(
            root=datapath,
            spider=item['spider'],
            file=item['pdf_file'],
        )
        print "file:"+dest
        # Use convert command from ImageMagick.
        cmd = ['convert'] + image_files + [dest]
        try:
            # TODO: capture errors
            subprocess.check_call(cmd, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as detail:
            print detail
            raise DropItem("failed to generate PDF")

        return item
