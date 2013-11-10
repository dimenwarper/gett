from matplotlib.pylab import *
import scipy.stats
import pdb

def parcorr(y, x, z):
    wx = lstsq(z, x)[0]   
    wy = lstsq(z, y)[0]   
    y = y - dot(z, wy)
    x = x - dot(z, wx)
    return dot(x, y)/sqrt(dot(y, y)*dot(x, x))


def direct_edges(Mexp, edges, Mgen, restrict_snps=[]):
    nsamples, nsnps = shape(Mgen)
    diredges = set()
    P = scipy.stats.norm.pdf
    if len(restrict_snps) == 0:
	snps = range(nsnps)
    else:
	snps = restrict_snps
    # The likelihood functions are defined the probabilities of the z transforms
    # of the partial correlations following a standard normal distribution in each case where g1 -> g2
    # and g2 -> g1. We take the log likelihood ratio to perform a likelihood ratio test.
    for (g1, g2) in edges:
	l_g1_g2 = 0
	l_g2_g1 = 0
        for i in snps[:500]:
            if True or i < Mgen.shape[1]:
		l_g1_g2 += log(P(arctanh(parcorr(Mexp[g2, :], Mgen[:, i], array([Mexp[g1, :]]).T))))
		l_g2_g1 += log(P(arctanh(parcorr(Mexp[g1, :], Mgen[:, i], array([Mexp[g2, :]]).T))))
	# Right now, just take the log ratios and compare them. Rigorously, the ratio follows
	# a chi squared statistic and we could report causality with confidence.
	if (l_g1_g2 - l_g2_g1) < 0:
	    diredges.add((g2, g1))
	else:
	    diredges.add((g1, g2))
    return diredges
