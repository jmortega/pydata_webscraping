# Scrapy settings for slideshare project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'slidebot'

SPIDER_MODULES = ['slidebot.spiders']
NEWSPIDER_MODULE = 'slidebot.spiders'

ITEM_PIPELINES = {
    'slidebot.pipelines.SlideDefaults': 10,
    'slidebot.pipelines.SlideImages': 20,
    'slidebot.pipelines.SlidePDF': 30,
}

# relative path to execution working directory
FILES_STORE = 'output'

CONCURRENT_ITEMS = 1
CONCURRENT_REQUESTS = 3

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'slidebot (+http://www.yourdomain.com)'
