# coding: utf-8

# In[36]:

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite


# In[39]:
# this file is on google drive
df = pd.read_csv('/DATA CLEANED SOC NET ANALYSIS.csv')


# In[53]:

class CleanUp:
    """this class cleans up the dataframe to prepare it for social network analysis"""
    def __init__(self, df):
        #self.df = df
        self.df = df
        
        #do initial cleaning
        self.df['supplier_name'] =  self.df['supplier_name'].str.replace(',', ' ')
        self.df['supplier_name'] =  self.df['supplier_name'].str.replace(' ', '_')
        self.df['department_name_update'] =  self.df['department_name_update'].str.replace(',', ' ')
        self.df['department_name_update'] =  self.df['department_name_update'].str.replace(' ', '_')
        self.df['creation_date'] = self.df['creation_date'].str.replace('00:00:00', '')
        #create seperate year, month, day colums
        self.df['year'] = self.df["creation_date"].apply(lambda x: x[:4])
        self.df['month'] = self.df['creation_date'].apply(lambda x: x[5:7])
        self.df['day'] = self.df['creation_date'].apply(lambda x: x[8:10])
        
        
    def subsetInit(self, year):
        #sebset according to year and remove all obeservations with office max, give
        #something back and alko office supply, these suppliers have too many links
        #and make the data too noisy, and are not of interest for this analysis
        self.df = self.df[self.df['year'] == year]
        self.df = self.df[self.df.supplier_name != 'OFFICE_MAX']
        self.df = self.df[self.df.supplier_name != 'GIVE_SOMETHING_BACK']
        self.df = self.df[self.df.supplier_name != 'ALKO_OFFICE_SUPPLY']
        
    
    def subset(self,month,transType):
        #sebset according to month and transaction type
        self.df = self.df[self.df['month'].isin([month])]
        #self.df = self.df[self.df['day'].isin(day)]
        self.df = self.df[self.df['item_type'].isin([transType])]
        self.df = self.df[['supplier_name','department_name_update']]
        self.df = self.df.drop_duplicates()
        #reindex dataframe
        self.df.index = range(1,len(self.df) + 1)
        return self.df
    

data = CleanUp(df)

#subset parameters, year, month and transaction type, there are four
#transaction types: NonCatalog Product, PunchOut Product, SQ Hosted Product
year = "2013"
month = "05"
transType = "NonCatalog Product"

data.subsetInit(year)

dataCleaned = data.subset(month, transType)




# In[56]:

len(dataCleaned)


# In[67]:

class graphData:
    """this class creates the social network graph, draws it and saves it in a png file and
    conducts centrality, density and clustering calculations"""
    
    def __init__(self, df):
        self.df = df
        #create the graph
        self.G=nx.Graph()
        self.G.add_nodes_from(self.df['department_name_update'], bipartite = 0)
        self.G.add_nodes_from(self.df['supplier_name'], bipartite = 1)
        self.edgeList = [tuple(x) for x in self.df.values]
        self.G.add_edges_from(self.edgeList)

    def draw(self):
        #create node list for suppliers and departments
        nodelistDept = self.df['department_name_update'].tolist()
        nodelistSup = self.df['supplier_name'].tolist()
        #draw the graph
        pos=nx.networkx.spring_layout(self.G)
        nx.draw_networkx_nodes(self.G, pos, nodelist = nodelistDept, node_color = 'r', node_size = 50)
        nx.draw_networkx_nodes(self.G, pos, nodelist = nodelistSup, node_color= 'w', node_size=50)
        nx.draw_networkx_edges(self.G,pos,width=0.5,alpha=0.5)
        nx.draw_networkx_edges(self.G,pos,edgelist=self.edgeList)

        #plt.show()
        plt.savefig('./pic.png')

    def calc(self):
        bottom_nodes, top_nodes = bipartite.sets(self.G)
        GProjected = nx.bipartite.projected_graph(self.G, top_nodes)
        #density
        dens = nx.density(GProjected)
        print "Density: ", dens
        #average clustering
        ave_clus = nx.average_clustering(GProjected)
        print ""
        print "Avererage clustring: ", ave_clus
        #centrality
        cent = nx.betweenness_centrality(GProjected)
        centDf = pd.DataFrame(cent.items(), columns=['actor', 'centrality']).sort(columns="centrality", ascending=False)
        print ""
        print "Centrality"
        print centDf[0:5]   
        
dataGraphed = graphData(dataCleaned)
dataGraphed.draw()
dataGraphed.calc()



