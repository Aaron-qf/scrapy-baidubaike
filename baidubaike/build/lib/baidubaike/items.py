# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaidubaikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    view = scrapy.Field()
    resource = scrapy.Field()
    crawled_at = scrapy.Field()
    polysemy = scrapy.Field()
    origin = scrapy.Field()
    layer = scrapy.Field()
    father_title = scrapy.Field()
    html = scrapy.Field()
    read = scrapy.Field()

class RelatedInfoItem(scrapy.Item):
    title = scrapy.Field()
    father_id = scrapy.Field()
    id = scrapy.Field()





