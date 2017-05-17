# Script to plot recall or precision dependent on the filtering of the query on rank
# usage: python eval_results.py relevant_uids irrelevant_uids
# The files with uids are line separated _id
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


f_correct = open(sys.argv[1], "r")
f_incorrect = open(sys.argv[2], "r")

correct_ids = [int(line) for line in f_correct]
incorrect_ids = [int(line) for line in f_incorrect]

num_relevant = 100
num_retrieved = len(correct_ids) + len(incorrect_ids)


print(correct_ids)


index = "blocket_new_analyzers_pattern_fix"

correct_docs = get_doc_items( correct_ids, index )
incorrect_docs = get_doc_items( incorrect_ids, index )

lower_bounds = np.linspace(0, 0.8, 17)
top_bounds = np.linspace(1, 2, 21)
print(top_bounds)


l_p = []
l_r = []
for j in range(len(top_bounds)):
    u_p = []
    u_r = []
    for i in range(len(lower_bounds)):

        filtered_correct = [a for a in correct_docs if (a['_source']['title_rank'] > lower_bounds[i] and a['_source']['title_rank'] < top_bounds[j])]
        filtered_incorrect = [a for a in incorrect_docs if (a['_source']['title_rank'] > lower_bounds[i] and a['_source']['title_rank'] < top_bounds[j])]

        filtered_num_retrieved = len(filtered_incorrect) + len(filtered_correct)
        print(filtered_num_retrieved)
        
        u_p.append(len(filtered_correct) / filtered_num_retrieved)
        u_r.append(len(filtered_correct) / num_relevant)

    l_p.append(u_p)
    l_r.append(u_r)


p_array = np.array(l_p)
print(p_array)
r_array = np.array(l_r)

x, y = np.meshgrid(lower_bounds, top_bounds)

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(x, y, r_array)

plt.show()
