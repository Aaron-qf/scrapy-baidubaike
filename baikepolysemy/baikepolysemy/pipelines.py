# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo.errors import DuplicateKeyError


class BaikepolysemyPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_url = mongo_uri
        self.mongo_db  = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB2')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # self.db.polysemyInfo.create_index([('label', pymongo.ASCENDING)])  # 建立source的唯一索引
        self.db.polysemyInfo.insert(dict(item))

        return item




    def close_spider(self,spider):
        self.client.close()
