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

class Undirected_WeightedGWU(gwu.GraphWithUpdate,nx.Graph):
    
    def __init__(self,graph = None,**args):
        """ The creator of DiGraphWithUpdate Class """
        nx.Graph.__init__(self,graph,args)
        self.shortest_path_dict = None
        self.max_distance = None
        self.max_strength = None
       
    def add_edge(self,u,v,**args):
        nx.Graph.add_edge(self, u, v, args)
        
        #update info about the network : not really an update but a computation
        if self.shortest_path_dict is not None :
            self.shortest_path_dict = nx.shortest_path_length(self,weight="weight")
        if self.max_distance is not None :
            self.max_distance = max(max(dictionnaire.values()) for dictionnaire in self.get_shortest_path_dict().values())
        if self.max_strength is not None :
            self.max_strength = max(self.degree(weight="weight").values())
        
    def isWeighted(self):
        return True   
    
    def isDirected(self):
        return False   
    
    
 
    def OrigStrength(self) : 
        ''' returns a 2d array containing the  strength = weighted in degree of the origin node for all edges
        '''
        probas = np.dot( 
                      np.array(self.degree(weight="weight").values()).reshape(-1,1),
                      np.ones((1,self.number_of_nodes())))
        return probas
    
    def NormalizedOrigStrength(self) : 
        ''' returns a 2d array containing the  strength of the origin node divide by max of in_strength for all edges
        '''
        if self.get_max_strength() == 0 :
            return np.zeros((self.number_of_nodes(), self.number_of_nodes()))
        return self.OrigStrength()/self.get_max_strength()
    
    
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
    
   
    def TargStrength(self) : 
        ''' returns a 2d array containing the in degree of the target node for all edges
        ''' 
        probas =  np.dot( 
                      np.ones((self.number_of_nodes(),1)),
                      np.array(self.degree(weight="weight").values()).reshape(1,-1)
                      )       
        return probas
    
    def NormalizedTargStrength(self) : 
        ''' returns a 2d array containing the in degree of the target node for all edges divided by max of in_strength
        '''    
        if self.get_max_strength() == 0 :
            return np.zeros((self.number_of_nodes(), self.number_of_nodes()))   
        return self.TargStrength()/self.get_max_strength()
    
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
    
   
    def MaxStrength(self):
        ''' returns a 2d array filled with only one value : the sum of in strengths in the network'''
        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        value = self.get_max_strength()
        probas.fill(value)
        return probas
    
    def AverageStrength(self):
        ''' returns a 2d array filled with only one value : the sum of in strengths in the network'''
        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        value = sum(self.degree(weight="weight").values())/self.number_of_nodes()
        probas.fill(value)
        return probas
    
    def TotalWeight(self):
        ''' returns a 2d array filled with only one value : the sum of strengths of links in the network = size of the network'''
        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        value = self.size(weight="weight")
        probas.fill(value)
        return probas
    
    
    def AverageWeight(self):
        ''' returns a 2d array filled with only one value : the sum of in strengths in the network'''
        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        if self.number_of_edges() == 0 : 
            value = 0
        else :
            value = self.size(weight="weight")/self.number_of_edges()
        probas.fill(value)
        return probas
    
    def MaxWeight(self):
        ''' returns a 2d array filled with only one value : the maximal weight in the network'''
        probas = np.empty((self.number_of_nodes(), self.number_of_nodes()))
        list_of_weights = nx.get_edge_attributes(self, "weight").values()
        if len(list_of_weights) == 0 :
            value = 0
        else :
            value = max(list_of_weights)
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
            self.shortest_path_dict = nx.shortest_path_length(self,weight="weight")
        return self.shortest_path_dict

    def get_max_strength(self):
        ''' returns the maximum of out_strengths, if it does not exist, it computes it'''
        if self.max_strength is None :
            self.max_strength = max(self.degree(weight="weight").values())
        return self.max_strength
    
    def get_max_distance(self):
        if self.max_distance is None :
            self.max_distance = max(max(dictionnaire.values()) for dictionnaire in self.get_shortest_path_dict().values())
        return self.max_distance
    
