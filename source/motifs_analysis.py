#!/usr/bin/env python
# coding: utf-8

# In[18]:


from graph_construction import *
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import netsci.metrics.motifs as nsm
import matplotlib.pyplot as plt
import netsci.visualization as nsv
import copy
import networkx.algorithms.isomorphism as iso
import itertools
from networkx.algorithms import bipartite


# In[19]:


celegans_network = construct_graph()
# graph.display_graph()
# celegans_network.display_graph()


# In[ ]:


# G = nx.from_numpy_matrix(np.matrix(celegans_network.graph), create_using=nx.DiGraph)
# print(G.number_of_nodes())
# G.number_of_edges()


# In[ ]:


# nx.average_clustering(G)


# In[ ]:


# for g in nx.connected_component_subgraphs(G):
#     print(nx.average_shortest_path_length(g))
# print(nx.average_shortest_path_length(G))


# In[ ]:


def erdos_renyi(nodes, edges):
    graph = Graph(nodes)
    edge = 0
    while(edge <= edges):
        source = random.randint(0, nodes-1)
        target = random.randint(0, nodes-1)
        if source != target and graph.graph[source][target] != 1:
            graph.add_edge(source, target, 1)
            edge += 1
    return graph.graph


# In[ ]:


# nodes = G.number_of_nodes()
# edges = G.number_of_edges()
# cc = []
# asl = []
# for i in range(50):
#     random_control = erdos_renyi(nodes, edges)
#     G_ = nx.from_numpy_matrix(np.matrix(random_control), create_using=nx.DiGraph)
#     cc.append(nx.average_clustering(G_))
#     asl.append(nx.average_shortest_path_length(G_))
# print(str(np.mean(cc))+' '+str(np.std(cc)))
# print(str(np.mean(asl))+' '+str(np.std(asl)))


# In[ ]:
def wrong_ffms(graph):
    nodes = len(graph)
    count = 0
    print('here')
    for i in range(nodes):
        for j in range(nodes):
            if i != j and graph[i][j] == 1:
                for k in range(nodes):
                    if k != i and k != j and graph[i][k] == 1 and graph[j][k] == 1:
                        count += 1
    return count

def motif_significance(graph, epochs_1 = 50, index = 6):
    nodes = graph.nodes
    edges = graph.edges
    ffm_main = nsm.motifs(np.array(graph.graph))[index]
#     print(ffm_main)
    motif_count = []
    for epoch_1 in range(epochs_1):
        random_control = erdos_renyi(nodes, edges)
        ffm_count = nsm.motifs(np.array(random_control))[index]
#         print(ffm_count)
        motif_count.append(ffm_count)
    return (ffm_main-np.mean(motif_count))/np.std(motif_count)


# In[ ]:


# graph = copy.deepcopy(celegans_network)
# z_score = motif_significance(graph)
# # print(z_score)


# In[ ]:


class Motif_Tuning:
    
    def add_ffm_connection(self, graph, nodes):
        i = 0
        j = 0
        k = 0
        while(not (i != j and j != k and k != i and graph[i][j] == 1 and graph[j][k] == 1 and graph[i][k] != 1)):
            i = random.randint(0,nodes-1)
            j = random.randint(0, nodes-1)
            k = random.randint(0, nodes-1)
        graph[i][k] = 1
        return graph
        
    def delete_connection(self, graph, nodes):
        i = 0
        j = 0
        while(not (i != j and graph[i][j] == 1)):
            i = random.randint(0,nodes-1)
            j = random.randint(0, nodes-1)
        graph[i][j] = 0
        return graph
    
    def add_connection(self, graph, nodes):
        i = 0
        j = 0
        while(i == j or graph[i][j] == 1):
            i = random.randint(0,nodes-1)
            j = random.randint(0, nodes-1)
        graph[i][j] = 1
        return graph
    
    def delete_ffm_connection(self, graph, nodes):
        i = 0
        j = 0
        k = 0
        while(not (i != j and j != k and k != i and graph[i][j] == 1 and graph[j][k] == 1 and graph[i][k] == 1)):
            i = random.randint(0,nodes-1)
            j = random.randint(0, nodes-1)
            k = random.randint(0, nodes-1)
        graph[i][k] = 0
        return graph
        
    def increase(self, graph, nodes, ffm):
        
        flag_1 = 0
        while(flag_1 == 0):
            graph_ = self.add_ffm_connection(copy.deepcopy(graph), nodes)
            flag_2 = 0
            while(flag_2 == 0):
                graph__ = self.delete_connection(copy.deepcopy(graph_), nodes)
#                 print(nsm.motifs(np.array(graph__))[6])
                graph__nx = nx.from_numpy_matrix(np.matrix(graph__), create_using=nx.DiGraph)
                if nx.is_weakly_connected(graph__nx) and ffm < nsm.motifs(np.array(graph__))[6]:
#                 if nx.is_weakly_connected(graph__nx) and ffm < wrong_ffms(graph__):
                    return graph__
                if nsm.motifs(np.array(graph__))[6] - ffm == 0:
#                 if wrong_ffms(graph__) - ffm == 0:
                    break                                         
                
            
    def decrease(self, graph, nodes, ffm):
        
        flag_1 = 0
        while(flag_1 == 0):
            graph_ = self.delete_ffm_connection(copy.deepcopy(graph), nodes)
            flag_2 = 0
            while(flag_2 == 0):
                graph__ = self.add_connection(copy.deepcopy(graph_), nodes)
                graph__nx = nx.from_numpy_matrix(np.matrix(graph__), create_using=nx.DiGraph)
                if (nx.is_weakly_connected(graph__nx)) and (ffm - nsm.motifs(np.array(graph__))[6]>0):
#                 if (nx.is_weakly_connected(graph__nx)) and (ffm - wrong_ffms(graph__)>0):
                    return graph__
                if (not nx.is_weakly_connected(graph__nx)) or (ffm - nsm.motifs(np.array(graph__))[6]>=0):
                    flag_2 = 1
                    break


# In[ ]:


# tuning = Motif_Tuning()
# graph = celegans_network.graph
# ffm_main = nsm.motifs(np.array(graph))[6]
# print(ffm_main)
# ffm_increase = tuning.decrease(copy.deepcopy(graph), celegans_network.nodes, ffm_main)
# print(nsm.motifs(np.array(ffm_increase))[6])


# In[15]:


def directed_bipartite(graph):
    nodes = len(graph)
    B = nx.Graph()
#     bipartite = Graph(2*nodes)
    left_nodes = range(nodes)
    right_nodes = range(nodes, 2*nodes)
    B.add_nodes_from(left_nodes, bipartite=0)
    B.add_nodes_from(right_nodes, bipartite=1)
    for i in range(nodes):
        for j in range(nodes):
            if graph[i][j] == 1:
                B.add_edges_from([(i, nodes+j)])
    return B


# In[29]:


def get_drivers(graph):
    G = directed_bipartite(graph)
    u = [n for n in G.nodes if G.nodes[n]['bipartite'] == 0]
    matching_edges = nx.bipartite.maximum_matching(G, top_nodes=u)
    nodes = len(graph)
    matching_nodes = []
    for key in matching_edges:
        matching_nodes.append(matching_edges[key])
    count = 0
    for i in range(nodes):
        if i not in matching_nodes:
            count += 1
    return count


# In[ ]:




