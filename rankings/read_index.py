#!/usr/bin/python

from __future__ import print_function
import json, sys, csv, elasticsearch
from elasticsearch import Elasticsearch, helpers

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_all_ads_with_terms(index, doc_type):
    es = Elasticsearch(hosts=["tvesovla.asuscomm.com:9200"], timeout=5000)
    ads = list(helpers.scan(es, index=index, doc_type=doc_type))

    res = {}
    for ad in ads:
        res[ad["_id"]] = ad
        res[ad["_id"]]["ad_text_terms"] = []
        res[ad["_id"]]["title_terms"] = []

    ids = []
    for ad in ads:
        ids.append(ad["_id"])

    terms = es.mtermvectors(index, doc_type, body = {'ids': ids}, fields = "ad_text,title")
    for ad_terms in terms["docs"]:
        id = ad_terms["_id"]

        for term in ad_terms["term_vectors"]["ad_text"]["terms"]:
            res[id]["ad_text_terms"].append(term)

        for term in ad_terms["term_vectors"]["title"]["terms"]:
            res[id]["title_terms"].append(term)

    return res

def matrix_to_csv(filename, matrix):
    with open(filename, "w") as f:
        csvwriter = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in matrix:
            csvwriter.writerow(row)
    eprint("File " + filename + " was generated.")

def process_all_ads(index, doc_type):
    all_ads = get_all_ads_with_terms(index, doc_type)
    eprint("Got " + str(len(all_ads)) + " ads from '" + index + "' index.")

    for term_field in ["ad_text_terms", "title_terms"]:
        ads_file = "ads.csv"
        terms_file = "terms-" + term_field + ".csv"
        atf_file = "ads-terms-frequency-" + term_field + ".csv"

        terms = {}
        for ad_id in all_ads:
            ad = all_ads[ad_id]
            for term in ad[term_field]:
                terms[term] = 1

        unique_terms = terms.keys()
        unique_terms.sort()
        eprint("Unique terms: " + str(len(unique_terms)) + ".")

        ads_matrix = []
        for ad_id in all_ads:
            ad = all_ads[ad_id]
            ads_matrix.append([int(ad["_id"]), int(ad["_source"]["price"])])
        matrix_to_csv(ads_file, ads_matrix)

        terms_matrix = []
        for term in unique_terms:
            terms_matrix.append([term.encode('utf8')])
        matrix_to_csv(terms_file, terms_matrix)

        atf = []
        for ad_id in all_ads:
            ad = all_ads[ad_id]
            row = []
            for term in unique_terms:
                if term in ad[term_field]:
                    row.append(1)
                else:
                    row.append(0)
            atf.append(row)
        matrix_to_csv(atf_file, atf)

index = "blocket_new_anlyzers"
doc_type = "blocket_ad"
process_all_ads(index, doc_type)
