import numpy as np
import rpy2.robjects as robjects
from sklearn.linear_model import lars_path
from sklearn import linear_model
from generalized_lasso import generalized_lasso
from ett.network_building.models import SparseGraph

def joint_graphical_lasso(data_matrices, Lambda1, lambda2=0):
    n, p = data_matrices[0].shape[0], data_matrices[0].shape[0]
    
    if type(Lambda1) != float:
        rLambda1 = robjects.r.matrix(robjects.FloatVector(Lambda1.ravel()), nrow=n, byrow=True)
    else:
        rLambda1 = Lambda1
    matrix_list = [(i+1, robjects.r.matrix(robjects.FloatVector(X.ravel()), nrow=n, byrow=True)) for i, X in data_matrices]
    rmatrix_list = robjects.ListVector(dict(matrix_list))

    robjects.r('library(JGL)')
    glasso = robjects.r.glasso
    JGL = robjects.r.JGL


    gobj = JGL(rmatrix_list, lambda1=rLambda1, lambda2=lambda2, return_whole_theta=True)
    Thetas = [reshape(array(list(gobj[0][i])), [n, n]) for i in xrange(len(matrices))]
    return [SparseGraph(T) for T in Thetas]



def centralized_graphical_lasso( X, D, alpha=0.01, max_iter = 100, convg_threshold=0.001 ):
    """ This function computes the graphical lasso algorithm as outlined in Sparse inverse covariance estimation with the
        graphical lasso (2007).
        
    inputs:
        X: the data matrix, size (nxd)
        alpha: the coefficient of penalization, higher values means more sparseness.
        max_iter: maximum number of iterations
        convg_threshold: Stop the algorithm when the duality gap is below a certain threshold.
        
    
    
    """
    
    if alpha == 0:
        return cov_estimator(X)
    n_features = X.shape[1]

    mle_estimate_ = cov_estimator(X)
    covariance_ = mle_estimate_.copy()
    precision_ = np.linalg.pinv( mle_estimate_ )
    indices = np.arange( n_features)
    for i in xrange( max_iter):
        for n in range( n_features ):
            sub_estimate = covariance_[ indices != n ].T[ indices != n ]
            row = mle_estimate_[ n, indices != n]
            #solve the lasso problem
            # Not now DAAAAAAAAARLING! lez do the generalized lasso instead
            #_, _, coefs_ = lars_path( sub_estimate, row, Xy = row, Gram = sub_estimate, 
            #                            alpha_min = alpha/(n_features-1.),
            #                            method = "lars")
            #coefs_ = coefs_[:,-1] #just the last please.
            #clf = linear_model.Lasso(alpha=alpha)
            #clf.fit(sub_estimate, row)
            #coefs_ = clf.coef_
            coefs_ = generalized_lasso(sub_estimate, row, D, alpha)
	    #update the precision matrix.
            precision_[n,n] = 1./( covariance_[n,n] 
                                    - np.dot( covariance_[ indices != n, n ], coefs_  ))
            precision_[indices != n, n] = - precision_[n, n] * coefs_
            precision_[n, indices != n] = - precision_[n, n] * coefs_
            temp_coefs = np.dot( sub_estimate, coefs_)
            covariance_[ n, indices != n] = temp_coefs
            covariance_[ indices!=n, n ] = temp_coefs

        print 'Finished iteration %s' % i
        #if test_convergence( old_estimate_, new_estimate_, mle_estimate_, convg_threshold):
        if np.abs( _dual_gap( mle_estimate_, precision_, alpha ) )< convg_threshold:
                break
    else:
        #this triggers if not break command occurs
        print "The algorithm did not coverge. Try increasing the max number of iterations."
    
    return covariance_, precision_
        
        
        
        
def cov_estimator( X ):
    return np.cov( X.T) 
    
    
def test_convergence( previous_W, new_W, S, t):
    d = S.shape[0]
    x = np.abs( previous_W - new_W ).mean()
    print x - t*( np.abs(S).sum() + np.abs( S.diagonal() ).sum() )/(d*d-d)
    if np.abs( previous_W - new_W ).mean() < t*( np.abs(S).sum() + np.abs( S.diagonal() ).sum() )/(d*d-d):
        return True
    else:
        return False

def _dual_gap(emp_cov, precision_, alpha):
    """Expression of the dual gap convergence criterion

    The specific definition is given in Duchi "Projected Subgradient Methods
    for Learning Sparse Gaussians".
    """
    gap = np.sum(emp_cov * precision_)
    gap -= precision_.shape[0]
    gap += alpha * (np.abs(precision_).sum()
                    - np.abs(np.diag(precision_)).sum())
    return gap 
