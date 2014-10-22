import argparse
import gett.io
import pdb
from gett.network_building import clustering
from scipy.sparse import lil_matrix
from matplotlib.pylab import *
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('expfile', metavar='EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('communityfile', metavar='COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('parameterfile', metavar='PARAMETER_FILE', type=argparse.FileType('r'))
parser.add_argument('--k', type=int, default=10, help='Number of clusters in partition')
parser.add_argument('--nsim', type=int, default=1000, help='Number of sampling iterations for MCMC')
parser.add_argument('outfile', metavar='OUT_FILE', type=argparse.FileType('w'))

args = parser.parse_args()

print 'Parsing expression file'
header, genenames, Mexp = gett.io.read_expression_matrix(args.expfile)
print 'Parsing community file'
nodesbycommunity, communities = gett.io.read_community(args.communityfile)
print 'Parsing parameter file'
E, Y = args.parameterfile.readline().strip().split('\t')
alpha = float(args.parameterfile.readline().strip())
E = float(E)
Y = float(Y)


nnodes = len(genenames)
nodes = arange(nnodes)
M = lil_matrix((nnodes, nnodes))
degrees = defaultdict(int)
for c, edges in communities.iteritems():
    for (n1, n2) in edges:
        M[n1, n2] = 1
        degrees[n1] += 0.5
        degrees[n2] += 0.5

# This is too costly, not doable =(
#results = clustering.dense_overlap_community_posterior(M, args.k, n=args.nsim, burn=args.nsim/5, return_metrics=False)
print 'Calculating overlaps'
#C_con, C_sep = clustering.dense_overlap_community_mle_overlaps(E, Y, alpha)
C_con, C_sep = 5, 1
C = zeros([nnodes])
for n in nodes:
    print 'Doing %s' % genenames[n]
    if n not in degrees or degrees[n] < 5:
        continue
    neighbors = []
    for m in nodes:
        if M[n, m] == 1 and n != m:
            neighbors.append(m)
    for n1 in neighbors:
        for n2 in neighbors:
            if M[n1, n2] == 0 and n1 != n2:
                C[n] += 1
    C[n] /= len(neighbors)
    C[n] *= 2

NC = C.max()
C /= C.max()
print 'Plotting'
hist(C, 50, alpha=0.5)
savefig('C_histogram.png', dpi=200)
print 'Writing results to output file'
C_sorted = sorted(C, reverse=True)
sorted_indices = [i[0] for i in sorted(enumerate(C), key=lambda x:x[1], reverse=True)]
args.outfile.write('Dataset has minimum number of clusters %s\n' % NC)
for i, c in enumerate(C_sorted):
    args.outfile.write('%s\t%s\n' % (genenames[sorted_indices[i]], c))
args.outfile.close()
