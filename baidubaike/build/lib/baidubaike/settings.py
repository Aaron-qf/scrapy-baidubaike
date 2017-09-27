# -*- coding: utf-8 -*-

# Scrapy settings for baidubaike project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'baidubaike'

SPIDER_MODULES = ['baidubaike.spiders']
NEWSPIDER_MODULE = 'baidubaike.spiders'

SPLASH_URL = 'http://211.159.152.173:8050/'
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

REDIS_URL = 'redis://:SUlJXNItlgxjZJv6dyGApHaEoS+ccNKhWGBAFEso9cU=@DataCrawl-Pool2.redis.cache.chinacloudapi.cn:6379'


MONGO_URI = 'mongodb://datacrawl-mongostore:AzHHSIXn1SLfHv7GurDSwPHDiCHSQUyjk2zjx3IUXCDhnaiUyqFGHclev8aPdCHB6IgkYqYVHrvxiyowfAgTnQ==@datacrawl-mongostore.documents.azure.cn:10250/?ssl=true&ssl_cert_reqs=CERT_NONE'
MONGO_DB ='baidubaike'

QINIU_ACCESS_KEY = 'H3dzG379hH1dS3rIgW5uMIy1e7HX3R-apWVY9upV'
QINIU_SECRET_KEY = 'Eqs6vTrAXRtKicK0IKIvLZo5HpvEeJyavVPPeBlI'
QINIU_BUCKET = 'baidubaike-html'

# 爬虫队列的存储方式,默认会使用 PriorityQueue
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'baidubaike (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#每次启动重新爬取（默认FALSE，不重爬）
SCHEDULER_FLUSH_ON_START = False

#所有任务爬取完不清除队列
SCHEDULER_PERSIST = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # 'baidubaike.middlewares.BaidubaikeSpiderMiddleware': 543,
   'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'baidubaike.middlewares.MyCustomDownloaderMiddleware': 543,
   # 'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware':722,
   'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware':722,
   'scrapy_splash.SplashCookiesMiddleware': 723,
   'scrapy_splash.SplashMiddleware': 725,
   'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'baidubaike.pipelines.BaidubaikePipeline': 300,
   'baidubaike.pipelines.MongoPipeline': 300,
   'baidubaike.pipelines.QiniuPipeline': 290,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

