from numpy import *
import scipy.cluster.hierarchy as sch
from scipy.sparse.extract import find
from scipy.sparse import lil_matrix
import scipy.stats
import log
import pdb


def choose_clusters_by_partition_density(Z, start, end, step, criterion='inconsistent', edges=[]):
    maxdensity = 0
    pickedclusts = []
    for idx in arange(start, end, step):
	C = sch.fcluster(Z, idx, criterion=criterion)
	densities = [0] * len(set(C))
	if len(edges) > 0: 
	    Mc = len(edges)
	else:
	    Mc = len(C)
	for k, c in enumerate(set(C)):
	    mc = float((C == c).sum())
	    if len(edges) > 0:
	        s = set()
		for i in nonzero(C == c)[0]:
		    s.add(edges[i][0])
		    s.add(edges[i][1])
		nc = float(len(s))
	    else:
		nc = mc
	    if nc <= 2:
		densities[k] = 0
	    else:
		densities[k] = 2./Mc*mc*((mc-(nc-1))/((nc-1)*(nc-2)))
	avgdensity = sum(densities)
	print 'Num clusts %s, index %s, density %s' % (len(set(C)), idx, avgdensity)
	if maxdensity < avgdensity:
	    maxdensity = avgdensity
	    pickedclusts = C
    return pickedclusts
		    
	
def topological_overlap_matrix(M):
    nelems = shape(M)[0]
    res = zeros([nelems, nelems])
    print 'Precomputing N matrix'
    N = M != 0
    print 'Done precomputing, doing rest of computation'
    for i in range(nelems):
	for j in range(i, nelems):
	    res[i,j] = (logical_and(N[i,:], N[j,:]).sum() + M[i,j])/(min(N[i,:].sum(), N[j,:].sum()) + 1)
	    res[j,i] = res[i,j]
    return res

def sampling_sparsifier_Kn(M, gamma):
    nelems = shape(M)[0]
    res = zeros([nelems, nelems])
    p = min(1, gamma/nelems)
    edges = []
    for i in range(nelems):
	for j in range(i, nelems):
	    if random.rand() <= p:
		res[i, j] = 1/p*M[i, j]
		res[j, i] = res[i, j]
		edges.append((i,j))
    return res, edges

def threshold(Mcorr, sthresh, hthresh):
    nelems = shape(Mcorr)[0]
    rows, cols, dat = find(Mcorr >= hthresh)
    return abs(Mcorr**sthresh), zip(rows, cols)

def link_communities_matrix_by_TOM(M, edges):
    nelems = shape(M)[0]
    nlinks = len(edges)
    res = zeros([nlinks, nlinks])
    log.write_and_close('Calculating TOM matrix')
    TOM = topological_overlap_matrix(M)
    prevprog = -1
    for l in range(nlinks):
	prog = int(float(l)/nlinks * 100)
	if (prog % 10 == 0 or l == 0) and prog != prevprog:
	    log.write_and_close('%s %%' % prog)
            prevprog = prog
	for m in range(l, nlinks):
	    i, k = edges[l]
	    j, kprime = edges[m]
	    if not kprime == k:
		if j == k:
		    j = kprime
		else:
		    continue
	    res[l, m] = TOM[i, j]
	    res[m, l] = res[l, m]
    return res

def weighted_link_communities_matrix(M, edges):
    nelems = shape(M)[0]
    nlinks = len(edges)
    res = zeros([nlinks, nlinks])
    def A(i, j, M):
        Aij = M[i, j]
	if i == j:
	    Aij += 1/(sum(M[i, :] > 0)) * M[i, :].sum()
	return Aij
    log.write_and_close('pre computing a[] vectors')
    a = {}
    """
    for i, j in edges:
        print count
	a[i] = array([A(i, x, M) for x in range(nelems)])
	a[j] = array([A(j, x, M) for x in range(nelems)])
 """
    prevprog = -1
    for l in range(nlinks):
	prog = int(float(l)/nlinks * 100)
	if (prog % 10 == 0 or l == 0) and prog != prevprog:
	    log.write_and_close('%s %%' % prog)
            prevprog = prog
	for m in range(l, nlinks):
	    i, k = edges[l]
	    j, kprime = edges[m]
	    if not kprime == k:
		if j == k:
		    j = kprime
		else:
		    continue
	    ai = array([A(i, x, M) for x in range(nelems)])
	    aj = array([A(j, x, M) for x in range(nelems)])
	    res[l, m] = dot(ai, aj)/(dot(ai, ai) + dot(aj, aj) - dot(ai, aj))
	    #res[l, m] = dot(a[i], a[j])/(dot(a[i], a[i]) + dot(a[j], a[j]) - dot(a[i], a[j]))
	    res[m, l] = res[l, m]
    return res


def topological_change_trait(Mexp_cases, Mcorr_cases, Mcorr_controls, Mcorr_Madj_controls, conf_val_cases, conf_val_controls, networks_cases):
    genemeans = Mexp_cases.mean(axis=1)
    traits = {}
    for id, net in networks_cases.iteritems():
	dims = shape(Mexp_cases)
	degrees = {}
	for edge in net:
	    for i in range(2):
	        if edge[i] in degrees:
		    degrees[edge[i]] += 1
		else:
		    degrees[edge[i]] = 0 
	maxdeg = 0 
	gene = -1
	for g, deg in degrees.iteritems():
	    if deg > maxdeg:
		maxdeg = deg
		gene = g
	if gene < 0:
	    log.write('Warning: A netwok with no edges was found')
	traits[id] = zeros([dims[1]])
	case_neighbors = []
	for edge in net:
	    if edge[0] == gene:
		case_neighbors.append(edge[1])
	    if edge[1] == gene:
		case_neighbors.append(edge[0])
	control_neighbors = [g for g in Madj_controls[gene,:] if g > 0]
	for n in case_neighbors:
	    denom = sqrt(norm([x - genemeans[gene] for x in Mexp[gene,:]])*norm([y - genemeans[n] for y in Mexp[gene,:]]))
	    sgn = Mcorr_cases[gene, n]/abs(Mcorr_cases[gene, n])
	    for p in range(dims[1]):
		traits[id][p] += conf_val_cases[gene,n] * sgn * (Mexp_cases[gene,p] - genemeans[gene])*(Mexp_cases[n,p] - genemeans[n])/denom
	for n in control_neighbors:
	    denom = sqrt(norm([x - genemeans[gene] for x in Mexp[gene,:]])*norm([y - genemeans[n] for y in Mexp[gene,:]]))
	    sgn = Mcorr_controls[gene, n]/abs(Mcorr_controls[gene, n])
	    for p in range(dims[1]):
		traits[id][p] -= conf_val_controls[gene,n] * sgn * (Mexp_cases[gene,p] - genemeans[gene])*(Mexp_cases[n,p] - genemeans[n])/denom
    return traits

def get_degrees(edges):
    degrees = {}
    for n1, n2 in edges:
	for n in (n1, n2):
	    if n not in degrees:
		degrees[n] = 1
	    else:
		degrees[n] += 1
    return degrees

def preservation_metric(clusteredges, networkedges):
    degrees = get_degrees(clusteredges)
    vec1 = degrees.values()
    vec2 = [sum([1 for m in degrees if (n,m) in networkedges or (m,n) in networkedges]) for n in degrees]
    return scipy.stats.pearsonr(vec1, vec2)
	    
    
