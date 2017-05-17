import math
import sys
from elasticsearch import Elasticsearch

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


host = 'tvesovla.asuscomm.com'
port = 9200
es = Elasticsearch([{'host': host, 'port': port}])

def get_doc_items( uids, index ):

    return [es.get(index=index, id = uid) for uid in uids]


f= open(sys.argv[1], "r")

ids = [int(line) for line in f]

index = "blocket_new_analyzers_pattern_fix"
doc_items = get_doc_items(ids, index)


output_f = open(sys.argv[1] + ".csv", 'w')

for di in doc_items:
    item = di['_source']

    output_f.write(di['_id']+",")
    output_f.write(str(item['price'])+ ",")
    output_f.write(str(item['title_rank'])+ ",")
    output_f.write(str(item['text_rank']))

    output_f.write("\n")



