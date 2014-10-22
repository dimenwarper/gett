import matplotlib
matplotlib.use('Agg')
import pdb
import argparse
import gett.io_utils
from gett.network_building import confidence
from matplotlib.pylab import *
from collections import defaultdict
from mpl_toolkits.mplot3d import Axes3D

parser = argparse.ArgumentParser()
parser.add_argument('expfile', metavar='EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('communityfile', metavar='COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('--encodefile', metavar='ENCODE_ANNOTATED_FILE', type=argparse.FileType('r'), default=None)
parser.add_argument('--directedcommunityfile', metavar='DIRECTED_COMMUNITY_FILE', type=argparse.FileType('r'), default=None)
parser.add_argument('--sizecutoff', type=int, default=5)
parser.add_argument('outdir', metavar='OUT_DIR', type=str)

args = parser.parse_args()

def normalize_dict(d):
    vals = d.values()
    vals = array(vals)
    mean = vals.mean()
    std = vals.std()
    dn = {}
    """
    for k in d:
        dn[k] = log(d[k])/log(vals.max())
    maxval = max(dn.values())
    minval = min(dn.values())

    #for k, v in dn.iteritems():
    #    dn[k] = (v + 0.5)/maxval
    """
    sorted_vals = sorted(list(set(vals)))
    ref = arange(0, 1, 1./len(sorted_vals))
    for k in d:
        idx = sorted_vals.index(d[k])
        dn[k] = ref[idx]
    return dn

def get_roles(lcs, gcs):
    lc_mean = array(lcs.values()).mean()
    gc_mean = array(gcs.values()).mean()
    lc_mean, gc_mean  = 0.5, 0.5
    roles = {}
    for n, lc in lcs.iteritems():
        gc = gcs[n]
        if lc > lc_mean:
            if gc > gc_mean:
                roles[n] = 'C-hub'
            else:
                roles[n] = 'L-hub'
        else:
            if gc > gc_mean:
                roles[n] = 'S-hub'
            else:
                roles[n] = 'N-hub'
    return roles

s2efile = open('/home/tsuname/resources/hs_symbol2entrez.txt')
symbol2entrez = {}
line = s2efile.readline()
while line:
    f = line.strip().split('\t')
    if len(f) > 1:
	symbol2entrez[f[0]] = f[1]
    line = s2efile.readline()


print 'Parsing expression file'
header, genenames, Mexp = gett.io_utils.read_expression_matrix(args.expfile)
geneids = [symbol2entrez[g] if g in symbol2entrez else 'NA' for g in genenames]
print 'Parsing community file'
nodesbycommunity, communities = gett.io_utils.read_community(args.communityfile)
if args.directedcommunityfile:
    dnodesbycommunity, dcommunities = gett.io_utils.read_community(args.directedcommunityfile)

if args.encodefile:
    print 'Parsing regression file'
    encode_annot_pvals = {'cat1':[], 'cat2':[], 'cat3':[]}
    for line in args.encodefile.readlines():
	if line[0] == '#':
	    continue
	fields = line.strip().split('\t')
	for i, cat in enumerate(['cat1', 'cat2', 'cat3']):
	    encode_annot_pvals[cat].append(float(fields[i+1].split(':')[0]))

commsizes = defaultdict(int)

# Degrees and causality flow statistics
degrees = defaultdict(int)
commdegrees = defaultdict(int)
ntcommdegrees = defaultdict(int)
gcs = defaultdict(int)
lcs = defaultdict(int)
# Maximum intra-modular degrees (mids)
mids = defaultdict(int)
curr_mids = defaultdict(int)
numntcomm = 0.
if args.directedcommunityfile:
    causalflowbynode = defaultdict(int)
    for c, edges in dcommunities.iteritems():
	for n1, n2 in edges:
	    causalflowbynode[n1] -= 1
	    causalflowbynode[n2] += 1
for c, edges in communities.iteritems():
    for n1, n2 in edges:
	curr_mids[n1] = 0.
	curr_mids[n2] = 0.
    for n1, n2 in edges:
	degrees[n1] += 1.
	degrees[n2] += 1.
	curr_mids[n1] += 1. 
	curr_mids[n2] += 1.
    #degrees[n1] /= len(nodesbycommunity[c])
    #degrees[n2] /= len(nodesbycommunity[c])
    #curr_mids[n1] /= len(nodesbycommunity[c])
    #curr_mids[n2] /= len(nodesbycommunity[c])
    for n1, n2 in edges:
	if curr_mids[n1] > mids[n1]:
	    mids[n1] = curr_mids[n1] 
	if curr_mids[n2] > mids[n2]:
	    mids[n2] = curr_mids[n2] 
for c, nodes in nodesbycommunity.iteritems():
    commsizes[len(nodes)] += 1
    for n in nodes:
        commdegrees[n] += 1
    if len(nodes) >= args.sizecutoff:
	for n in nodes:
	    ntcommdegrees[n] += 1
        numntcomm += 1

for n, m in degrees.iteritems():
    lcs[n] = m
    if n not in gcs:
        gcs[n] = 0.

for n, cd in ntcommdegrees.iteritems():
    gcs[n] = float(cd)
    if n not in lcs:
        lcs[n] = 0


lcs = normalize_dict(lcs)
gcs = normalize_dict(gcs)
roles = get_roles(lcs, gcs)

expmeans = defaultdict(int)
for n in commdegrees:
    expmeans[n] = Mexp[n,:].mean()
maxdegree = float(max(degrees.values()))
maxcommdegree = float(max(commdegrees.values()))
maxmid = float(max(mids.values()))

numcomm = float(len(nodesbycommunity))

ncomdegdict = dict([(k,v/numcomm) for k,v in commdegrees.iteritems()])
nntcomdegdict = dict([(k,v/numntcomm) for k,v in ntcommdegrees.iteritems()])
ncomdeg = ncomdegdict.values()
nntcomdeg = nntcomdegdict.values()
#nmids = [mids[n]/maxmid for n in commdegrees]
#ndeg = [degrees[n]/maxdegree for n in commdegrees]
nmids = mids
ndeg = degrees
if args.directedcommunityfile:
    maxcausalflow = float(max([abs(x) for x in causalflowbynode.values()]))

print 'Printing out summary file'
ofile = open(args.outdir + '/summary.txt', 'w')
ofile.write('#Gene symbol\tEntrez id\tLC\tGC\tRole\tNormalized maximum intramodular degree\tNormalized total degree\tNormalized number of communities\tNormalized number of non-trivial communities (size >=%s)\tMean Expression\n' % args.sizecutoff)
for name in sorted(genenames):
    n = genenames.index(name)
    if n in commdegrees:
        id = geneids[n]
        if n in ntcommdegrees: 
            nntcomdeg = nntcomdegdict[n]
        else:
            nntcomdeg = 0
        ofile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (name, id, lcs[n], gcs[n], roles[n], mids[n]/maxmid, degrees[n]/maxdegree, commdegrees[n]/maxcommdegree, nntcomdeg, expmeans[n]))
    else:
        ofile.write('%s\n' % (name))
