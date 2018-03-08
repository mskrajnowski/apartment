# -*- coding: utf-8 -*-

import os

from apartment.crawler.shub import environment


# Convert scrapinghub ENV_* settings to environment variables,
# so we can use them to build settings
environment.load_env()

# Scrapy settings for apartment project
# https://doc.scrapy.org/en/latest/topics/settings.html

BOT_NAME = 'apartment'

SPIDER_MODULES = ['apartment.crawler.spiders']
NEWSPIDER_MODULE = 'apartment.crawler.spiders'

# TODO: name the bot :)
#USER_AGENT = 'apartment (+http://www.yourdomain.com)'

COOKIES_ENABLED = False
REDIRECT_ENABLED = True
RETRY_ENABLED = False   # Will be handled by Frontera
TELNETCONSOLE_ENABLED = False

SPIDER_MIDDLEWARES = {
    # See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
    # 'apartment.crawler.middlewares.ApartmentSpiderMiddleware': 543,
    'frontera.contrib.scrapy.middlewares.schedulers.SchedulerSpiderMiddleware': 999,
}

DOWNLOAD_MAXSIZE = 10 * 1024 * 1024  # 10MB Maximum document size
DOWNLOAD_TIMEOUT = 60
DOWNLOADER_MIDDLEWARES = {
    # See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
    # 'apartment.crawler.middlewares.ApartmentDownloaderMiddleware': 543,
    'frontera.contrib.scrapy.middlewares.schedulers.SchedulerDownloaderMiddleware': 999,
}

EXTENSIONS = {
    # See https://doc.scrapy.org/en/latest/topics/extensions.html
    # 'scrapy.extensions.telnet.TelnetConsole': None,
}

ITEM_PIPELINES = {
    # See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
    # 'apartment.crawler.pipelines.ApartmentPipeline': 300,
}

# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
ROBOTSTXT_OBEY = True

# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Frontera
SCHEDULER = 'frontera.contrib.scrapy.schedulers.frontier.FronteraScheduler'
FRONTERA_SETTINGS = 'apartment.crawler.frontera.settings'

# Scrapinghub
SHUB_PROJECT_ID=os.environ.get('SHUB_PROJECT_ID', '')
SHUB_API_KEY=os.environ.get('SHUB_API_KEY', '')
