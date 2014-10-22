from numpy import *
import scipy.cluster.hierarchy as sch
from scipy.sparse.extract import find
from scipy.sparse import lil_matrix
import random
import itertools
import log
import pdb

def bootstrap_communities(Mexp, communities, nbootstraps, min_corr=0.5):
    confidence_values = {}
    nsamples = shape(Mexp)[1]
    _random, _int = random.random, int
    for cname, edges in communities.iteritems():
	for e in edges:
	    confidence_values[e] = 0.
    edges = confidence_values.keys()
    for i in xrange(nbootstraps):
	sample_indices = [_int(_random() * nsamples) for i in itertools.repeat(None, nsamples)]
	Mcorr = corrcoef(Mexp[:, sample_indices])
	for e in edges:
	    if Mcorr[e[0], e[1]] >= min_corr:
		confidence_values[e] += 1.
    for e in edges:
	confidence_values[e] /= nbootstraps
    return confidence_values



