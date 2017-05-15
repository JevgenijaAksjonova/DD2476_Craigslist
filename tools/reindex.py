from elasticsearch import Elasticsearch
import index_iterator
import does_nothing_processor

host = "tvesovla.asuscomm.com"
port = 9200
es = Elasticsearch([{'host': host, 'port': port}])

#old_name = "blocket_company_ad_test"
old_name = "blocket_reindex_test"
new_name = "blocket_reindex_test_with_new_tokenizers"
idx_prop = { # Index properties for the new index
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
                        "fields": {
                            "filtered": {
                                "type": "text",
                                "analyzer": "patterns_analyzer"
                                }
                            }
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
                                },
                            "filtered": {
                                "type": "text",
                                "analyzer": "patterns_analyzer"
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

ri = index_iterator.reindex_iterator(es,old_name, new_name, idx_prop, does_nothing_processor.does_nothing_processor())

ri.run_reindex()


