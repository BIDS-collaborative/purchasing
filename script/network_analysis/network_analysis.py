# coding: utf-8
import os
import networkx as nx
import matplotlib.pyplot as plt
import cython
import numpy as np
import pandas as pd
from networkx.algorithms import bipartite

# load in merged data
data_path = '../../../UCB_dept_merge.csv'
mergeData = pd.read_csv(data_path)

# cut out unnecessary info on department name
mergeData["department_name"] = mergeData["department_name"].apply(lambda x: x.split()[0])

# just keep department_name and supplier_name
deptSupplier = mergeData[['department_name','supplier_name']]
wanted = deptSupplier.drop_duplicates()

#make a bipartite graph, each edge is a co-occurrence of columns
test = nx.Graph()
test.add_nodes_from(wanted['department_name'], bipartite = 0)
test.add_nodes_from(wanted['supplier_name'], bipartite = 1)
edges = [tuple(x) for x in wanted.values]
test.add_edges_from(edges)

# Graph visualization
nx.draw(test)
plt.show()
plt.savefig("test.png")