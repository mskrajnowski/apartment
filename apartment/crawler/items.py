# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Apartment(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
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
