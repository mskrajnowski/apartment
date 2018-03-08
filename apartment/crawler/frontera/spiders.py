from scrapy import signals, spiders
from scrapy.exceptions import DontCloseSpider


class KeepIdleMixin:
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        spider.crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self):
        self.log("Spider idle signal caught.")
        raise DontCloseSpider


class Spider(KeepIdleMixin, spiders.Spider):
    pass


class CrawlSpider(KeepIdleMixin, spiders.CrawlSpider):
    pass
