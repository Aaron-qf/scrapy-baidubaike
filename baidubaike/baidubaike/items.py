# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaidubaikeItem(scrapy.Item):#实体项
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
    layer = scrapy.Field()#为了调试方便而添加的网页层数，导出时不添加此项
    father_title = scrapy.Field()#为了调试方便而添加的父节点名称，导出时不添加此项

class RelatedInfoItem(scrapy.Item):#关联项
    title = scrapy.Field()
    father_id = scrapy.Field()
    id = scrapy.Field()





