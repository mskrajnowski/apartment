# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, Identity, MapCompose, TakeFirst
from w3lib.html import remove_tags

from ...items import Apartment


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


class OtodomApartmentLoader(ItemLoader):
    default_item_class = Apartment
    default_input_processor = MapCompose(remove_tags, str.strip)
    default_output_processor = TakeFirst()

    urls_out = Identity()
    features_out = Identity()
    image_urls_out = Identity()
    images_out = Identity()

    id_in = Compose(default_input_processor, MapCompose(parse_int))
    area_in = Compose(default_input_processor, MapCompose(parse_float))
    building_floors_in = Compose(default_input_processor, MapCompose(parse_int))
    building_year_in = Compose(default_input_processor, MapCompose(parse_int))
    floor_in = Compose(default_input_processor, MapCompose(parse_int))
    latitude_in = Compose(default_input_processor, MapCompose(parse_float))
    longitude_in = Compose(default_input_processor, MapCompose(parse_float))
    rent_in = price_in = Compose(default_input_processor, MapCompose(parse_float))
    rooms_in = Compose(default_input_processor, MapCompose(parse_int))
