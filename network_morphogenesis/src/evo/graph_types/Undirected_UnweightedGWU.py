'''
Created on 5 fevr. 2013

@author: davidfourquet
inspired by Telmo Menezes's work : telmomenezes.com
'''
"""
this class inherits from networkx.DiGraph and GraphWithUpdate. It stores a distance matrix and some global variables about the network. 
It allows us to update them easily instead of computing them many times.
       

"""
import networkx as nx
import numpy as np
import GraphWithUpdate as gwu
import community as com 

class Undirected_UnweightedGWU(gwu.GraphWithUpdate, nx.Graph):
    
    def __init__(self,graph = None):
        """ The creator of UndirectedUnweightedGraphWithUpdate Class """
        
        nx.Graph.__init__(self,graph)
        self.shortest_path_dict = None
        self.max_distance = None
        self.max_degree = None
       
    def add_edge(self,u,v,**args):
        nx.Graph.add_edge(self, u, v, args)
        
        #update info about the network : not really an update but a computation
        if self.shortest_path_dict is not None :
            self.shortest_path_dict = nx.shortest_path_length(self)
        if self.max_distance is not None :
            self.max_distance = max(max(dictionnaire.values()) for dictionnaire in self.get_shortest_path_dict().values())
        if self.max_degree is not None :
            self.max_degree = float(max(self.degree().values()))
        
    def isWeighted(self):
        return False   
    
    def isDirected(self):
        return False 
    
      
    def OrigDegree(self) : 
        ''' returns a 2d array containing the  degree of the origin node for all edges
        '''
        probas = np.dot( 
                        np.array(self.degree().values(),dtype=float).reshape(-1,1),
                        np.ones((1,self.number_of_nodes())))
        return probas
    
    def NormalizedOrigDegree(self) : 
        ''' returns a 2d array containing  degree of origin divided by max of in_degrees 
        '''
        return self.OrigDegree()/self.get_max_degree()
    
    
    def OrigId(self) :
        ''' returns a 2d array containing the identity number (0 to n=number of nodes) of the origin node for all edges
        ''' 
        probas = np.dot( 
                      np.array(range(self.number_of_nodes()),dtype=float).reshape(-1,1),
                      np.ones((1,self.number_of_nodes())))
        return probas
    
    def NormalizedOrigId(self) :
        ''' returns a 2d array containing the identity number (0 to n=number of nodes) of the origin node for all edges divide by the total number of nodes
        ''' 
        
        return self.OrigId()/self.number_of_nodes()
    
    def TargDegree(self) : 
        ''' returns a 2d array containing the in degree of the target node for all edges
        ''' 
        probas =  np.dot( 
                      np.ones((self.number_of_nodes(),1)),
                      np.array(self.degree().values(),dtype=float).reshape(1,-1)
                      )       
        return probas
    
    def NormalizedTargDegree(self) : 
        ''' returns a 2d array containing the in degree of the target node for all edges divided by max of in_degrees
        ''' 
          
        return self.TargDegree()/self.get_max_degree()
    
    def TargId(self) : 
        ''' returns a 2d array containing the identity number of the target node for all edges
        ''' 
        probas =  np.dot( 
                      np.ones((self.number_of_nodes(),1)),
                      np.array(range(self.number_of_nodes()),dtype=float).reshape(1,-1)
                      )               
        return probas
    
    
    
    def NormalizedTargId(self) : 
        ''' returns a 2d array containing the identity number of the target node for all edges divided by the number of nodes
        '''       
        return self.TargId()/self.number_of_nodes()
    #@profile
    def OrigPagerank(self):
        ''' returns a 2d array containing the pagerank of the origin node for all edges
        ''' 
        probas = np.dot( 
                      np.array(nx.pagerank_numpy(self).values(),dtype=float).reshape(-1,1),
                      np.ones((1,self.number_of_nodes())))
        return probas
    
    #@profile
    def TargPagerank(self):
        ''' returns a 2d array containing the pagerank of the target node for all edges
        ''' 
        probas =  np.dot( 
                      np.ones((self.number_of_nodes(),1)),
                      np.array(nx.pagerank_numpy(self).values(),dtype=float).reshape(1,-1)
                      )       
        return probas
    
    #@profile
    def OrigCoreN(self):
        ''' returns a 2d array containing the pagerank of the origin node for all edges
        ''' 
        probas = np.dot( 
                      np.array(nx.core_number(self).values(),dtype=float).reshape(-1,1),
                      np.ones((1,self.number_of_nodes())))
        return probas
    
    #@profile
    def TargCoreN(self):
        ''' returns a 2d array containing the pagerank of the target node for all edges
        ''' 
        probas =  np.dot( 
                      np.ones((self.number_of_nodes(),1)),
                      np.array(nx.core_number(self).values(),dtype=float).reshape(1,-1)
                      )       
        return probas
    
    #@profile
    def OrigCloseness(self):
        ''' returns a 2d array containing the closeness of the origin node for all edges
        ''' 
        probas = np.dot( 
                      np.array(nx.closeness_centrality(self).values(),dtype=float).reshape(-1,1),
                      np.ones((1,self.number_of_nodes())))
        return probas
    
    #@profile
    def TargCloseness(self):
        ''' returns a 2d array containing the closeness of the target node for all edges
        ''' 
        probas =  np.dot( 
                      np.ones((self.number_of_nodes(),1)),
                      np.array(nx.closeness_centrality(self).values(),dtype=float).reshape(1,-1)
                      )       
        return probas
    #@profile
    def OrigBetweenness(self):
        ''' returns a 2d array containing the betweenness of the origin node for all edges
        ''' 
        probas = np.dot( 
                      np.array(nx.betweenness_centrality(self).values(),dtype=float).reshape(-1,1),
                      np.ones((1,self.number_of_nodes())))
        return probas
    
    #@profile
    def TargBetweenness(self):
        ''' returns a 2d array containing the betweenness of the target node for all edges
        ''' 
        probas =  np.dot( 
                      np.ones((self.number_of_nodes(),1)),
                      np.array(nx.betweenness_centrality(self).values(),dtype=float).reshape(1,-1)
                      )       
        return probas
    #@profile
    def OrigClustering(self):
        ''' returns a 2d array containing the clustering of the origin node for all edges
        ''' 
        probas = np.dot( 
                      np.array(nx.clustering(self).values(),dtype=float).reshape(-1,1),
                      np.ones((1,self.number_of_nodes())))
        return probas
    
    #@profile
    def TargClustering(self):
        ''' returns a 2d array containing the clustering of the target node for all edges
        ''' 
        probas =  np.dot( 
                      np.ones((self.number_of_nodes(),1)),
                      np.array(nx.clustering(self).values(),dtype=float).reshape(1,-1)
                      )       
        return probas
    #@profile
    def OrigEccentricity(self):
        ''' returns a 2d array containing the eccentricity of the origin node for all edges
        ''' 
        sp = self.get_shortest_path_dict()
        probas = np.dot( 
                      np.array(nx.eccentricity(self, sp = sp).values(),dtype=float).reshape(-1,1),
                      np.ones((1,self.number_of_nodes())))
        return probas
    
    #@profile
    def TargEccentricity(self):
        ''' returns a 2d array containing the eccentricity of the target node for all edges
        ''' 
        sp = self.get_shortest_path_dict()
        probas =  np.dot( 
                      np.ones((self.number_of_nodes(),1)),
                      np.array(nx.eccentricity(self, sp = sp).values(),dtype=float).reshape(1,-1)
                      )       
        return probas
    #@profile
    def SameCommunity(self) :
        ''' returns a 2d array containing 1 when both nodes are in the same community'''
        partition = com.best_partition(self)
        
        probas = np.zeros((self.number_of_nodes(), self.number_of_nodes()))
        
        for node1 in partition :
            for node2 in partition :
                if partition[node1]==partition[node2] :
                    probas[node1,node2] = 1.
        
        return probas
    
    def Distance(self) :
        ''' returns a 2d array containing the distance = shortest path length, takes weights into account'''
        ''' gives +infinity if no path'''
        
        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        #every path that does not exist has distance +infinity
        probas.fill(float('+inf'))
        
        for node1, row in self.get_shortest_path_dict().iteritems():
            for node2, length in row.iteritems():
                probas[node1, node2] = length 
        return probas

    def NormalizedDistance(self) :
        ''' returns a 2d array containing the distance = shortest path length, takes weights into account'''
        ''' gives +infinity if no path'''
        ''' divides by distance maximal distance which is always real but can be 0 ''' 
        return self.Distance()/self.get_max_distance()

    def NumberOfNodes(self):
        ''' returns a 2d array filled with only one value : the number of nodes of the network'''
        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        value = self.number_of_nodes()
        probas.fill(value)
        return probas
    
    def NumberOfEdges(self):
        ''' returns a 2d array filled with only one value : the number of edges of the network'''
        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        value = self.number_of_edges()
        probas.fill(value)
        return probas
    
    def MaxDegree(self):
        ''' returns a 2d array filled with only one value : the maximal in degree among nodes in the network'''
      
        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        max_degree = self.get_max_degree()
        probas.fill(max_degree)
        return probas
    
    def AverageDegree(self):
        ''' returns a 2d array filled with only one value : the average of  in degrees in teh network'''
        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        value = sum(self.degree().values())/self.number_of_nodes()
        probas.fill(value)
        return probas
    
    
    def MaxDistance(self) :
        ''' returns a 2d array filled with only one value : the max of distances in the network'''

        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        max_distance = self.get_max_distance()
        probas.fill(max_distance)  
        return probas
    
    def AverageDistance(self) :
        ''' returns a 2d array filled with only one value : the average of distances in the network'''
        
        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        shortest_path_dict = self.get_shortest_path_dict()
        number_of_distances = sum(len(dictionnaire.values()) for dictionnaire in shortest_path_dict.values())
        sum_of_distances = sum(sum(dictionnaire.values()) for dictionnaire in shortest_path_dict.values())
        value = sum_of_distances/number_of_distances
        probas.fill(value)  
        return probas
    
    def TotalDistance(self) :
        ''' returns a 2d array filled with only one value : the sum of distances in the network'''
        
        
        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        shortest_path_dict = self.get_shortest_path_dict()
        value = sum(sum(dictionnaire.values()) for dictionnaire in shortest_path_dict.values())
        probas.fill(value)  
        return probas
    
    def Constant(self) :
        ''' returns a 2d array filled with only one value : 1'''
        
        probas = np.ones((self.number_of_nodes(), self.number_of_nodes()))  
        return probas
    
    def Random(self) :
        ''' returns a 2d array filled with only random value between 0 and 1'''
        
        probas = np.random.rand(self.number_of_nodes(), self.number_of_nodes())  
        return probas
    
    def get_shortest_path_dict(self) :
        ''' returns the dict od dict of shortest path lengths, if it does not exist, it creates it'''
        if self.shortest_path_dict is None :
            self.shortest_path_dict = nx.shortest_path_length(self)
        return self.shortest_path_dict
    
    def get_max_degree(self):
        ''' returns the maximum of in_degrees, if it does not exist, it computes it'''
        if self.max_degree is None :
            self.max_degree = max(self.degree().values())
        return self.max_degree 
    
    
    def get_max_distance(self):
        if self.max_distance is None :
            self.max_distance = max(max(dictionnaire.values()) for dictionnaire in self.get_shortest_path_dict().values())
        return self.max_distance
    
    