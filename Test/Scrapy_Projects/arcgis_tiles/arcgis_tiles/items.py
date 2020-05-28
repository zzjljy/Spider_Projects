# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class ArcgisTilesItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class ArcgisTilesJson(scrapy.Item):
    collection = table = 'service'
    service_name = scrapy.Field()
    service_config = scrapy.Field()
    layers = scrapy.Field()


class ArcgisTilesItem(scrapy.Item):
    tile_collection = scrapy.Field()
    row = scrapy.Field()
    col = scrapy.Field()
    level = scrapy.Field()
    image = scrapy.Field()