# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


from baidubaike.items import RelatedInfoItem,BaidubaikeItem
from baidubaike.spiders.baike import BaikeSpider
from pymongo.errors import DuplicateKeyError
from qiniu import put_stream, Auth
from io import BytesIO

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
        # self.db.relatedInfo.create_index([('source', pymongo.ASCENDING)], unique=True)  # 建立source的唯一索引
        # self.db.entityInfo.create_index([('id', pymongo.ASCENDING)], unique=True)  # 建立source的唯一索引
        if isinstance(item, BaidubaikeItem):  # 实体列表
            try:
                self.db.entityInfo.insert(dict(item))  # 实体信息列表建立
            except DuplicateKeyError as e:#出现重复的实体
                pass
            try:
                self.db.relatedInfo.insert({'layer':item['layer'],'source': item['id'], 'title': item['title'], 'related': []})  # 关联信息列表建立
            except DuplicateKeyError as e:  # 出现重复的实体
                pass


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




#存储html到七牛云
class QiniuPipeline(object):
    def __init__(self, qiniu_access_key, qiniu_secret_key, qiniu_bucket):
        self.qiniu_access_key = qiniu_access_key
        self.qiniu_secret_key = qiniu_secret_key
        self.qiniu_bucket = qiniu_bucket

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            qiniu_access_key=crawler.settings.get('QINIU_ACCESS_KEY'),
            qiniu_secret_key=crawler.settings.get('QINIU_SECRET_KEY'),
            qiniu_bucket=crawler.settings.get('QINIU_BUCKET')
        )

    def open_spider(self, spider):
        self.auth = Auth(self.qiniu_access_key, self.qiniu_secret_key)

    def process_item(self, item, spider):
        if isinstance(item, BaidubaikeItem):
            key = item['title'] + '.html'
            token = self.auth.upload_token(self.qiniu_bucket, key, 3600)
            content = item['html']
            io = BytesIO()
            io.write(content.encode('utf-8'))
            ret, info = put_stream(token, key, io, key, len(content.encode('utf-8')))
            print(ret, info)
            # item['resource'] = key
            del item['html']
        return item
