# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch
import googlemaps
import time


class CrawlersPipeline(object):
    def process_item(self, item, spider):
        return item

class ElasticsearchPipeline(object):

    def __init__(self, es_address = None, es_port = None, index_name = None):

        self.es_host = es_address
        self.es_port = es_port
        self.index_name = index_name

    @classmethod
    def from_crawler(cls, crawler):

        es_settings = crawler.settings.get('ELASTIC_SETTINGS')
        if 'index_name' in es_settings:
            return cls( es_settings['host'], es_settings['port'], es_settings['index_name'] )
        else:
            return cls( es_settings['host'], es_settings['port'], None )

    def open_spider(self, spider):
        self.es = Elasticsearch([{'host': self.es_host, 'port': self.es_port}])
        if self.index_name == None:
            self.index_name = 'blocket_'+time.strftime("%Y-%m-%d_%X", time.gmtime())
            self.es.indices.create(index=self.index_name)
        else:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name)

    def process_item(self, item, spider):

        # add the document, i.e. item, to index self.index_name
        uid = item['uid']
        del item['uid']
        print("The uid is:", uid)
        self.es.index(index=self.index_name, id=uid, body=item, doc_type="blocket_ad")

        return item

class GoogleMapsPipeline(object):
    # api-key: AIzaSyA9d-hRcRfnfSDzd709zmQJORutp96n9r0
    
    def __init__(self, api_key = None):
        self.api_key = api_key

    @classmethod
    def from_crawler(cls, crawler):
        api_settings = crawler.settings.get('GOOGLEMAPS')

        return cls( api_settings['api_key'])

    def open_spider(self, spider):
        self.gm = googlemaps.Client(key=self.api_key)

    def process_item( self, item, spider ):

        if item['loc_name']:
            geocode = self.gm.geocode(item['loc_name']+', Sweden')
            longlat = geocode[0]['geometry']['location']

            if longlat:
                longlat['lon'] = longlat['lng']
                del longlat['lng']
                item['geo_point'] = longlat

        return item

class UIDcheckPipeline(object):

    def open_spider(self, spider):

        self.uids = set()
        self.f = open("non_unique.txt", "w")

    def process_item(self, item, spider):
        if item['uid'] in self.uids:
            f.write("UID not unique:", item['uid'])

        else:
            self.uids.add(item['uid'])

        return item
