# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    # define the fields for your item here like:

    province = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    price = scrapy.Field()
    origin_url = scrapy.Field()
