# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch
import googlemaps
import time
import pickle
import pprint
import re


class CrawlersPipeline(object):
    def process_item(self, item, spider):
        return item

class ElasticsearchPipeline(object):

    def __init__(self, es_settings = {}):

        self.es_host = es_settings['host']
        self.es_port = es_settings['port']
        if 'index_name' in es_settings:
            self.index_name = es_settings['index_name']
        else:
            self.index_name = None
        if 'index_prop' in es_settings:
            self.index_prop = es_settings['index_prop'] 
        else:
            self.index_prop = None

    @classmethod
    def from_crawler(cls, crawler):

        es_settings = crawler.settings.get('ELASTIC_SETTINGS')
        return cls(es_settings)

    def open_spider(self, spider):
        self.es = Elasticsearch([{'host': self.es_host, 'port': self.es_port}])
        if self.index_name == None:
            self.index_name = 'blocket_'+time.strftime("%Y-%m-%d_%X", time.gmtime())
            self.es.indices.create(index=self.index_name, body=self.index_prop)
        else:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name, body=self.index_prop)

    def process_item(self, item, spider):

        # add the document, i.e. item, to index self.index_name
        uid = item['uid']
        del item['uid']
        print("The uid is:", uid)
        self.es.index(index=self.index_name, id=uid, body=item, doc_type="blocket_ad")

        return item

class GoogleMapsPipeline(object):
    # api-key: AIzaSyA9d-hRcRfnfSDzd709zmQJORutp96n9r0
    # TODO : add a geo_shape field aswell
    
    def __init__(self, api_key = None, loc_dict_filename = None):
        self.api_key = api_key
        if loc_dict_filename is None:
            self.loc_dict_filename = 'loc_dict_' + time.strftime("%Y-%m-%d_%X", time.gmtime())
        else:
            self.loc_dict_filename = loc_dict_filename
        self.loc_dict = None

    @classmethod
    def from_crawler(cls, crawler):
        googlemaps_settings= crawler.settings.get('GOOGLEMAPS')
        if 'loc_dict_filename' not in googlemaps_settings:
            googlemaps_settings['loc_dict_filename'] = None

        return cls( googlemaps_settings['api_key'],
                googlemaps_settings['loc_dict_filename'])

    def open_spider(self, spider):
        try:
            self.loc_dict_file = open(self.loc_dict_filename, "rb")
            self.loc_dict = pickle.load(self.loc_dict_file)
            print("#######################################################################\
                    THE LOCATION DICT HAS BEEN OPENED \
                    #############################")
            input()
        except (FileNotFoundError,AttributeError, EOFError, IndexError, ImportError, pickle.UnpicklingError) as e:
            self.loc_dict = {}
            input()
        self.f = open("unknown_locations.txt", "w")

        if self.loc_dict is None:
            self.loc_dict = {}
        
        self.gm = googlemaps.Client(key=self.api_key)

    def close_spider( self, spider):
        self.loc_dict_file = open(self.loc_dict_filename, "wb")
        pickle.dump(self.loc_dict, self.loc_dict_file)

    def process_item( self, item, spider ):

        if 'loc_name' in item:

            if item['loc_name'] in self.loc_dict:
                geocode = self.loc_dict[item['loc_name']]
            else:
                geocode = self.gm.geocode(item['loc_name']+', Sweden')
                self.loc_dict[item['loc_name']] = geocode # Add to dict

            if len(geocode) > 0:
                longlat = geocode[0]['geometry']['location']
            else:
                self.f.write(item['loc_name'] + "\n")
                return None
                
            if 'lng' in longlat: # Convert to format wanted by elasticsearch
                longlat['lon'] = longlat['lng']
                del longlat['lng']

            item['location'] = longlat

        return item


#        if 'loc_name' in item:
#            
#            
#            geocode = self.gm.geocode(item['loc_name']+', Sweden')
#            longlat = geocode[0]['geometry']['location']
#
#            if longlat:
#                longlat['lon'] = longlat['lng']
#                del longlat['lng']
#                item['location'] = longlat
#
#        return item

class GoogleMapsSubstitutePipeline(object):

    def process_item( self, item, spider ):
        geo_point = {
                'lat': 0.0,
                'lon': 0.0
                }

        item['location'] = geo_point
        return item

class FilterPipeline(object):

    def __init__(self):
        self.pattern = re.compile('\d+\s*([kK][rR]|:-)')

    def process_item(self, item, spider):

        if item['ad_text']:
            txt = item['ad_text']
            matches = self.pattern.findall(txt)
            if len(matches) >= 3:
                # If more than 3 price tags in the ad text, skip that ad
                return None
            else:
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
