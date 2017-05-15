import elasticsearch.helpers
import pprint
from elasticsearch import Elasticsearch
import googlemaps


class reindex_iterator:

    def __init__( self, es, old_index_name, new_index_name, index_prop, item_processor ):
        self.es = es
        self.old_index_name = old_index_name
        self.new_index_name = new_index_name
        self.new_index_properties = index_prop
        self.item_processor = item_processor
#        self.loc_dict = {}

        self.f = open("error_file.txt", "w")

        # api-key: AIzaSyA9d-hRcRfnfSDzd709zmQJORutp96n9r0
        #self.gm = googlemaps.Client(key="AIzaSyA9d-hRcRfnfSDzd709zmQJORutp96n9r0")

        if not self.es.indices.exists(index=self.new_index_name):
            self.es.indices.create(index=self.new_index_name, body=self.new_index_properties)


    def run_reindex(self):

        for doc_item in self.get_iterator(self.old_index_name):

            item = doc_item['_source']
            pprint.pprint(item)

            self.es.index(index = self.new_index_name, id = doc_item['_id'], body = item, doc_type = doc_item['_type'])




    def get_iterator(self,index_name):

        empty_query = {
                "query": {"match_all": {}}
                }

        for document_item in elasticsearch.helpers.scan(self.es, query=empty_query, index=index_name):
            
            index = document_item['_index']
            docid = document_item['_id']
            doc_type = document_item['_type']
            item = document_item['_source']

            doc_item = self.item_processor.process(document_item)
#            item = self.process_item(item, docid, doc_type)

            if not doc_item is None:
                yield doc_item 

    def process_item(self, item, docid, doc_type):

        if not self.es.exists(index=self.new_index_name, id=docid, doc_type = doc_type):

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

        else:
            return None

