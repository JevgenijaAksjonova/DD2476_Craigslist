import elasticsearch.helpers
from elasticsearch import Elasticsearch
import pprint


host = 'tvesovla.asuscomm.com'
port = 9200

es = Elasticsearch([{'host': host, 'port': port}])


index_name = "reindex_index"
idx_prop = {
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
                    "title" : {
                        "type" : "text"
                        },
                    "location": {
                        "type" : "geo_point"
                        }
                    }
                }
            }
        }

#es.indices.delete(index="test_index")
#es.indices.create(index="test_index", body=idx_prop)

empty_query = {
        "query": {"match_all": {}}
        }

for document in elasticsearch.helpers.scan(es, query=empty_query, index="test_index"):
    pprint.pprint(document)

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
#es.index(index=index_name, id=1, body=item, doc_type="blocket_ad")
#

