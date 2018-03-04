# -*- coding: utf-8 -*-
from itertools import chain
from urllib.parse import urlencode

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags

from . import urls
from .loader import OtodomApartmentLoader


class OtodomSpider(CrawlSpider):
    name = 'otodom'
    allowed_domains = ['otodom.pl']

    # Workaround for otodom displaying a maximum of 500 pages of results,
    # split the search into price segments
    start_urls = [
        urls.search(min_price=min_price, max_price=min_price + 50_000)
        for min_price in range(0, 1_000_000, 50_000)
    ]
    start_urls.append(urls.search(min_price=1_000_000))

    start_urls = [urls.search(min_price=0, max_price=50_000)]

    rules = (
        Rule(
            LinkExtractor(
                allow='/sprzedaz/mieszkanie/?(.*&)?page=', 
                restrict_css='.pager .pager-next',
            ), 
        ),
        Rule(
            LinkExtractor(
                allow='/oferta/', 
                restrict_css='.listing-title ~ article',
            ), 
            callback='parse_offer', 
        ),
    )

    def parse_offer(self, response):
        features = [
            remove_tags(feature_html).strip()
            for feature_html in chain(
                response.css('.params-list .sub-list li').extract(),
                response.css('.params-list .dotted-list li').extract(),
            )
        ]

        named_features = {}
        for feature in features:
            name, _, value = feature.partition(': ')

            if value:
                named_features[name.strip()] = value.strip()

        loader = OtodomApartmentLoader(response=response)

        loader.add_css(
            'id', 
            '.section-offer-text.updated .text-details .left p:first-child', 
            re=r'Nr oferty w Otodom: (\d+)',
        )

        loader.add_css('url', 'head link[rel="canonical"]::attr(href)')
        loader.add_css('url', 'head meta[property="og:url"]::attr(content)')
        loader.add_value('url', response.url)

        loader.add_css('title', 'header [itemprop=name]')
        loader.add_css('description', '[itemprop=description]')

        loader.add_css(
            'price', 
            '[itemtype="http://schema.org/PropertyValue"] [itemprop=value]', 
            re=r'([\d ]+([,.]\d+)?) zł',
        )
        loader.add_value(
            'rent', 
            named_features.get('Czynsz'), 
            re=r'([\d ]+([,.]\d+)?) zł',
        )
        loader.add_value('ownership', named_features.get('Forma własności'))
        
        loader.add_css('address', 'header [itemprop=address]')
        loader.add_css('latitude', 'meta[itemprop=latitude]::attr(content)')
        loader.add_css('longitude', 'meta[itemprop=longitude]::attr(content)')
        
        loader.add_value('market', named_features.get('Rynek'))
        loader.add_css('area', '.param_m strong', re=r'([\d ]+([,.]\d+)?) m²')
        loader.add_css('rooms', '.room-lane .big')
        loader.add_css('floor', '.param_floor_no strong')
        
        loader.add_value('building_type', named_features.get('Rodzaj zabudowy'))
        loader.add_value('building_material', named_features.get('Materiał budynku'))
        loader.add_css('building_floors', '.param_floor_no span::text', re=r'\(z (\d+)\)')
        loader.add_value('building_year', named_features.get('Rok budowy'))
        loader.add_value('building_heating', named_features.get('Ogrzewanie'))
        
        for feature in features:
            loader.add_value('features', feature)
        
        loader.add_css('image_urls', '[itemtype="http://schema.org/ImageGallery"] a[itemprop=contentUrl]::attr(href)')

        return loader.load_item()
