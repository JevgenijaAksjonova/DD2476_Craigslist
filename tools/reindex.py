from elasticsearch import Elasticsearch
import index_iterator
import does_nothing_processor

host = "tvesovla.asuscomm.com"
port = 9200
es = Elasticsearch([{'host': host, 'port': port}])

#old_name = "blocket_company_ad_test"
old_name = "blocket_new_analyzers"
new_name = "blocket_new_analyzers_url_fix"
idx_prop = { # Index properties for the new index
        "settings": {
            "index.query.default_field": "title_text",
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
                "_all": {
                    "enabled": False
                    },
                "properties": {
                    "ad_text": {
                        "type": "text",
                        "analyzer": "patterns_analyzer",
                        "copy_to": "title_text"
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
                            },
                        "copy_to": "title_text"
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
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 512
                                }
                            }
                        },
                    "title_text": {
                        "type" : "text",
                        "analyzer": "patterns_analyzer"
                        },
                    "text_rank": {
                        "type": "float"
                        },
                    "title_rank": {
                        "type": "float"
                        }
                    }
                }
            }
        }

ri = index_iterator.reindex_iterator(es,old_name, new_name, idx_prop, does_nothing_processor.does_nothing_processor())

ri.run_reindex()


