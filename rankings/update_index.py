#!/usr/bin/python

from __future__ import print_function
import json, sys, elasticsearch, csv
from elasticsearch import Elasticsearch, helpers

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def read_values(csv_file):
    res = {}
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        reader.next() # skip header
        for row in reader:
            res[int(row[1])] = float(row[2])

    return res

def ad_field(index, doc_type, field_name, values):
    es = Elasticsearch(hosts=["tvesovla.asuscomm.com:9200"], timeout=5000)
    docs = list(helpers.scan(es, index=index, doc_type=doc_type))

    actions = []
    for doc in docs:
        int_id = int(doc["_id"])
        actions.append({
            '_op_type': 'update', 
            "_id" : doc["_id"],
            "_type" : doc["_type"],
            "_index" : doc["_index"],
            "doc" : {field_name: values[int_id]}
        })

    # print(json.dumps(actions))
    eprint("Will execute " + str(len(actions)) + " actions on index " + index + ".")
    success, failed = helpers.bulk(es, actions, index=index, doc_type=doc_type, refresh=True)
    if success != len(actions):
        eprint("There were some errors.")
        print(failed)
    else:
        eprint("Index updated successfully.")

index = "blocket_new_anlyzers"
doc_type = "blocket_ad"
field = "text_rank"
values_file = "text_rank_svm7.csv"
#field = "title_rank"
#values_file = "title_rank_svm3.csv"

values = read_values(values_file)
eprint("Read " + str(len(values)) + " from file " + values_file + ".")

ad_field(index, doc_type, field, values)
