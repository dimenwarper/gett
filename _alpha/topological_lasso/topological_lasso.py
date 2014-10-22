"""
Simple "glue code" to call the glasso or JGL R packages
and the bigclam program from the SNAP package
"""
from matplotlib.pylab import *
import rpy2.robjects as robjects
import gett.io
import os
import argparse
import pickle
import pdb

parser = argparse.ArgumentParser()
parser.add_argument('ncomm', metavar='N_COMMUNITIES', type=int, help='Number of sampling iterations for bootstrap')
parser.add_argument('expfile', metavar='EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('--corrthresh', metavar='CORRELATION_THRES', type=float, default=0.)
parser.add_argument('--edgefile', metavar='EDGE_FILE', type=argparse.FileType('r'), default=None)
parser.add_argument('--maxiter', metavar='MAX_ITER', type=int, default=10)
parser.add_argument('--method', metavar='METHOD', type=str, default='jgl')

args = parser.parse_args()

print 'Parsing expression file'
header, genenames, Mexp = gett.io.read_expression_matrix(args.expfile)

if args.edgefile != None:
    print 'Parsing edge file'
    edges = [[genenames.index(x) for x in l.strip().split('\t')] for l in args.edgefile.readlines() if l.strip().split('\t')[0] != l.strip().split('\t')[1]]

    Sigma = zeros([len(genenames), len(genenames)])
    for n1, n2 in edges:
        Sigma[n1,n2] = 1
        Sigma[n2,n1] = 1
else:
    Sigma = cov(Mexp)


robjects.r('library(glasso)')
robjects.r('library(JGL)')
glasso = robjects.r.glasso
JGL = robjects.r.JGL

# Get communities with BIGCLAM
def get_community_associations(Sigma, ncomm, D=None, F=None):
    nvars = Sigma.shape[0]
    if D == None:
        D = zeros([nvars, nvars])
    if F == None:
        F = zeros([nvars, ncomm])
    edges = []
    print 'Getting edges from covariance matrix'
    I = where(Sigma != 0)
    for i in xrange(len(I[0])):
        edges.append((I[0][i], I[1][i]))
    """
    for i in xrange(Sigma.shape[0]):
        for j in xrange(Sigma.shape[1]):
            if Sigma[i,j] != 0:
                edges.append((i,j))
    """
    print 'Writing edges'
    tmpfile = open('edges_tmp.txt', 'w')
    for n1, n2 in edges:
        tmpfile.write('%s\t%s\n' % (n1, n2))
    tmpfile.close()
    os.system('/home/tsuname/Snap-2.0/examples/bigclam/bigclam -c:%s -i:%s' % (ncomm ,tmpfile.name))
    print 'Reading community file'
    resfile = open('cmtyvv.txt')
    lines = resfile.readlines()
    F[:] = 0
    for i, line in enumerate(lines):
        vals = [int(x) for x in line.strip().split('\t')]
        for v in vals[1:]:
            F[v,i] = 1
    for v1 in xrange(nvars):
        for v2 in xrange(v1, nvars):
            D[v1,v2] = dot(F[v1,:], F[v2,:])
            D[v2,v1] = D[v1,v2]
    # F contains the association vectors for each node
    # D is the penalty matrix induced by F, for the graphical LASSO
    print 'Done getting communities'
    return F, D

# Start by calling bigclam, get community structure first

# Get covariance matrix with the graphical LASSO
# for a covariance matrix  and using a penalty matrix D
def get_covariance_matrix_glasso(s, D):
    rho = robjects.r.matrix(robjects.FloatVector(D.ravel()), nrow=D.shape[0], byrow=True)
    rs = robjects.r.matrix(robjects.FloatVector(s.ravel()), nrow=s.shape[0], byrow=True)
    gobj = glasso(rs, rho)
    Sigma = reshape(array(list(gobj[0])), [D.shape[0], D.shape[1]])
    return Sigma

def get_covariance_matrix_JGL(X, D):
    lambda1 = robjects.r.matrix(robjects.FloatVector(D.ravel()), nrow=D.shape[0], byrow=True)
    lambda2 = 0
    rX = robjects.r.matrix(robjects.FloatVector(X.ravel()), nrow=X.shape[0], byrow=True)
    rL = robjects.ListVector({'1':rX, '2':rX})
    gobj = JGL(rL, lambda1=lambda1, lambda2=lambda2, return_whole_theta=True)
    Sigma = reshape(array(list(gobj[0][0])), [D.shape[0], D.shape[1]])
    return Sigma

print 'First bigclam iteration'
F, D = get_community_associations(Sigma, args.ncomm)
for i in xrange(args.maxiter):
    print 'Iteration %s' % i
    if args.method == 'glasso':
        print 'Getting covariance matrix with graphical LASSO'
        Sigma = get_covariance_matrix(Sigma, D)
    if args.method == 'jgl':
        print 'Getting covariance matrix with fused graphical LASSO'
        Sigma = get_covariance_matrix_JGL(Sigma, D)
    print 'Getting community associations with BIGCLAM'
    F, D = get_community_associations(Sigma, args.ncomm, D=D, F=F)
print 'Done'
pickle.dump(Sigma, open('Sigma.pickle', 'w'))
pickle.dump(F, open('F.pickle', 'w'))
pickle.dump(D, open('D.pickle', 'w'))
