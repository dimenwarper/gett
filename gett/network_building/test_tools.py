import tools
from matplotlib.pylab import *

M = randn(10,10)
Mcorr = corrcoef(M)
matshow(M)
savefig('M.png')
clf()
matshow(Mcorr)
savefig('Mcorr.png')

Ms, edges = tools.sampling_sparsifier_Kn(Mcorr, log(10))
clf()
matshow(Ms)
savefig('Ms.png')
print 'Edges (%s) %s' % (len(edges), edges)

Mls = tools.weighted_link_communities_matrix(Ms, edges)
clf()
matshow(Mls)
savefig('Mls.png')
