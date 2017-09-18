# -*- coding: utf-8 -*-
import scrapy
import  re

from baidubaike.items import BaidubaikeItem,RelatedInfoItem
from datetime import  datetime
from collections import deque


script = """
function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(args.wait))
    key_word = splash:select('.lemmaWgt-subLemmaListTitle')
    
    if(key_word~=nil)
    then
        a = splash:select('.custom_dot .list-dot:first-child .para a')
        jump = a:get_attributes('href')
        assert(splash:go(jump))
        assert(splash:wait(0.5))
    end
    return splash:html()
end
"""


class BaikeSpider(scrapy.Spider):

    http_user= 'admin'
    http_pass= 'admin'

    name = "baike"
    allowed_domains = ["baike.baidu.com"]
    start_urls = ['http://baike.baidu.com/']

    item_queue = deque()
    item_queue.clear()
    f = open('d:/test.txt', 'r', encoding='utf-8')
    item_seed = f.readlines()
    for item in item_seed:
        str = re.match(r'[^\t]+\t([^\t]+)\t[^\t]+\t', item)
        item_n = str.group(1)
        item_queue.append(item_n)#所有入口种子存放在队列之中
    
    filename = 'd:/html/'
    if not os.path.exists(filename):#创建文件如果文件不存在
        os.makedirs(filename)

        
        
    def start_requests(self):
        first_url = 'http://baike.baidu.com/item/'+self.item_queue.popleft()#弹出队列中第一个item
        yield scrapy.Request(first_url, callback=self.start_parse, priority=0, meta={'priority': 0, 'time':1,'splash': {
            'args': {'lua_source': script, 'wait': 0.5}, 'endpoint': 'execute'}})  # 第一层地址


    def start_parse(self, response):

        if(response.meta.get('time')==1):#仅第一个入口种子执行while循环的初始化，产生所有种子url，后续种子跳过该环节
            while (self.item_queue):  # 生成所有种子的request ；队列为空返回false
                seed_url = 'http://baike.baidu.com/item/' + self.item_queue.popleft()
                yield scrapy.Request(seed_url, callback=self.start_parse, priority=0, meta={'priority': 0, 'time':0,'splash': {
                    'args': {'lua_source': script, 'wait': 0.5}, 'endpoint': 'execute'}})  # 第一层种子地址


        if (response.css('.baikeLogo').extract_first()!=None):#判断是否存在该词条
            pass

        else:#词条存在则提取页面信息生成item
            item = BaidubaikeItem()
            self.title = response.css('.lemmaWgt-lemmaTitle-title h1::text').extract_first()
            self.title_polysemy=response.css('.lemmaWgt-lemmaTitle-title h2::text').extract_first()#判断是否为歧义项
            if(self.title_polysemy==None):
                item['title'] = self.title
                item['polysemy'] = 0
                item['origin'] = None
            else:
                item['title'] = self.title+self.title_polysemy
                item['polysemy'] = 1
                item['origin'] = self.title

            item['id'] = response.css('.description ul>li>a::attr(href)').re_first(r'/historylist/[^/]*/([0-9]*)')
            item['url'] = 'http://baike.baidu.com/item/'+self.title+'/'+item['id']
            item['view'] = response.css('.description ul>li>span[id=j-lemmaStatistics-pv]::text').extract_first()
            item['resource'] = item['title']+'.html'
            item['crawled_at'] = datetime.now()
            item['layer'] = response.meta.get('priority')
            yield item

            with open(self.filename+item['title']+'.html', 'wb') as file_writer: #download html
                file_writer.write(bytes(response.text,encoding='utf-8'))


            #创建关联实体的request
            self.relate_item = response.css('div[class=para][label-module=para] a[target=_blank]::text').re(r'[^\n]+')
            for item_next in self.relate_item:
                relate_url = 'http://baike.baidu.com/item/' + item_next
                priority = response.meta.get('priority')-1
                father_id = item['id']
                father_title = item['title']
                yield scrapy.Request(relate_url, callback=self.follow_parse, priority=priority,
                                     meta={'priority': priority, 'father_id': father_id, 'father_title': father_title,
                                           'related_title': item_next,
                                           'splash': {'args': {'lua_source': script, 'wait': 0.5},
                                                      'endpoint': 'execute'}})




    def follow_parse(self,response):#处理关联实体页面
        if (response.css('.baikeLogo').extract_first() != None):  # 判断是否存在该词条
            pass
        else:#处理关联实体，提取信息生成item/item_related（插入种子的related字段中）
            item = BaidubaikeItem()
            item_related = RelatedInfoItem()
            self.title = response.css('.lemmaWgt-lemmaTitle-title h1::text').extract_first()
            self.title_polysemy = response.css('.lemmaWgt-lemmaTitle-title h2::text').extract_first()  # 判断是否为歧义项
            if (self.title_polysemy == None):
                item['title'] =  self.title#关联词的全名
                item['polysemy'] = 0
                item['origin'] = None
            else:
                item['title'] =  self.title + self.title_polysemy
                item['polysemy'] = 1
                item['origin'] = self.title

            item_related['title'] = response.meta.get('related_title')#上一层页面中关联词
            item['id'] = item_related['id'] = response.css('.description ul>li>a::attr(href)').re_first(r'/historylist/[%A-Za-z0-9]*/([0-9]*)')
            item['url'] = 'http://baike.baidu.com/item/'+self.title+'/'+item['id']
            item['view'] = response.css('.description ul>li>span[id=j-lemmaStatistics-pv]::text').extract_first()
            item['resource'] = item['title']+'.html'
            item['crawled_at'] = datetime.now()
            item['layer'] = response.meta.get('priority')
            item['father_title'] = response.meta.get('father_title')
            item_related['father_id'] = response.meta.get('father_id')#获取父节点的id

            yield item
            yield item_related
            
            with open(self.filename+item['title']+'.html', 'wb') as file_writer: #download html
                file_writer.write(bytes(response.text,encoding='utf-8'))

            #生成下一节点的request
            self.relate_item = response.css('div[class=para][label-module=para] a[target=_blank]::text').re(r'[^\n]+')
            for item_next in self.relate_item:
                relate_url = 'http://baike.baidu.com/item/' + item_next
                priority = response.meta.get('priority') - 1
                father_id = item['id']
                father_title = item['title']
                yield scrapy.Request(relate_url, callback=self.follow_parse, priority=priority,
                                     meta={'priority': priority, 'father_id': father_id, 'father_title': father_title,
                                           'related_title': item_next,
                                           'splash': {'args': {'lua_source': script, 'wait': 0.5},
                                                      'endpoint': 'execute'}})






