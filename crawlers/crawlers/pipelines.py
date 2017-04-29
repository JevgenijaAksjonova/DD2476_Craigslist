# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch
import time


class CrawlersPipeline(object):
    def process_item(self, item, spider):
        return item

class ElasticsearchPipeline(object):

    def __init__(self, es_address = None, es_port = None):

        self.es_host = es_address
        self.es_port = es_port

    @classmethod
    def from_crawler(cls, crawler):

        es_settings = crawler.settings.get('ELASTIC_SETTINGS')
        return cls( es_settings['host'], es_settings['port'] )

    def open_spider(self, spider):
        self.es = Elasticsearch([{'host': self.es_host, 'port': self.es_port}])
        self.index_name = 'blocket_'+time.strftime("%Y-%m-%d_%X", time.gmtime())
        self.es.indices.create(index=self.index_name)
        self.id = 1

    def process_item(self, item, spider):

        print("hahahah")
        # add the document, i.e. item, to index self.index_name
        self.es.create(index=self.index_name, id=str(self.id), body=item, doc_type="external")
        # increase id number
        self.id += 1

        return item


