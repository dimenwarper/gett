import matplotlib
matplotlib.use('Agg')
import scipy.cluster.hierarchy as sch
import fastcluster
import os.path
import sys
import pdb
import argparse
import ett.network_building.tools as ntools
import ett.io
from ett.network_building import log as logger
from operator import itemgetter

from scipy.spatial.distance import squareform
from matplotlib.pylab import *

parser = argparse.ArgumentParser()
parser.add_argument('expfile', metavar='EXPRESSION_FILE', type=argparse.FileType('r'), help='The gene expression file. Rows are genes, columns are samples. Tab delimited.')
parser.add_argument('outprefix', help='Prefix for output files')
parser.add_argument('--nbins', type=int, default=50, help='Number of bins to discretize weights')

args = parser.parse_args()
print  'Parsing gene expression file'
samples, genenames, M = ett.io.read_expression_matrix(args.expfile, get_rid_of_NAs=True, merge_same_ids=True)
print  'Finished parsing input matrix. Matrix has %s rows and %s columns (number of samples are %s).' % (M.shape[0], M.shape[1], len(samples)) 
print  'Calculating correlation matrix'
Mcorr = corrcoef(M)
Mabs = abs(Mcorr)
"""
print  'Applying soft thresholding %s and hard thresholding %s' % (args.sthresh, args.hthresh)
Ms, edges = ntools.threshold(abs(Mcorr), args.sthresh, args.hthresh)
"""
TOM = ntools.topological_overlap_matrix(Mcorr)
Z = fastcluster.linkage(TOM, method='single')
print 'Finished clustering, calculating entropies'
maxdistance = TOM.max()
mean_ents = {}
max_ents = {}
min_ents = {}
sum_ents = {}
collapsed_ents = {}
for i in arange(0, maxdistance, maxdistance/50.):
    clusts = sch.fcluster(Z, i, criterion='distance')
    clustids = set(clusts)
    nclustids = len(clustids)
    if nclustids in mean_ents:
        continue
    print 'Doing for distance %s and %s number of clusters' % (i, nclustids)
    clusts = array(clusts)
    entropies = []
    collapse_vals = []
    for c in clustids:
        I = clusts == c
        entropies.append(ntools.graph_entropy(Mabs[I,:][:,I], args.nbins))
        collapse_vals.append(TOM[I,:][:,I].mean())
    entropies = array(entropies)
    mean_ents[nclustids] = entropies.mean()
    max_ents[nclustids] = entropies.max()
    min_ents[nclustids] = entropies.min()
    sum_ents[nclustids] = entropies.sum()
    collapsed_ents[nclustids] = ntools.entropy(array(collapse_vals), args.nbins)


genesums = {}
for i in xrange(len(genenames)):
    genesums[i] = Mabs[i,:].sum()/2.

sorted_genesums = sorted(genesums.iteritems(), key=itemgetter(1))

max_f = -inf
best_genes = []
ngenes = len(genenames)
for gid, val in sorted_genesums:
    if max_f != -inf:
        f = max_f + val - len(best_genes) + 1
    else:
        f = val - len(best_genes) + 1
    if f > max_f:
        max_f = f
        best_genes.append(gid)

best_gene_file = open(args.outprefix + 'best_genes.txt', 'w')
print 'Best genes were:'
for gid in best_genes:
    print '%s %s %s' % (gid, genenames[gid], genesums[gid])
    best_gene_file.write('%s\t%s\t%s\n' % (gid, genenames[gid], genesums[gid]))

print 'Plotting entropy plots'
clustrange = sorted(mean_ents.keys())
figure(1)
clf()
semilogx(clustrange, [mean_ents[c] for c in clustrange], linewidth=2, marker='o')
xlabel('Number of clusters')
ylabel('Mean entropy')
savefig(args.outprefix + 'mean_entropies_by_clustersize.png')

figure(1)
clf()
semilogx(clustrange, [min_ents[c] for c in clustrange], linewidth=2, marker='o')
xlabel('Number of clusters')
ylabel('Min entropy')
savefig(args.outprefix + 'min_entropies_by_clustersize.png')

figure(1)
clf()
semilogx(clustrange, [max_ents[c] for c in clustrange], linewidth=2, marker='o')
xlabel('Number of clusters')
ylabel('Max entropy')
savefig(args.outprefix + 'max_entropies_by_clustersize.png')

figure(1)
clf()
semilogx(clustrange, [sum_ents[c] for c in clustrange], linewidth=2, marker='o')
xlabel('Number of clusters')
ylabel('Entropy sum')
savefig(args.outprefix + 'sum_entropies_by_clustersize.png')

figure(1)
clf()
semilogx(clustrange, [collapsed_ents[c] for c in clustrange], linewidth=2, marker='o')
xlabel('Number of clusters')
ylabel('Collapsed entropies')
savefig(args.outprefix + 'collapsed_entropies_by_clustersize.png')
