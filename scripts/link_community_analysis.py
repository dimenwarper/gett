import matplotlib
matplotlib.use('Agg')
import scipy.cluster.hierarchy as sch
import fastcluster
import os.path
import sys
import pdb
import argparse
import gett.network_building.tools as ntools
import gett.io
from gett.network_building import log as logger

from scipy.spatial.distance import squareform
from matplotlib.pylab import *

sys.setrecursionlimit(1000000)
parser = argparse.ArgumentParser()
parser.add_argument('expfile', metavar='EXPRESSION_FILE', type=argparse.FileType('r'), help='The gene expression file. Rows are genes, columns are samples. Tab delimited.')
parser.add_argument('--sthresh', type=float, default=1., help='Soft threshold to apply to correlation matrix. Default is 1')
parser.add_argument('--hthresh', type=float, default=0.75, help='Hard threshold to apply to correlation matrix. Default is 0.75')
parser.add_argument('--binarize', dest='binarize', action='store_const', const=True, default=False, help='Binarize the thresholded correlation matrix, setting all non-zero entries to one')	
parser.add_argument('--random', type=bool, default=False, help='Apply random sparsification instead of thresholding. Default is false.')
parser.add_argument('--clustermethod', type=str, default='hierarchical', help='Clustering method. Default is hierarchical.')
parser.add_argument('--k', type=int, default=-1, help='Number of clusters. Ignored if using hierarchical.')
parser.add_argument('--outname', type=str, default='', help='Name to pre-append to output files.')

args = parser.parse_args()
print  'Parsing input file'
samples, genes, M = gett.io.read_expression_matrix(args.expfile, get_rid_of_NAs=True, merge_same_ids=True)
print  'Finished parsing input matrix. Matrix has %s rows and %s columns (number of samples are %s).' % (M.shape[0], M.shape[1], len(samples)) 
print  'Calculating correlation matrix'
Mcorr = corrcoef(M)
print  'Applying soft thresholding %s and hard thresholding %s' % (args.sthresh, args.hthresh)
if not args.random:
    Ms, edges = ntools.threshold(abs(Mcorr), args.sthresh, args.hthresh)
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
edgefile = open('%s%s.edges' % (args.outname, args.expfile.name), 'w')
for i, j in edges:
    edgefile.write('%s\t%s\n' % (genes[i], genes[j]))
edgefile.close()
if args.binarize:
    Ms[Ms != 0] = 1
# Cluster
if args.clustermethod == 'hierarchical':
    print 'Doing hierarchical clustering'
    print  'Building link community matrix'
    D = ntools.link_communities_matrix_by_TOM(Ms, edges, squareform=True)
    del(Ms)
    #for i in range(D.shape[0]):
    #	D[i,i] = 1

    print 'Max similarity %s, mean %s, standard dev %s' % (D.max(), D.mean(), D.std())
    logger.write_and_close('Max similarity %s, mean %s, standard dev %s' % (D.max(), D.mean(), D.std()))
    #Mls = squareform(1 - abs(D))
    Mls = D
    logger.write_and_close('squared the matrix')
    #del(D)
    Z = fastcluster.linkage(Mls, method='single')
    logger.write_and_close('ran linkage')
    #Z = sch.linkage(Mls, method='single')
    maxdistance = Mls.max()
    del(Mls)
    logger.write_and_close('Done clustering, about to choose clusters')

    print  'Choosing cluster by maximum partition density'
    clusts = ntools.choose_clusters_by_partition_density(Z, 0, maxdistance, 0.01*maxdistance, criterion='distance',  edges=edges)
    if len(set(clusts)) == 0:
	print  'Could not maximize partition density! Check dataset manually'
	exit()

else:
    print 'Calculating TOM matrix'
    TOM = ntools.topological_overlap_matrix(Ms)
    del(Ms)
    if args.k < 0:
	args.k = int(sqrt(len(edges)/2))
    print 'k is set to %s' % args.k
    def dissimilarity_fun(e1, e2):
        return 1 - abs(ntools.link_communities_dissimilarity(e1, e2, TOM)) 
    if args.clustermethod == 'kmedoids':
	print 'Doing k-medoids clustering'
	medoids, clusts = ntools.kmedoids(edges, args.k, dissimilarity_fun)
    if args.clustermethod == 'clarans':
	print 'Doing CLARANS clustering'
	medoids, clusts = ntools.clarans(edges, args.k, dissimilarity_fun)

print 'Found %s clusters' % len(set(clusts))
print  'Writing community file'
communityfile = open('%s%s.communities' % (args.outname, args.expfile.name) , 'w')
for i, e in enumerate(edges):
    communityfile.write('%s\t%s\t%s\n' % (clusts[i], e[0], e[1]))
communityfile.close()
