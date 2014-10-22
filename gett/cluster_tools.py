import scipy
import pylab
import scipy.cluster.hierarchy as sch

"""
This is essentially due to Steve Tjoa
see his blog/page http://stevetjoa.com/
"""

def show_heatmap(D):
# Compute and plot dendrogram.
    fig = pylab.figure()
    axdendro = fig.add_axes([0.09,0.1,0.2,0.8])
    Y = sch.linkage(D, method='centroid')
    Z = sch.dendrogram(Y, orientation='right')
    axdendro.set_xticks([])
    axdendro.set_yticks([])

# Plot distance matrix.
    axmatrix = fig.add_axes([0.3,0.1,0.6,0.8])
    index = Z['leaves']
    D = D[index,:]
    D = D[:,index]
    im = axmatrix.matshow(D, aspect='auto', origin='lower')
    axmatrix.set_xticks([])
    axmatrix.set_yticks([])

# Plot colorbar.
    axcolor = fig.add_axes([0.91,0.1,0.02,0.8])
    pylab.colorbar(im, cax=axcolor)

# Display and save figure.

