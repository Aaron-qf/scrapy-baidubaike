# -*- coding: utf-8 -*-
from scrapy import Request,Spider,signals
import re

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


class SeedsSpider(Spider):
    name = "seeds"
    queue = 'baike'
    allowed_domains = ["baike.baidu.com"]
    start_urls = ['http://baike.baidu.com/']
    file_name = 'd:/tag_sameMeaningTags_idf_ver4.txt'

    http_user = 'admin'
    http_pass = 'admin'

    custom_settings = {
        'SCHEDULER': 'seed.scheduler.Scheduler',
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter'
    }

    def start_requests(self):
        self.crawler.signals.connect(self.make_requests,signal= signals.spider_idle )
        return []

    def make_requests(self):
        for request in self.start():
            self.crawler.engine.slot.scheduler.enqueue_request(request)


    def start(self):
        with open(self.file_name,'r',encoding='utf-8') as f:
            for line in f.readlines():
                str = re.match(r'[^\t]+\t([^\t]+)\t[^\t]+\t', line)
                seed = str.group(1)
                print(seed)
                url = 'http://baike.baidu.com/item/' + seed
                yield Request(url,  priority=0,callback = self.parse,
                                     meta={'priority': 0, 'time': 0, 'splash': {
                                         'args': {'lua_source': script, 'wait': 0.5}, 'endpoint': 'execute'}})  # 第一层地址



    def parse(self, response):
        pass
