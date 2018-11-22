# -*- coding: utf-8 -*-

# Scrapy settings for springer_project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'springer_project'

SPIDER_MODULES = ['springer_project.spiders']
NEWSPIDER_MODULE = 'springer_project.spiders'

LOG_LEVEL = 'WARNING'
LOG_FILE = './springer.log'

RETRY_TIMES = 5  # 指定失败后重复尝试的次数
DOWNLOAD_TIME = 20  # 指定超时时间

# DOWNLOAD_FAIL_ON_DATALOSS = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.3
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
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'springer_project.middlewares.SpringerProjectSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'springer_project.middlewares.SpringerProjectDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'springer_project.pipelines.SpringerProjectPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# 使用scrapy-redis里的去重组件，不使用scrapy默认的去重方式
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 使用scrapy-redis里的调度器组件，不使用默认的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 允许暂停，redis请求记录不丢失
SCHEDULER_PERSIST = True

# 默认的scrapy-redis请求队列形式（按优先级）
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"

# 指定数据库的主机IP
REDIS_HOST = "127.0.0.1"
# 指定数据库的端口号
REDIS_PORT = 6379
# REDIS_URL = "redis://127.0.0.1:6379"

FEED_EXPORT_ENCODING = 'UTF-8'

DOWNLOAD_FAIL_ON_DATALOSS = False

# IMAGES_STORE = '.\Image'  # 图像存储

# #################    MONGODB     #############################
# MONGODB_SERVER = 'localhost'
# MONGODB_PORT = 27017
# MONGODB_DB = 'dqd_db'  # 数据库
# MONGODB_COLLECTION = 'dqd_collection'  # 集合
#
# ####################    MYSQL      #############################
# MYSQL_HOST = 'localhost'
# MYSQL_DBNAME = 'dqd_database'  # 数据库名称
# MYSQL_USER = 'root'
# MYSQL_PASSWD = 'mysql'

# 待爬取完后调试异常处理  # TODO
# 2018-09-30 21:49:17 [scrapy.core.downloader.handlers.http11]
# WARNING: Got data loss in https://link.springer.com/article/10.1007/BF01080452.
# If you want to process broken responses set the setting DOWNLOAD_FAIL_ON_DATALOSS = False --
# This message won't be shown in further requests
"""
DOWNLOAD_FAIL_ON_DATALOSS = False

如果设置为 True :
scrapy.Request 有一个 errback 参数, 当 Request 请求出错的时候,会自动调用这个回调函数

如果设置为 False:
scrapy 会自动添加一个名为 dataloss 的 flag 到 response.flags, 用下面代码判断是否发生错误:

if 'dataloss' in response.flags:
"""