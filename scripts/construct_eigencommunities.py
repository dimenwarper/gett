import sys
import pdb
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import squareform
import fastcluster
from optparse import OptionParser
from ett.network_building import tools as ntools
from numpy import *


usage = 'usage: python %prog [options] gene_expression_file community_file output_file'
parser = OptionParser(usage)
parser.add_option('-c', '--clustercutoff', dest='clustercutoff', default=0, type='int', help='Minimum community size to be included')

(options, args) = parser.parse_args()
gexpfile = open(args[0])
communityfile = open(args[1])
eigenexpfile = open(args[2], 'w')
clusterfile = open(args[0] + '.community_clusters', 'w')

print 'Writing sample order file'
header = gexpfile.readline()
"""
for h in header.strip().split('\t'):
    orderfile.write(h + '\n')
orderfile.close()
"""
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
print 'Parsing community file'
clusters = []
nodesbycluster = {}
for line in communityfile.readlines():
    fields = line.strip().split('\t')
    e = (int(fields[1]), int(fields[2]))
    if e[0] != e[1]:
	cluster = float(fields[0])
	clusters.append(cluster)
	if cluster in nodesbycluster:
	    nodesbycluster[cluster].add(e[0])
	    nodesbycluster[cluster].add(e[1])
	else:
	    nodesbycluster[cluster] = set([e[0], e[1]])

clusters = array(clusters)
uc = unique(clusters)
print 'Getting eigencommunities'
for i, c in enumerate(uc):
    #print 'cluster %s of %s' % (i + 1, len(uc))
    indices = array(list(nodesbycluster[c]))
    if len(indices) >= options.clustercutoff:
	clusterfile.write('%s:size:%s\t' % (c, len(indices)) + '\t'.join([geneorder[idx] for idx in indices]) + '\n')
	Mgexpprime = Mgexp[indices,:]
	E = linalg.svd(Mgexpprime)[2][0]
	eigenexpfile.write('%s\t' % c + '\t'.join([str(f) for f in E]) + '\n')
    else:
	#print 'Skipping cluster %s of size %s < %s (cutoff)' % (c, len(indices), options.clustercutoff) 
	pass

eigenexpfile.close()


 
