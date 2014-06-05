import scipy.sparse
from collections import defaultdict
import pdb

#The following methods are for sparse matrices S
def get_neighbors(S):
    neighbors = defaultdict(list)
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



