# -*- coding: utf-8 -*-
import scrapy


class OtodomSpider(scrapy.Spider):
    name = 'otodom'
    allowed_domains = ['otodom.pl']
    start_urls = ['http://otodom.pl/']

    def parse(self, response):
        pass
