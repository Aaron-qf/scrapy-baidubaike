# -*- coding: utf-8 -*-
from collections import deque
from urllib.parse import unquote

import pymongo
import scrapy
import re
import json

from baikepolysemy.items import BaikepolysemyItem
from scrapy import crawler


script = """
function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(args.wait))
    return splash:html()
end
"""

class PolysemySpider(scrapy.Spider):
    http_user = 'admin'
    http_pass = 'admin'

    name = "polysemy"
    allowed_domains = ["baike.baidu.com"]
    start_urls = ['http://baike.baidu.com/']
    client = pymongo.MongoClient('mongodb://datacrawl-mongostore:AzHHSIXn1SLfHv7GurDSwPHDiCHSQUyjk2zjx3IUXCDhnaiUyqFGHclev8aPdCHB6IgkYqYVHrvxiyowfAgTnQ==@datacrawl-mongostore.documents.azure.cn:10250/?ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client['baidubaike']
    collection = db.entityInfo

    def start_requests(self):
        # self.client = pymongo.MongoClient(self.settings.get('MONGO_URI'))
        # self.db = self.client[self.settings.get('MONGO_DB2')]
        # self.collection = self.db.entityInfo
        self.item = self.collection.find_one_and_update({'read' : 0},{'$set': {'read': 1}})
        if (self.item['polysemy']==0):
            self.name = self.item['title']
        else:
            self.name = self.item['origin']


        first_url = 'http://baike.baidu.com/item/' + self.name +'?force=1'  # 弹出队列中第一个item
        yield scrapy.Request(first_url, callback=self.parse, priority=0,
                             meta={'priority': 0,'splash': {
                                 'args': {'lua_source': script, 'wait': 0.5}, 'endpoint': 'execute'}})  # 第一层地址

    def parse(self, response):


        if(response.css('.lemmaWgt-subLemmaListTitle').extract_first()!=None):#歧义项
            label = response.css('.lemmaWgt-lemmaTitle-title h1::text').extract_first()
            items = response.css('div[class=para][label-module=para] a[target=_blank]')
            for item in items:
                polysemy_url = 'http://baike.baidu.com'+item.css('a::attr(href)').extract_first()
                polysemy_title = item.css('a::text').extract_first()
                yield scrapy.Request(polysemy_url, callback=self.polysemy_parse, priority=0,
                                     meta={'priority': 0, 'label': label,
                                           'polysemy_url': polysemy_url, 'polysemy_title': polysemy_title,
                                           'splash': {
                                               'args': {'lua_source': script, 'wait': 0.5},
                                               'endpoint': 'execute'}})  # 传递值给歧义项




        else:#非歧义项
            item = BaikepolysemyItem()
            item['polysemy'] = 0
            item['label'] = item['title'] = response.css('.lemmaWgt-lemmaTitle-title h1::text').extract_first()
            id = response.css('.description ul>li>a::attr(href)').re_first(r'/historylist/[^/]*/([0-9]*)')
            item['url'] = 'http://baike.baidu.com/item/'+item['label']+'/'+id
            segments = response.css('div[class=lemma-summary][label-module=lemmaSummary] *::text').re(r'\S+')
            item['summary'] = "".join(segments)
            view = response.css('.description ul>li>span[id=j-lemmaStatistics-pv]::text').extract_first()
            if (view == None):
                item['view'] = -1
            else:
                item['view'] = view

            yield item



        # self.client = pymongo.MongoClient(self.settings.get('MONGO_URI'))
        # self.db = self.client[self.settings.get('MONGO_DB2')]
        # self.collection = self.db.entityInfo

        if(self.collection.find_one({'read' : 0})==None):
            pass
        else:
            self.item = self.collection.find_one_and_update({'read': 0}, {'$set': {'read': 1}})
            if (self.item['polysemy'] == 0):
                self.name = self.item['title']
            else:
                self.name = self.item['origin']
            next_url = 'http://baike.baidu.com/item/' + self.name + '?force=1'  # 弹出队列中下一个item
            yield scrapy.Request(next_url, callback=self.parse, priority=0,
                             meta={'priority': 0, 'splash': {
                                 'args': {'lua_source': script, 'wait': 0.5}, 'endpoint': 'execute'}})  # 下一项


    def polysemy_parse(self,response):#处理歧义项
        item = BaikepolysemyItem()
        item['polysemy'] = 1
        item['label'] = response.meta.get('label')
        url = response.meta.get('polysemy_url')
        item['url'] = unquote(url)
        item['title'] = response.meta.get('polysemy_title')
        segments = response.css('div[class=lemma-summary][label-module=lemmaSummary] *::text').re(r'\S+')
        item['summary'] = "".join(segments)
        view = response.css('.description ul>li>span[id=j-lemmaStatistics-pv]::text').extract_first()
        if (view == None):
            item['view'] = -1
        else:
            item['view'] = view
        yield item









