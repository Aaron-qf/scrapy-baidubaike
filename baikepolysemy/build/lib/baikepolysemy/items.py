# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaikepolysemyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    polysemy = scrapy.Field()
    label = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    view = scrapy.Field()

# class AntipolysemyItem(scrapy.Item):

