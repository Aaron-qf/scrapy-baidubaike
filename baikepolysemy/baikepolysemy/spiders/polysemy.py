# -*- coding: utf-8 -*-
from collections import deque
from urllib.parse import unquote

import scrapy
import json

from baikepolysemy.items import BaikepolysemyItem

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

    item_queue = deque()
    item_queue.clear()
    f = open('d:/json/s.json', 'r', encoding='utf-8')#读取json格式的文件
    item_seed = f.readlines()
    for item in item_seed:
        item_j = json.loads(item)
        item_n = item_j['origin']
        item_queue.append(item_n)  # 所有入口种子存放在队列之中
    print('all seeds have been processed successfully!')

    def start_requests(self):
        first_url = 'http://baike.baidu.com/item/' + self.item_queue.popleft() +'?force=1'  # 弹出队列中第一个item
        yield scrapy.Request(first_url, callback=self.parse, 
                             meta={'splash': {'args': {'lua_source': script, 'wait': 0.5}, 'endpoint': 'execute'}})  # 第一层地址

        
    def parse(self, response):
        
        if(response.css('.lemmaWgt-subLemmaListTitle').extract_first()!=None):#歧义项
            label = response.css('.lemmaWgt-lemmaTitle-title h1::text').extract_first()#标签
            items = response.css('div[class=para][label-module=para] a[target=_blank]')#获得多个歧义项
            for item in items:
                polysemy_url = 'http://baike.baidu.com'+item.css('a::attr(href)').extract_first()
                polysemy_title = item.css('a::text').extract_first()
                yield scrapy.Request(polysemy_url, callback=self.polysemy_parse, 
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
            segments = response.css('div[class=lemma-summary][label-module=lemmaSummary] div::text').extract()
            item['summary'] = "".join(segments)
            view = response.css('.description ul>li>span[id=j-lemmaStatistics-pv]::text').extract_first()
            if (view == None):
                item['view'] = -1
            else:
                item['view'] = view

            yield item

        #生成下一搜索项的request
        if(len(self.item_queue)== 0):
            pass
        else:
            next_url = 'http://baike.baidu.com/item/' + self.item_queue.popleft() + '?force=1'  # 弹出队列中下一个item
            yield scrapy.Request(next_url, callback=self.parse, 
                                meta={'splash': {'args': {'lua_source': script, 'wait': 0.5}, 'endpoint': 'execute'}})  # 下一项


    def polysemy_parse(self,response):#处理歧义项页面
        item = BaikepolysemyItem()
        item['polysemy'] = 1
        item['label'] = response.meta.get('label')
        url = response.meta.get('polysemy_url')
        item['url'] = unquote(url)
        item['title'] = response.meta.get('polysemy_title')
        segments = response.css('div[class=lemma-summary][label-module=lemmaSummary] div::text').extract()
        item['summary'] = "".join(segments)
        view = response.css('.description ul>li>span[id=j-lemmaStatistics-pv]::text').extract_first()
        if (view == None):
            item['view'] = -1
        else:
            item['view'] = view
        yield item









