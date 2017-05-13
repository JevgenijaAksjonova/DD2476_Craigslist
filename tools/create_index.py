# This is a small script to reindex some documents, it is pretty basic right now.
# For each item in the index it reindexes it with the same _id into the index specified
# in index_name. Changes to each item can be made within the function process item
# in index_iterator.py

import elasticsearch.helpers
from elasticsearch import Elasticsearch
import pprint
import index_iterator


host = 'tvesovla.asuscomm.com'
port = 9200

es = Elasticsearch([{'host': host, 'port': port}])


old_index_name = "blocket_maps_test"
index_name = "blocket_company_ad_test"
idx_prop = { # Index properties for the new index
        "mappings": {
            "blocket_ad": {
                "properties": {
                    "ad_text": {
                        "type": "text"
                        },
                    "datetime": {
                        "type" : "date"
                        },
                    "price" : {
                        "type" : "long"
                        },
                    "title": {
                        "type": "text",
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
                    }
                }
            }
        }

#es.indices.delete(index=index_name)
#es.indices.create(index=index_name, body=idx_prop)
#
#for doc_item in index_iterator.reindex_iterator(es, index_name=old_index_name):
#
#    item = doc_item['_source']
#    pprint.pprint(item)
#
#    es.index(index = index_name, id = doc_item['_id'], body = item, doc_type = doc_item['_type'])
#
#
#item = {
#        'title': "this is a title",
#        'ad_text': "this is a text",
#        'datetime': "2017-05-10T10:14",
#        'price': 1234,
#        'location':{
#            'lat': 12.34,
#            'lon': 45.67
#            }
#        }
#
#es.index(index="test_index", id=1, body=item, doc_type="blocket_ad")
#

