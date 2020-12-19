#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd


# In[ ]:


class Graph:
    
    def __init__(self, nodes, directed = False):
        self.nodes = nodes
        self.edges = 0
        self.directed = directed
        self.graph = [[0 for i in range(self.nodes)] for j in range(self.nodes)] 
        
    def add_edge(self, source, target, weight):
#         print(len(self.graph))
#         print(len(self.graph[0]))
          self.graph[source][target] = weight
          self.edges += 1
#         if self.directed == True:
#             self.graph[target][source] = weight
            
    def display_graph(self):
        
        for i in range(self.nodes):
            print(str(i), end = ' ')
            for j in range(self.nodes):
                print(str(self.graph[i][j]), end = ' ')
            print()
        


# In[ ]:


def construct_graph(path_edges = './celegansneural/celegans_277_edge_list.xls', path_names = './celegansneural/celegans_277_edge_list_names.xls'):
    edges = pd.read_excel(path_edges, header = None)
    edge_names = pd.read_excel(path_names, header = None)
    graph = Graph(len(edge_names.index))
    for i in range(len(edges.index)):
        target = edges.loc[i,0]
        source = edges.loc[i,1]
        weight = edges.loc[i,2]
        graph.add_edge(source-1, target-1, weight)
    return graph


# In[ ]:



    

