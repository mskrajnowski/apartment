# -*- coding: utf-8 -*-
import os
import re
from functools import wraps
from itertools import chain, islice

import scrapy
from scrapy.loader.processors import Compose, Identity, MapCompose, TakeFirst
from w3lib.html import remove_tags


class OtodomApartment(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    urls = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()

    price = scrapy.Field()
    rent = scrapy.Field()
    ownership = scrapy.Field()

    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()

    market = scrapy.Field()
    area = scrapy.Field()
    rooms = scrapy.Field()
    floor = scrapy.Field()

    building_type = scrapy.Field()
    building_material = scrapy.Field()
    building_floors = scrapy.Field()
    building_year = scrapy.Field()
    building_heating = scrapy.Field()

    features = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()


def re_extractor(pattern, group=1):
    regex = re.compile(pattern)

    def extractor(text):
        match = regex.match(text)
        return match.group(group) if match else None 

    return extractor


def parse_int(value):
    value.replace(' ', '')

    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def parse_float(value):
    value = value.replace(' ', '').replace(',', '.')

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


class OtodomApartmentLoader(scrapy.loader.ItemLoader):
    default_item_class = OtodomApartment
    default_input_processor = MapCompose(remove_tags, str.strip)
    default_output_processor = TakeFirst()

    urls_out = Identity()
    features_out = Identity()
    image_urls_out = Identity()
    images_out = Identity()

    id_in = Compose(default_input_processor, MapCompose(
        re_extractor(r'^Nr oferty w Otodom: (\d+)$'),
        parse_int,
    ))
    area_in = Compose(default_input_processor, MapCompose(
        re_extractor(r'^([\d ]+([,.]\d+)?) m²$'),
        parse_float,
    ))
    building_floors_in = Compose(default_input_processor, MapCompose(
        re_extractor(r'^\(z (\d+)\)$'), 
        parse_int,
    ))
    building_year_in = Compose(default_input_processor, MapCompose(parse_int))
    floor_in = Compose(default_input_processor, MapCompose(parse_int))
    latitude_in = Compose(default_input_processor, MapCompose(parse_float))
    longitude_in = Compose(default_input_processor, MapCompose(parse_float))
    rent_in = price_in = Compose(default_input_processor, MapCompose(
        re_extractor(r'^([\d ]+([,.]\d+)?) zł$'),
        parse_float,
    ))
    rooms_in = Compose(default_input_processor, MapCompose(parse_int))


class OtodomSpider(scrapy.Spider):
    name = 'otodom'
    allowed_domains = ['otodom.pl']

    def start_requests(self):
        for url in self.settings['OTODOM_START_URLS']:
            yield scrapy.Request(url=url, callback=self.parse_search_results)

    def parse_search_results(self, response):
        offers = response.css('.listing-title ~ article')
        offer_urls = offers.css('a[href*="/oferta/"]::attr(href)')

        for url in offer_urls:
            yield response.follow(url, callback=self.parse_offer)

        for url in response.css('.pager .pager-next a::attr(href)'):
            yield response.follow(url, callback=self.parse_search_results)

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

        loader.add_css('id', '.section-offer-text.updated .text-details .left p:first-child')

        for field in ('url', 'urls'):
            loader.add_css(field, 'head link[rel="canonical"]::attr(href)')
            loader.add_css(field, 'head meta[property="og:url"]::attr(content)')
            loader.add_value(field, response.url)

        loader.add_css('title', 'header [itemprop=name]')
        loader.add_css('description', '[itemprop=description]')

        loader.add_css('price', '[itemtype="http://schema.org/PropertyValue"] [itemprop=value]')
        loader.add_value('rent', named_features.get('Czynsz'))
        loader.add_value('ownership', named_features.get('Forma własności'))
        
        loader.add_css('address', 'header [itemprop=address]')
        loader.add_css('latitude', 'meta[itemprop=latitude]::attr(content)')
        loader.add_css('longitude', 'meta[itemprop=longitude]::attr(content)')
        
        loader.add_value('market', named_features.get('Rynek'))
        loader.add_css('area', '.param_m strong')
        loader.add_css('rooms', '.room-lane .big')
        loader.add_css('floor', '.param_floor_no strong')
        
        loader.add_value('building_type', named_features.get('Rodzaj zabudowy'))
        loader.add_value('building_material', named_features.get('Materiał budynku'))
        loader.add_css('building_floors', '.param_floor_no span::text')
        loader.add_value('building_year', named_features.get('Rok budowy'))
        loader.add_value('building_heating', named_features.get('Ogrzewanie'))
        
        for feature in features:
            loader.add_value('features', feature)
        
        loader.add_css('image_urls', '[itemtype="http://schema.org/ImageGallery"] a[itemprop=contentUrl]::attr(href)')

        return loader.load_item()
