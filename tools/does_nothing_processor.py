# THis processor does nothing


class does_nothing_processor():

    def __init__(self):
        # Here we can define resources used for processing of items from elasticsearch
        pass

    def process(self, doc_item):
        # the method just returns the doc_item

        item = doc_item['_source'] # If you want to modify fields in the document
        doc_id = doc_item['_id'] # the document id
        doc_type = doc_item['_type'] # the document type
        return doc_item

