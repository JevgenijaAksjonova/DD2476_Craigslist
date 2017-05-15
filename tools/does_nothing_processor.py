# THis processor does nothing


class does_nothing_processor():

    def __init__(self):
        # Here we can define resources used for processing of items from elasticsearch
        pass

    def process(self, doc_item):
        # the method just returns the doc_item
        return doc_item