ofile.close()
    
exit()
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
#ylim(0,1)
#xlim(0,1)
savefig(args.outdir + '/community_vs_degree.png')

clf()
title('Gene intramodular degree vs gene number of communities -- with expression')
r = arange(0,1,0.01)
expmean_array = array([expmeans[n] for n in commdegrees])
X, Y = meshgrid(r,r)
Z = zeros([X.shape[0], X.shape[0]])
for i in xrange(len(ncomdeg)):
    x = ncomdeg[i]
    y = nmids[i]
    z = expmean_array[i]
    xidx = (abs(r - x)).argmin()
    yidx = (abs(r - y)).argmin()
    Z[yidx, xidx] = max(Z[yidx, xidx], z)
levels = arange(Z.min(), Z.max(), 1)
"""
fig = figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X,Y,Z, facecolors=cm.jet(Z))
ax.set_zlabel('Expression')
"""
contour(X,Y,Z, levels=levels)
xlabel('Normalized number of communities')
ylabel('Normalized intramodular degree')
#ylim(0,1)
#xlim(0,1)
savefig(args.outdir + '/community_vs_degree_heatmap.png')

clf()
title('Local/global centrality vs expression')
scatter(ncomdeg, [mids[n] for n in commdegrees], color='r')
xlabel('Normalized community degree')
ylabel('Normalized intramodular degree')
savefig(args.outdir + '/local_vs_global.png')

clf()
title('Local vs global centrality')
scatter([mids[n]/float(cdeg) for n, cdeg in commdegrees.iteritems()], expmean_array, color='r')
xlabel('Normalized community degree')
ylabel('Mean expression')
savefig(args.outdir + '/local_global_vs_expression.png')


clf()
title('Number of genes by community')
logncomm = [log10(k) for k in commsizes.keys()]
loggcomm = [log10(v) for v in commsizes.values()]
scatter(logncomm, loggcomm, color='k')
rx = arange(min(logncomm), max(logncomm))
ry = arange(min(loggcomm), max(loggcomm))
xlabel('Number of genes by community')
ylabel('Number of communities')
xticks(rx, ['$10^{%.2f}$' % i for i in rx])
yticks(ry, ['$10^{%.2f}$' % i for i in ry])
savefig(args.outdir + '/genes_by_communities.png')

# ENCODE annotation p value distributions

if args.encodefile:
    for i, cat in enumerate(['cat1', 'cat2', 'cat3']):
	clf()
	title('RegulomeDB annotation p-value distribution -- Category %s' % (i + 1))
	hist(encode_annot_pvals[cat], 50, normed=True)
	xlabel('P-value')
	ylabel('Normalized count')
	savefig(args.outdir + '/regulomedb_pvals_cat_%s.png' % (i+1))

# Community degrees against causal flow
if args.directedcommunityfile:
    clf()
    title('Community degrees vs causal flow')
    scatter([commdegrees[n]/maxcommdegree for n in causalflowbynode], [x/maxcausalflow for x in causalflowbynode.values()], color='r')
    ylim(-1,1)
    xlim(0,1)
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

