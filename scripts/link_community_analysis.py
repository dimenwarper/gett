import matplotlib
matplotlib.use('Agg')
import scipy.cluster.hierarchy as sch
import fastcluster
from ett.cluster_tools import show_heatmap
import os.path
import sys
import pdb
import argparse
import ett.network_building.tools as ntools
import ett.io
from ett.network_building import log as logger

from scipy.spatial.distance import squareform
from matplotlib.pylab import *

sys.setrecursionlimit(1000000)
parser = argparse.ArgumentParser()
parser.add_argument('expfile', metavar='EXPRESSION_FILE', type=argparse.FileType('r'), help='The gene expression file. Rows are genes, columns are samples. Tab delimited.')
parser.add_argument('--sthresh', type=float, default=1., help='Soft threshold to apply to correlation matrix. Default is 1')
parser.add_argument('--hthresh', type=float, default=0.75, help='Hard threshold to apply to correlation matrix. Default is 0.75')
parser.add_argument('--random', type=bool, default=False, help='Apply random sparsification instead of thresholding. Default is false.')

args = parser.parse_args()
samples, genes, M = ett.io.read_expression_matrix(args.expfile)
print  'Parsing input file'
print  'Finished parsing input matrix'
print  'Calculating correlation matrix'
Mcorr = corrcoef(M)
print  'Applying soft thresholding %s and hard thresholding %s' % (args.sthresh, args.hthresh)
if not args.random:
	Ms, edges = ntools.threshold(Mcorr, args.sthresh, args.hthresh)
else:
    print  'Sampling an O(log(n)) sparsifier'
    gamma = max(log2(3/0.3), log2(shape(M)[0]))**2/3
    Ms, edges = ntools.sampling_sparsifier_Kn(Mcorr, gamma)
    print  'Gamma: %s' % gamma
    print  'Probability pij: %s' % (gamma/nelems)
print  'Number of edges in original matrix: %s' % len(Mcorr)**2
print  'Number of edges in sparsifier: %s' % len(edges)
# To save memory
del(Mcorr)
print 'Writing edge file'
edgefile = open(args.expfile.name + '.edges', 'w')
for i, j in edges:
    edgefile.write('%s\t%s\n' % (genes[i], genes[j]))
edgefile.close()
print  'Building link community matrix'
# Build distance matrix; save on same  Mls variable to save memory
Mls = squareform(1 - abs(ntools.link_communities_matrix_by_TOM(Ms, edges)))
del(Ms)
D = Mls - Mls.min()
Z = fastcluster.linkage(Mls, method='centroid')
maxdistance = Mls.max()
del(Mls)
# Cluster
print  'Choosing cluster by maximum partition density'
clusts = ntools.choose_clusters_by_partition_density(Z, 0, maxdistance, 0.1*maxdistance, criterion='distance',  edges=edges)
if len(set(clusts)) == 0:
    print  'Could not maximize partition density! Check dataset manually'
    exit()
print 'Found %s clusters' % len(set(clusts))
print  'Writing community file'
communityfile = open('%s.communities' % args.expfile.name , 'w')
for i, e in enumerate(edges):
    communityfile.write('%s\t%s\t%s\n' % (clusts[i], e[0], e[1]))
communityfile.close()
