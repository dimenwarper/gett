from matplotlib.pylab import *
import scipy.stats
import random
import operator
from gett.settings import *
from gett.aux.fisher import fisher_exact
import pdb
def significance_by_enrichment(nodesbycluster, allnodes, taggednodes, cutoff=0.05, apply_bonferroni=False, size_cutoff=1):
    sigvals = {}
    numtests = len([1 for k, v in nodesbycluster.iteritems() if len(v) >= size_cutoff])
    true_cutoff = cutoff
    if apply_bonferroni:
	true_cutoff = cutoff/numtests
    for cluster, nodes in nodesbycluster.iteritems():
        if len(nodes) >= size_cutoff:
	    in_cluster_selected = len([n for n in nodes if n in taggednodes])
	    not_in_cluster_selected = len(taggednodes) - in_cluster_selected
	    not_in_cluster_not_selected = len(allnodes) - len(nodes) - not_in_cluster_selected
	    in_cluster_not_selected = len(nodes) - in_cluster_selected
	    table = [[in_cluster_selected, not_in_cluster_selected], \
		   [in_cluster_not_selected, not_in_cluster_not_selected]]
            #if 0 in (in_cluster_selected, not_in_cluster_selected, in_cluster_not_selected, not_in_cluster_not_selected):
		#sigvals[cluster] = 0
	    oddsratio, pval = fisher_exact(table)
	    if isnan(pval):
		tmp = table[0][1]
		table[0][1] = table[0][0]
		table[0][0] = tmp
		tmp = table[1][1]
		table[1][1] = table[1][0]
		table[1][0] = tmp
		oddsratio, pval = fisher_exact(table)
	    if pval <= true_cutoff:
		sigvals[cluster] = pval
    return sorted(sigvals.iteritems(), key=operator.itemgetter(1))


def all_OMIM_genes(omim_file=MIM2GENE_FILE):
    mim2gene = open(omim_file)
    line = mim2gene.readline()
    omim_genes = []
    while line:
	if line[0] == '#':
	    continue
	fields = line.strip().split('\t')
	if fields[1] == 'gene':
	    omim_genes.append(fields[3])
	line = mim2gene.readline()
    return omim_genes

def tag_by_genenames(nodes, genenamedict, genenames):
    return [n for n in nodes if genenamedict[n] in genenames]

def tag_by_differential_expression(Mexp1, Mexp2, cutoff=0.05, apply_bonferroni=True):
    dim = shape(Mexp1)[0]
    if apply_bonferroni:
	true_cutoff = cutoff/dim
    else:
	true_cutoff = cutoff
    return [n for n in range(dim) if scipy.stats.mannwhitneyu(Mexp1[n,:], Mexp2[n,:])[1] <= true_cutoff]

def significance_by_randomiziation(allnodes, alledges, nodesbycluster, edgesbycluster, cluster_fun, \
                                   nrand=700, cutoff=0.05, apply_bonferroni=True, compare=lambda x,y: x > y, size_cutoff=1, by_edges=False, debug=False):
    true_cutoff = cutoff
    numtests = len([1 for k, v in nodesbycluster.iteritems() if len(v) >= size_cutoff])
    res = []
    if apply_bonferroni:
	true_cutoff /= numtests
    for c, edges in edgesbycluster.iteritems():
	count = 0.
	measure = cluster_fun(edges)
	if len(nodesbycluster[c]) < size_cutoff or isnan(measure):
	    continue
	for i in xrange(nrand):
	    if by_edges:
		randclust = random.sample(alledges, len(edgesbycluster[c]))
            else:
		randnodes = random.sample(allnodes, len(nodesbycluster[c]))
		randclust = [e for e in alledges if e[0] in randnodes or e[1] in randnodes]
	    randmeas = cluster_fun(randclust)
	    if compare(randmeas, measure):
		count += 1.
	if debug:
	    print [c, count, count/nrand]
	if count/nrand <= true_cutoff:
	    res.append([c, count/nrand])
    return res

def SAM_d(Mexp1, Mexp2):
    dims1 = shape(Mexp1)
    dims2 = shape(Mexp2)
    a = (1./dims1[1] + 1./dims2[1])/(dims1[1] + dims2[1] - 2)
    samd = zeros(dims1[0])
    for i in range(dims1[0]):
	numerator = Mexp1[i,:].mean() - Mexp2[i,:].mean()
	s0 = 3.3 # Warning and TODO! need to substitute with computation that minimizes coefficient of variation
	denominator = sqrt(Mexp1[i,:].std()**2 + Mexp2[i,:].std()**2 + s0)
	samd[i] = numerator/denominator
    return samd
    
