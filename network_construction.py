import utils
from scipy.stats import stats
from numpy import array
from copy import copy
from operator import itemgetter
from heapq import heappush, heappop
from collections import defaultdict
from itertools import combinations # requires python 2.6+

def correlation_matrix(datatable, thresh): 
    corr_dict = {}
    pval_dict = {}
    corr_mat = []
    for i in range(len(datatable)):
	for j in range(i, len(datatable)):
	    k1 = datatable.keys()[i]
	    k2 = datatable.keys()[j]
	    corr, pval = stats.pearsonr(datatable[k1],\
	                                datatable[k2])
	    corr_dict[(k1,k2)] = corr**thresh
	    corr_dict[(k2,k1)] = corr**thresh
	    pval_dict[(k1,k2)] = pval
	    pval_dict[(k2,k1)] = pval
    for k1 in datatable:
	tmp = []
	for k2 in datatable:
	    tmp.append(corr_dict[(k1,k2)])
	corr_mat.append(tmp)
    return array(corr_mat), corr_dict, pval_dict

def Dc(m,n):
    """partition density"""
    try:
        return m*(m-n+1.0)/(n-2.0)/(n-1.0)
    except ZeroDivisionError: # numerator is "strongly zero"
        return 0.0

class HLC:
    def __init__(self,adj,edges):
        self.adj   = adj
        self.edges = edges
        self.Mfactor  = 2.0 / len(edges)
        self.edge2cid = {}
        self.cid2nodes,self.cid2edges = {},{}
        self.initialize_edges() # every edge in its own comm
        self.D = 0.0 # partition density
    
    def initialize_edges(self):
        for cid,edge in enumerate(self.edges):
            edge = swap(*edge) # just in case
            self.edge2cid[edge] = cid
            self.cid2edges[cid] = set([edge])
            self.cid2nodes[cid] = set( edge )
    
    def merge_comms(self,edge1,edge2):
        cid1,cid2 = self.edge2cid[edge1],self.edge2cid[edge2]
        if cid1 == cid2: # already merged!
            return
        m1,m2 = len(self.cid2edges[cid1]),len(self.cid2edges[cid2])
        n1,n2 = len(self.cid2nodes[cid1]),len(self.cid2nodes[cid2])
        Dc1, Dc2 = Dc(m1,n1), Dc(m2,n2)
        if m2 > m1: # merge smaller into larger
            cid1,cid2 = cid2,cid1
        
        self.cid2edges[cid1] |= self.cid2edges[cid2]
        for e in self.cid2edges[cid2]: # move edges,nodes from cid2 to cid1
            self.cid2nodes[cid1] |= set( e )
            self.edge2cid[e] = cid1
        del self.cid2edges[cid2], self.cid2nodes[cid2]
        
        m,n = len(self.cid2edges[cid1]),len(self.cid2nodes[cid1]) 
        Dc12 = Dc(m,n)
        self.D = self.D + ( Dc12 -Dc1 - Dc2) * self.Mfactor # update partition density
    
    def single_linkage(self,threshold=None):
        """docstring goes here..."""
        print "clustering..."
        self.list_D = [(1.0,0.0)] # list of (S_i,D_i) tuples...
        self.best_D = 0.0
        self.best_S = 1.0 # similarity threshold at best_D
        self.best_P = None # best partition, dict: edge -> cid
        
        H = similarities( self.adj ) # min-heap ordered by 1-s
        S_prev = -1
        for oms,eij_eik in H:
            S = 1-oms # remember, H is a min-heap
            if S < threshold:
                break
                
            if S != S_prev: # update list
                if self.D >= self.best_D: # check PREVIOUS merger, because that's
                    self.best_D = self.D  # the end of the tie
                    self.best_S = S
                    self.best_P = copy(self.edge2cid) # slow...
                self.list_D.append( (S,self.D) )
                S_prev = S
            self.merge_comms( *eij_eik )
        
        self.list_D.append( (0.0,self.list_D[-1][1]) ) # add final val
        if threshold != None:
            return self.edge2cid, self.D
        return self.best_P, self.best_S, self.best_D, self.list_D
    


def similarities(adj, weights={}):
    """Get all the edge similarities. Input dict maps nodes to sets of neighbors.
    Output is a list of decorated edge-pairs, (1-sim,eij,eik), ordered by similarity.
    """
    print "computing similarities..."
    i_adj = dict( (n,adj[n] | set([n])) for n in adj)  # node -> inclusive neighbors
    min_heap = [] # elements are (1-sim,eij,eik)
    for n in adj: # n is the shared node
        if len(adj[n]) > 1:
            for i,j in combinations(adj[n],2): # all unordered pairs of neighbors
                edge_pair = swap( swap(i,n),swap(j,n) )
                inc_ns_i,inc_ns_j = i_adj[i],i_adj[j] # inclusive neighbors
                if weights:
                    w = weights[edge_pair]
                else:
                    w = 1.0
                S = w * len(inc_ns_i&inc_ns_j) / len(inc_ns_i|inc_ns_j) # Jacc similarity...
                heappush( min_heap, (1-S,edge_pair) )
    return [ heappop(min_heap) for i in xrange(len(min_heap)) ] # return ordered edge pairs

def to_adjacency_list(score_dict, thresh=0):
    adj = defaultdict(set)
    for k1,k2 in score_dict:
	if score_dict[(k1,k2)] >= thresh:
	    adj[k1].add(k2)
	    adj[k2].add(k1)
    return adj

