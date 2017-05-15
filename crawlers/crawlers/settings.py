# -*- coding: utf-8 -*-

# Scrapy settings for crawlers project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawlers'

SPIDER_MODULES = ['crawlers.spiders']
NEWSPIDER_MODULE = 'crawlers.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawlers (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

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
#SPIDER_MIDDLEWARES = {
#    'crawlers.middlewares.CrawlersSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawlers.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
##    'crawlers.pipelines.CrawlersPipeline': 300,
    'crawlers.pipelines.GoogleMapsPipeline':450,
#    'crawlers.pipelines.GoogleMapsSubstitutePipeline':450,
#    'crawlers.pipelines.FilterPipeline':350,
    'crawlers.pipelines.ElasticsearchPipeline':500,
#    'crawlers.pipelines.UIDcheckPipeline' : 400,
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


# settings for elasticsearch
ELASTIC_SETTINGS = {
        'host': "tvesovla.asuscomm.com",
        'port': 9200,
        'index_name':"blocket_new_anlyzers_without_filtering",
        'index_prop' : { # Index properties for the new index
            "settings": {
                "analysis": {
                    "analyzer": {
                        "patterns_analyzer": {
                            "tokenizer": "patterns_tokenizer",
                            "filter": ["lowercase", "spacefilter"]
                            }
                        },
                    "tokenizer": {
                        "patterns_tokenizer": {
                            "type": "pattern",
                            "pattern": "([0-9]+[ ]*[Kk][Rr])|([0-9]+[ ]*[Gg][Bb])|([0-9]+([.,:/][0-9]+)+)|([0-9]+[a-zA-z+]+)|([0-9]+)|([a-z,A-Z]+)",
                            "group": 0
                            }
                        },
                    "filter": {
                        "spacefilter": {
                            "type": "pattern_replace",
                            "pattern": " ",
                            "replacement": ""
                            }
                        }
                    }
                },
            "mappings": {
                "blocket_ad": {
                    "properties": {
                        "ad_text": {
                            "type": "text",
                            "analyzer": "patterns_analyzer"
                            },
                        "datetime": {
                            "type" : "date"
                            },
                        "price" : {
                            "type" : "long"
                            },
                        "title": {
                            "type": "text",
                            "analyzer" : "patterns_analyzer",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                    }
                                }
                            },
                        "loc_name": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                    }
                                }
                            },
                        "location": {
                            "type" : "geo_point"
                            },
                        "company_ad": {
                            "type": "boolean"
                            },
                        "url": {
                            "type": "text"
                            }
                        }
                    }
                }
            }
        }

GOOGLEMAPS = {
        'api_key' : "AIzaSyA9d-hRcRfnfSDzd709zmQJORutp96n9r0",
        'loc_dict_filename': "location_dictionary"
        }
