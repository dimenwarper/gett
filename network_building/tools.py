from numpy import *
import time
import copy
import random as stdrandom
import scipy.cluster.hierarchy as sch
from scipy.sparse.extract import find
from scipy.sparse import lil_matrix
import scipy.stats
import log
import pdb
import numpy as np

"""
Used for medoid and clarans like clusterings; see clarans paper for details
m -- The current medoid
p -- The candidate new medoid
objects -- The objects to cluster
cost -- The cost funciton
"""
def _swap_cost(objects, m, p, assignments, medoids, cost):
    tcmp = 0
    nassignments = [0]*len(objects)
    for j, a in enumerate(assignments):
	if a == m:
	    mincost = float('inf')
	    j2 = -1
	    for m2 in medoids:
		if m2 != m and mincost > cost(objects[m2], objects[j]):
		    j2 = m2
		    mincost = cost(objects[m2], objects[j])
	    if cost(objects[j], objects[p]) >= cost(objects[j], objects[j2]):
		tcmp += cost(objects[j2], objects[j]) - cost(objects[j], objects[m])
		nassignments[j] = j2
	    else:
		tcmp += cost(objects[p], objects[j]) - cost(objects[j], objects[m])
		nassignments[j] = p
	else:
	    if cost(objects[j], objects[a]) > cost(objects[j], objects[p]):
		tcmp += cost(objects[j], objects[p]) - cost(objects[j], objects[a])
		nassignments[j] = p
	    else:
		nassignments[j] = a
    return tcmp, nassignments

def _assign(objects, medoids, cost):
    assgn = [0]*len(objects)
    tcost = 0
    for i, o in enumerate(objects):
	mincost = float('inf')
	for j in medoids:
	    c = cost(o, objects[j])
	    if c < mincost:
		mincost = c
		assgn[i] = j
	tcost += mincost
    return tcost, assgn



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
		    

def kmedoids(objects, k, cost):
    indices = range(len(objects))
    medoids = stdrandom.sample(indices, k)
    currcost, assignments = _assign(objects, medoids, cost)
    for j in medoids:
	change = False
	for i, o in enumerate(objects):
	    totcost = 0
	    for l, a in enumerate(assignments):
		if a == j:
		    totcost += cost(o, objects[l])
		else:
		    totcost += cost(objects[j], objects[l])
	    if currcost > totcost:
		currcost = totcost
		medoids[medoids.index(j)] = i
		for l, a in enumerate(assignments):
		    if a == j:
			assignments[l] = i
		j = i
		change = True
	if not change:
	    break
    return medoids, assignments


def clarans(objects, k, cost, maxneighbor=-1, numlocal=2):
    start = time.clock()
    n = len(objects)
    indices = range(n)
    medoids = stdrandom.sample(indices, k)
    bestmedoids = copy.copy(medoids)
    currcost, assignments = _assign(objects, medoids, cost)
    if maxneighbor < 0:
	maxneighbor = n/50
    i = 1
    j = 1
    mincost = float('inf')
    while i <= numlocal:
	while j <= maxneighbor:
	    m = stdrandom.choice(medoids)
	    p = m
	    while p == m:
		p = stdrandom.choice(indices)
	    sc, nassignments = _swap_cost(objects, m, p, assignments, medoids, cost)
	    if sc < 0:
		medoids[medoids.index(m)] = p
		currcost = currcost + sc
		assignments = nassignments
		j = 1
	    else:
		j += 1
	if mincost > currcost:
            bestmedoids = medoids
	i += 1
    print 'Elapsed %s' % (time.clock() - start)
    return bestmedoids, assignments
        


   
	
def topological_overlap_matrix(M):
    nelems = shape(M)[0]
    res = zeros([nelems, nelems])
    print 'Precomputing N matrix'
    print 'Done precomputing, doing rest of computation'
    for i in range(nelems):
	for j in range(i, nelems):
	    res[i,j] = (dot(M[i,:], M[j,:]) - M[i,j]*M[j,j] - M[i,i]*M[i,j] + M[i,j])/(min(M[i,:].sum(), M[j,:].sum()) + 1)
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
    Mthresh = abs(Mcorr)
    Mthresh[Mthresh < hthresh] = 0
    return Mthresh**sthresh, zip(rows, cols)


def link_communities_dissimilarity(e1, e2, TOM):
    i, k = e1
    j, kprime = e2
    if k == kprime:
	return TOM[i, j]
    elif i == j:
	return TOM[k, kprime]
    elif i == kprime:
	return TOM[k, j]
    elif j == k:
	return TOM[i, kprime]
    else:
	return 0


def link_communities_matrix_by_TOM(M, edges, squareform=False):
    nelems = shape(M)[0]
    nlinks = len(edges)
    if squareform:
	res = zeros(nlinks*(nlinks - 1)/2)
    else:
        res = zeros([nlinks, nlinks])
    log.write_and_close('Calculating TOM matrix')
    TOM = topological_overlap_matrix(abs(M))
    prevprog = -1
    if not squareform:
	for l in range(nlinks):
	    res[l, l] = 1
    for l in range(nlinks):
	prog = int(float(l)/nlinks * 100)
	if (prog % 10 == 0 or l == 0) and prog != prevprog:
	    log.write_and_close('%s %%' % prog)
            prevprog = prog
	for m in range(l + 1, nlinks):
	    if squareform:
		res[nlinks * l - (l*(l+1)/2) + m - l -1] = 1 - abs(link_communities_dissimilarity(edges[l], edges[m], TOM))
	    else:
		res[l, m] = link_communities_dissimilarity(edges[l], edges[m], TOM)
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

def preservation_metric(clusteredges, networkedges, by_edges=False):
    degrees = get_degrees(clusteredges)
    vec1 = degrees.values()
    if by_edges:
	degrees2 = get_degrees([e for e in clusteredges if e in networkedges or (e[1],e[0]) in networkedges])
	vec2 = [degrees2[n] if n in degrees2 else 0 for n in degrees]
    else:
	vec2 = [sum([1 for m in degrees if (n,m) in networkedges or (m,an) in networkedges]) for n in degrees]
    return scipy.stats.pearsonr(vec1, vec2)
	    
def entropy(data, nbins):
    n, bins = histogram(data.ravel(), nbins)
    n = n.astype(float_)
    n = take(n, nonzero(n)[0])         # get the positive
    p = n/data.size
    delta = bins[1]-bins[0]
    S = -1.0*sum(p*np.log(p))
    return S/np.log(data.size + 1)

def graph_entropy(Mweight, nbins, clusteredges=[]):
    if len(clusteredges) > 0:
        return nan #TODO need to consider the case when we specify which edges to take into account
    else:
        return entropy(Mweight, nbins)

