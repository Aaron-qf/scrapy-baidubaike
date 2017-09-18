# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib.request
import pymongo
import sys
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from bs4 import  BeautifulSoup

from baidubaike.items import RelatedInfoItem,BaidubaikeItem
from baidubaike.spiders.baike import BaikeSpider
from pymongo.errors import DuplicateKeyError


class BaidubaikePipeline(object):
    def process_item(self, item, spider):
        return item


def item_layer(args):
    pass


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_url = mongo_uri
        self.mongo_db  = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # name = item.__class__.__name__
        self.db.relatedInfo.create_index([('source', pymongo.ASCENDING)], unique=True)  # 建立source的唯一索引
        self.db.entityInfo.create_index([('id', pymongo.ASCENDING)], unique=True)  # 建立source的唯一索引
        if isinstance(item, BaidubaikeItem):  # 实体列表
            try:
                self.db.entityInfo.insert(dict(item))  # 实体信息列表建立
            except DuplicateKeyError as e:#出现重复的实体
                pass
            try:
                self.db.relatedInfo.insert({'layer':item['layer'],'source': item['id'], 'title': item['title'], 'related': []})  # 关联信息列表建立
            except DuplicateKeyError as e:  # 出现重复的实体
                pass
        # if isinstance(item, BaidubaikeItem):#种子列表
        #     for a in BaikeSpider.item_layer:
        #         print(a,'-------------------------')
        #     if(item['layer']==max(BaikeSpider.item_layer) ):
        #         print('!最高层数！！！！！！！！！！！！！！！！',max(BaikeSpider.item_layer))
        #         print('!层数！！！！！！！！！！！！！！！！',item['layer'])
        #         self.db.entityInfo.insert(dict(item))#种子列表实体信息
        #         # BaikeSpider.item_layer.popleft()
        #         self.db.relatedInfo.insert({'source': item['id'], 'title': item['title'],'related': []})#种子列表关联信息
        #         self.db.relatedInfo.ensure_index( [('source',pymongo.ASCENDING)],unique=True)#建立source的唯一索引


        if isinstance(item,RelatedInfoItem):#关联信息的插入
            self.db.relatedInfo.update(
                {'source':item.get('father_id')},
                {'$addToSet':
                    {
                        'related':{'$each':[{'title':item['title'],'id':item['id']}] }
                        # 'title':{'$each':item['title']},
                        # 'id':{'$each':item['id']}
                    }
                },
                upsert = True
            )

        return item




    def close_spider(self,spider):
        self.client.close()

#