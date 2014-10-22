from matplotlib.pylab import *
import gett.io_utils

def community_report(names, comm_vectors, weight_matrices=None, trait_names=None):
    print 'Writing community report'
    for i in xrange(len(names)):
        gett.io_utils.write_communities(open('%s.communities' % (names[i]), 'w'), comm_vectors[i])
    
    if weight_matrices is not None:
        network_report(names, weight_matrices, trait_names=trait_names)

def network_report(names, weight_matrices, trait_names=None):
    print 'Writing network report'
    for i in xrange(len(names)):
        gett.io_utils.write_edges(open('%s.edges' % (names[i]), 'w'), weight_matrices[i])
        if trait_names is not None:
            gett.io_utils.write_edges(open('%s.edges_named' % (names[i]), 'w'), weight_matrices[i], names=trait_names)
