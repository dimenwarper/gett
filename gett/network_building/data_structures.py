import scipy.sparse
from random import random
from collections import defaultdict
import pdb

#The following methods are for sparse matrices S
def get_neighbors(S):
    neighbors = defaultdict(list)
    if type(S) == list:
        # S is a list of edges
        for i,j in S:
            neighbors[i].append(j)
            neighbors[j].append(i)
    else:
        # S is a sparse matrix
        rows, columns = S.nonzero()
        for i, r in enumerate(rows):
            neighbors[r].append(columns[i])
    return neighbors

def get_edges(S):
    return zip(*S.nonzero())

class SparseGraph(scipy.sparse.dok_matrix):
    def __init__(self, *args, **kwargs):
        super(SparseGraph, self).__init__(*args, **kwargs)
        self.edges = get_edges(self)
        self.neighbors = get_neighbors(self)

    """
    Sample a set of edges with probability prob
    good for spliting the graph into training and test sets
    """
    def sample_edges(self, prob, return_neighbors=False):
        sampled_edges = []
        rest = []
        for i, j in self.edges:
            if random() > prob:
                sampled_edges.append((i,j))
            else:
                rest.append((i,j))
        if return_neighbors:
            return get_neighbors(sampled_edges), get_neighbors(rest)
        return sampled_edges, rest

    def max(self):
        return max(self.values())

    """
    Split set of edges deterministically into a set of size N and len(S.edges) - N
    good for spliting the graph into training and test sets
    """
    def split_edges(self, N, return_neighbors=False):
        sampled_edges = []
        rest = []
        count = 0
        for i, j in self.edges:
            if count < N:
                sampled_edges.append((i,j))
            else:
                rest.append((i,j))
            count += 1
        if return_neighbors:
            return get_neighbors(sampled_edges), get_neighbors(rest)
        return sampled_edges, rest

