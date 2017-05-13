from elasticsearch import Elasticsearch
import index_iterator

host = "tvesovla.asuscomm.com"
port = 9200
es = Elasticsearch([{'host': host, 'port': port}])

old_name = "blocket_company_ad_test"
new_name = "blocket_reindex_test"
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
ri = index_iterator.reindex_iterator(es,old_name, new_name, idx_prop)

ri.run_reindex()


