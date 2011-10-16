from numpy import *

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


def weighted_link_communities_matrix(M, edges):
    nelems = shape(M)[0]
    nlinks = len(edges)
    res = zeros([nlinks, nlinks])
    def A(i, j, M):
        Aij = M[i, j]
	if i == j:
	    Aij += (1/(M[i, :] > 0).sum()) * M[i, :].sum()
	return Aij

    for l in range(nlinks):
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
	    res[m, l] = res[l, m]
    return res
