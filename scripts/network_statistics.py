import matplotlib
matplotlib.use('Agg')
import pdb
import argparse
import ett.io
from ett.network_building import confidence
from matplotlib.pylab import *
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('expfile', metavar='EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('communityfile', metavar='COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('directedcommunityfile', metavar='DIRECTED_COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('outdir', metavar='OUT_DIR', type=str)

args = parser.parse_args()

print 'Parsing expression file'
header, genenames, Mexp = ett.io.read_expression_matrix(args.expfile)
print 'Parsing community file'
nodesbycommunity, communities = ett.io.read_community(args.communityfile)
dnodesbycommunity, dcommunities = ett.io.read_community(args.directedcommunityfile)

commsizes = defaultdict(int)

# Degrees and causality flow statistics
causalflowbynode = defaultdict(int)
degrees = defaultdict(int)
commdegrees = defaultdict(int)
for c, edges in dcommunities.iteritems():
    for n1, n2 in edges:
	causalflowbynode[n1] -= 1
	causalflowbynode[n2] += 1
for c, edges in communities.iteritems():
    for n1, n2 in edges:
	degrees[n1] += 1
	degrees[n2] += 1
for c, nodes in nodesbycommunity.iteritems():
    commsizes[len(nodes)] += 1
    for n in nodes:
	commdegrees[n] += 1

maxdegree = float(max(degrees.values()))
maxcausalflow = float(max([abs(x) for x in causalflowbynode.values()]))
maxcommdegree = float(max(commdegrees.values()))

figure(1)
# Degree decay graphs
clf()
title('Node degree decay')
scatter(range(len(degrees)), sorted(degrees.values(), reverse=True), color='b')
xlabel('Nodes')
ylabel('Degrees')
savefig(args.outdir + '/degree_decay.png')

clf()
title('Community degree decay')
scatter(range(len(commdegrees)), sorted(commdegrees.values(), reverse=True), color='g')
xlabel('Nodes')
ylabel('Number of communities')
savefig(args.outdir + '/community_degree_decay.png')

clf()
title('Gene number of edges vs gene number of communities')
scatter([x/maxcommdegree for x in commdegrees.values()], [degrees[n]/maxdegree for n in commdegrees], color='r')
xlabel('Normalized number of communities')
ylabel('Normalized number of edges')
savefig(args.outdir + '/community_vs_degree.png')

clf()
title('Number of genes by community')
scatter([log(k) for k in commsizes.keys()], [log(v) for v in commsizes.values()], color='k')
xlabel('Number of genes by community')
ylabel('Number of communities')
savefig(args.outdir + '/genes_by_communities.png')



# Community degrees against causal flow
clf()
title('Community degrees vs causal flow')
scatter([commdegrees[n]/maxcommdegree for n in causalflowbynode], [x/maxcausalflow for x in causalflowbynode.values()], color='r')
xlabel('Number of communities')
ylabel('Normalized causal flow')
savefig(args.outdir + '/community_vs_causal.png')

# Expression statisics
clf()
title('Expression levels and communities')
scatter([x/maxcommdegree for x in commdegrees.values()], [Mexp[n,:].mean() for n in commdegrees], color='r')
xlabel('Normalized number of communities')
ylabel('Mean expression')
savefig(args.outdir + '/community_vs_mean_expression.png')

clf()
title('Expression variability and communities')
scatter([x/maxcommdegree for x in commdegrees.values()], [Mexp[n,:].std()**2 for n in commdegrees], color='b')
xlabel('Normalized number of communities')
ylabel('Expresion variance')
savefig(args.outdir + '/community_vs_expression_variance.png')

clf()
title('Mean expression histogram')
hist([Mexp[n,:].mean() for n in commdegrees], 40, color='r')
savefig(args.outdir + '/mean_expression_histogram.png')

clf()
title('Expression variance histogram')
hist([Mexp[n,:].std()**2 for n in commdegrees], 40, color='b')
savefig(args.outdir + '/expression_variance_histogram.png')
