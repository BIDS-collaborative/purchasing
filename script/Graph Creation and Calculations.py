#NETWORK X DATA CLEANING AND EXPORT
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite

"""
read in cleaned up data, cleaned up data saved in temp.csv
"""
dataOrig = pd.read_csv('../temp.csv')

"""
clean up data for network analysis, remove "," and replace spaces with "_", remove
extranous data from creation date
"""
dataOrig['supplier_name'] =  dataOrig['supplier_name'].str.replace(',', ' ')
dataOrig['supplier_name'] =  dataOrig['supplier_name'].str.replace(' ', '_')
dataOrig['department_name_update'] =  dataOrig['department_name_update'].str.replace(',', ' ')
dataOrig['department_name_update'] =  dataOrig['department_name_update'].str.replace(' ', '_')
dataOrig['creation_date'] = dataOrig['creation_date'].str.replace('00:00:00', '')

"""
create seperate year, month, day colums
"""
dataOrig['year'] = dataOrig["creation_date"].apply(lambda x: x[:4])
dataOrig['month'] = dataOrig['creation_date'].apply(lambda x: x[5:7])
dataOrig['day'] = dataOrig['creation_date'].apply(lambda x: x[8:10])


"""
Subset data, use only variables of interest and remove suppliers that
create noise in data, including office max, give something back and alko office supplies
"""
#data = data[['creation_date', 'supplier_name','item_type','org_level_3']]
dataOrigSubset = dataOrig[[ 'supplier_name','department_name_update','item_type','year','month','day']]
#subsetting by element in row, subset data for year only, drop all 2104
#data = data[data['year'] == '2013']
dataOrigSubset = dataOrigSubset[dataOrigSubset['year'] == '2013']
dataOrigSubset = dataOrigSubset[dataOrigSubset.supplier_name != 'OFFICE_MAX']
dataOrigSubset = dataOrigSubset[dataOrigSubset.supplier_name != 'GIVE_SOMETHING_BACK']
dataOrigSubset = dataOrigSubset[dataOrigSubset.supplier_name != 'ALKO_OFFICE_SUPPLY']



"""
Make the graph, this graph is first 21 days in march, 2013
"""
day = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21']
dataToGraph = dataOrigSubset[dataOrigSubset['month'].isin(['03'])]
dataToGraph = dataToGraph[dataToGraph['day'].isin(day)]
#dataToGraph = dataToGraph[dataToGraph['item_type'].isin(['PunchOut Product'])]
dataToGraph = dataToGraph[dataToGraph['item_type'].isin(['NonCatalog Product'])]
dataToGraph = dataToGraph[['supplier_name','department_name_update']]
dataToGraph = dataToGraph.drop_duplicates()
#reindex dataframe
dataToGraph.index = range(1,len(dataToGraph) + 1)


"""
The graph that is created for this dataset is a two-mode (or bipartite) graph,
it is two-mode because it has two actors - department and supplier
"""
G = nx.Graph()
G.add_nodes_from(dataToGraph['department_name_update'], bipartite = 0)
G.add_nodes_from(dataToGraph['supplier_name'], bipartite = 1)
edgeList = [tuple(x) for x in dataToGraph.values]
G.add_edges_from(edgeList)

"""
For visualization, need to draw a graph where department and suppliers
are two different colors, here the departments are red and the suppliers
are white, node size is the same
"""
nodelistDept = dataToGraph['department_name_update'].tolist()
nodelistSup = dataToGraph['supplier_name'].tolist()
pos=nx.networkx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, nodelist = nodelistDept, node_color = 'r', node_size = 30)
nx.draw_networkx_nodes(G, pos, nodelist = nodelistSup, node_color= 'w', node_size=30)
nx.draw_networkx_edges(G,pos,width=0.5,alpha=0.5)
nx.draw_networkx_edges(G,pos,edgelist=edgeList)

#plt.show()
plt.savefig('.../2013MarchD21.png')


"""
Calculations, density, average clustering, centality and pearson correlation,
before doing any calculations, the graph must be transformed from a bipartite
graph into a unimodal graph (where actors are all the same type)
"""
bottom_nodes, top_nodes = bipartite.sets(G)
GProjected = nx.bipartite.projected_graph(G, top_nodes)
#density
dens = nx.density(GProjected)
#average clustering
ave_clus = nx.average_clustering(GProjected)
print "avererage clustring: ", ave_clus
#centrality
cent = nx.betweenness_centrality(GProjected)
centDf = pd.DataFrame(cent.items(), columns=['actor', 'centrality']).sort(columns="centrality", ascending=False)
print "centrality"
print centDf[0:10]
#pearson correlation
pears_corr = nx.degree_pearson_correlation_coefficient(GProjected)
print "pearson correlation"
