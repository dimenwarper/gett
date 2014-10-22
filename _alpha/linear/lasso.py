from numpy import arange, dot, zeros
from numpy.random import rand
from numpy.linalg.linalg import norm
import pdb

def generalized_lasso(X, y, D, alpha, niter=100, x0=None, tol=0.001):
    n = X.shape[0]
    p = X.shape[1]
    indices = arange(p)
    if x0 is None:
        res = rand(p)
    else:
        res = x0
    for it in xrange(1000):
        gap = 0
        for i in xrange(p):
            x_i = res[indices != i]
            X_i = X[:, indices != i]
            prev = res[i]
            res[i] = soft_thresh(alpha*D[:,i].sum()/norm(X[:,i]),
                    dot(X[:,i].T, y - dot(X_i, x_i))/dot(X[:,i].T, X[:,i]))
            gap += norm(res[i] - prev)
        if gap < tol:
            break
    print 'yues'
    return res



def soft_thresh(t, b):
    if b > 0 and abs(b) > t:
        return b - t
    elif b < 0 and abs(b) > t:
        return b + t
    else:
        return 0

