# -*- coding: utf-8 -*-

# Scrapy settings for arcgis_tiles project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'arcgis_tiles'

SPIDER_MODULES = ['arcgis_tiles.spiders']
NEWSPIDER_MODULE = 'arcgis_tiles.spiders'

POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_DATABASE = 'XXL_SYSTEM'
POSTGRES_USERNAME = 'postgres'
POSTGRES_PASSWORD = '123456'

MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'images360'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_PORT = 3306

MONGO_URI = 'localhost'
MONGO_DB = 'XXL_SYSTEM'

SQLITE_FILE = r'E:\dwg2000.sqlite3'

JOBDIR='myspider'
LOG_LEVEL='WARNING'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'arcgis_tiles (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
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
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'arcgis_tiles.middlewares.ArcgisTilesSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'arcgis_tiles.middlewares.ArcgisTilesDownloaderMiddleware': 543,
   'arcgis_tiles.middlewares.RandomUserAgentMiddleware': 543,
   # 'arcgis_tiles.middlewares.ProxyMiddleWare': 544,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'arcgis_tiles.pipelines.ArcgisTilesPipeline': 300,
    # json信息
   # 'arcgis_tiles.pipelines.PostgresJsonPipeline': 302,
    # 瓦片存入mongo
   # 'arcgis_tiles.pipelines.MongoPipeline': 304,
    # 瓦片存入mysql
    # 'arcgis_tiles.pipelines.MysqlPipeline': 302,
    #瓦片存入sqlite
    'arcgis_tiles.pipelines.Sqlite3Pipeline': 301,
    # 数据存入postgres
    # 'arcgis_tiles.pipelines.PostgresGeoItemPipeline': 305,
    # 'arcgis_tiles.pipelines.PostgresServiceLayerPipeline': 303,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
