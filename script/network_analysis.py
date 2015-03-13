
# coding: utf-8

# In[78]:

import os
import networkx as nx
import matplotlib.pyplot as plt
import cython
import numpy as np
import pandas as pd


# In[59]:

# load in merged data
data_path = '../../../UCB_dept_merge.csv'
mergeData = pd.read_csv(data_path)


# In[60]:

# cut out unnecessary info on department name
mergeData["department_name"] = mergeData["department_name"].apply(lambda x: x.split()[0])


# In[71]:

# just keep department_name and supplier_name
deptSupplier = mergeData[['department_name','supplier_name']]


# In[97]:

#keep only the unique values
wanted = deptSupplier.drop_duplicates()


# In[84]:

#try to create graphs
from networkx.algorithms import bipartite


# In[98]:

#make a bipartite graph
test= nx.Graph()
test.add_nodes_from(wanted['department_name'], bipartite = 0)
test.add_nodes_from(wanted['supplier_name'], bipartite = 1)
edges = [tuple(x) for x in wanted.values]
test.add_edges_from(edges)


# In[ ]:

nx.draw(test)
plt.show()
plt.savefig("test.png")


# In[ ]:




# In[ ]:



