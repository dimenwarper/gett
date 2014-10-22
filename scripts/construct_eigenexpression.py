import sys
import pdb
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import squareform
import fastcluster
from optparse import OptionParser
from gett.network_building import tools as ntools
from numpy import *


usage = 'usage: python %prog [options] gene_expression_file sample_order_file  output_file'
parser = OptionParser(usage)
parser.add_option('-s', '--soft', dest='softth', default=1, type='float', help='Soft threshold to apply to correlation matrix')
parser.add_option('-t', '--hard', dest='hardth', default=0, type='float', help='Hard threshold to apply to correlation matrix')

(options, args) = parser.parse_args()
gexpfile = open(args[0])
orderfile = open(args[1], 'w')
eigenexpfile = open(args[2], 'w')
clusterfile = open(args[1] + '.clusters', 'w')

print 'Writing sample order file'
header = gexpfile.readline()
for h in header.strip().split('\t'):
    orderfile.write(h + '\n')
orderfile.close()
print 'Parsing gene expression matrix'
line = gexpfile.readline()
geneorder = []
Mgexp = []
while line:
    fields = line.strip().split('\t')
    Mgexp.append([float(expval) for expval in fields[1:]])
    geneorder.append(fields[0])
    line = gexpfile.readline()

Mgexp = array(Mgexp)
print 'Calculating correlation matrix'
Mcorr = abs(corrcoef(Mgexp)**options.softth) - options.hardth

print 'Creating distance matrix from topological overlap matrix'
D = abs(1 - ntools.topological_overlap_matrix(Mcorr))
print 'Clustering'
Z = fastcluster.linkage(D, method='centroid')

print 'Choosing clusters'
clusts = []
midlen = 0
R =  arange(0, 2.2, 0.01)
for idx in R:
    clusts.append(sch.fcluster(Z, idx))
    midlen += len(set(clusts[-1]))
    print 'Found %s clusters for level %s' % (len(set(clusts[-1])), idx)

midlen /= len(R)
print 'Threshold to pick clusters %s' % midlen
print 'Picking clusters'
for c in clusts:
    if len(set(c)) <= midlen:
	pickedclusts = c
	break
print 'Choosing %s clusters' % len(set(pickedclusts))

visitedclusts = []
print 'Getting eigengenes'
for i, c in enumerate(set(pickedclusts)):
    print 'cluster %s of %s' % (i + 1, len(set(pickedclusts)))
    if c not in visitedclusts:
	visitedclusts.append(c)
	indices = [i for i, v in enumerate(pickedclusts) if v == c]
	clusterfile.write('\t'.join([geneorder[idx] for idx in indices]) + '\n')
	Mgexpprime = Mgexp[indices,:]
	E = linalg.svd(Mgexpprime)[2][0]
	eigenexpfile.write('\t'.join([str(f) for f in E]) + '\n')

eigenexpfile.close()


    
