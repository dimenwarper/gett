import numpy as np
import sys
import pdb
import rpy2.robjects as robjects
import scipy.sparse
from collections import defaultdict
from sklearn.linear_model import lars_path
from sklearn import linear_model
from ett.linear.lasso import generalized_lasso
from ett.network_building.data_structures import SparseGraph
from random import shuffle
from matplotlib.pylab import *


def _data_matrix_to_R(X):
    p = X.shape[0]
    return robjects.r.matrix(robjects.FloatVector(X.values.T.ravel()), ncol=p, byrow=False)

def cov_shrink(data_matrix):
    robjects.r('library(corpcor)')
    p = data_matrix.shape[0]
    print 'Obtaining shrinkage estimator of covariance matrix (via corpcor)'
    res = robjects.r['cov.shrink'](_data_matrix_to_R(data_matrix))
    res = np.reshape(np.array(list(res)), [p,p])
    return res

def _filter_matrix(M, thresh, normalize=False):
    if normalize:
        normf = abs(M[abs(M) != 1]).max()
        print 'Normalizing value %s' % norm
    else:
        normf = 1
    if thresh is not None:
        M[abs(M)/normf < thresh] = 0
    print (M != 0).sum()
    selected_indices = np.array([True if (M[i,:] != 0).sum() > 2 else False for i in xrange(M.shape[0])])

    print 'Number of selected indices: %s' % sum(selected_indices)
    return selected_indices, M

def corr(data_matrix, thresh=None):
    print 'Obtaining correlation matrix (trivial estimator)'
    res = np.corrcoef(data_matrix)
    return _filter_matrix(res, thresh)

def pcor_shrink(data_matrix, thresh=None, cor=False):
    robjects.r('library(corpcor)')
    p = data_matrix.shape[0]
    if cor:
        print 'Obtaining shrinkage estimator of the correlation matrix (via corpcor)'
        res = robjects.r['cor.shrink'](_data_matrix_to_R(data_matrix))
    else:
        print 'Obtaining shrinkage estimator of the partial correlation matrix (via corpcor)'
        res = robjects.r['pcor.shrink'](_data_matrix_to_R(data_matrix))
    res = np.reshape(np.array(list(res)), [p,p])
    return _filter_matrix(res, thresh)

def invcov_shrink(data_matrix, thresh=None):
    robjects.r('library(corpcor)')
    p = data_matrix.shape[0]
    print 'Obtaining shrinkage estimator of inverse covariance matrix (via corpcor)'
    res = robjects.r['invcov.shrink'](_data_matrix_to_R(data_matrix))
    res = np.reshape(np.array(list(res)), [p,p])
    if thresh is not None:
        res[abs(res) < abs(res).mean() + abs(res).std()*thresh] = 0
    selected_indices = np.array([True if (res[i,:] != 0).sum() > 2 else False for i in xrange(p)])
    return selected_indices, res

def joint_graphical_lasso(data_matrices, Lambda1, lambda2=0, return_whole_theta=False, mindegree=0, return_aic=False):
    p, n = data_matrices[0].shape[0], data_matrices[0].shape[1]
    
    if type(Lambda1) == float:
        rLambda1 = robjects.FloatVector([Lambda1])
    elif type(Lambda1) == np.ndarray:
        rLambda1 = robjects.r.matrix(robjects.FloatVector(Lambda1.ravel()), nrow=p, byrow=True)
    elif type(Lambda1) == list:
        rLambda1 = robjects.vectors.ListVector(dict([(str(i), robjects.r.matrix(robjects.FloatVector(L.ravel()), nrow=p, byrow=True)) for i, L in enumerate(Lambda1)]))
    else:
        print 'Type of penalty matrix not recognized'

    matrix_list = [(str(i+1), _data_matrix_to_R(X)) for i, X in enumerate(data_matrices)]
    rmatrix_list = robjects.ListVector(dict(matrix_list))

    robjects.r('library(JGL)')
    JGL = robjects.r.JGL


    print 'Calling JGL'
    gobj = JGL(rmatrix_list, lambda1=rLambda1, lambda2=lambda2, return_whole_theta=return_whole_theta, maxiter=50, tol=0.001)
    if return_whole_theta:
        Thetas = [np.reshape(np.array(list(gobj[0][i])), [p, p]) for i in xrange(len(data_matrices))]
        selected_indices = np.array([True]*p)
    else:
        selected_indices = np.array(gobj[2]) == 1
        new_p = selected_indices.sum()
        Thetas = [np.reshape(np.array(list(gobj[0][i])), [new_p, new_p]) for i in xrange(len(data_matrices))]
        print 'NEW_P %s ' % new_p
        selected_selected_indices = []
        for i, idx in enumerate(np.where(selected_indices)[0]):
            selected = False
            selected_indices[idx] = False
            for T in Thetas:
                if (T[i,:] != 0).sum() - 1 >= mindegree:
                    selected_indices[idx] = True
                    selected = True
            if selected:
                selected_selected_indices.append(i)
        Thetas = [T[selected_selected_indices,:][:,selected_selected_indices] for T in Thetas]
        new_p = selected_indices.sum()
        print 'NEW_P after pruning %s ' % new_p
        print 'Number of variables after JGL %s' % new_p
    sgraphs =  [SparseGraph(T) for T in Thetas]
    print 'Number of non-trivial edges: %s and %s' % (len([(i,j) for i,j in sgraphs[0].edges if i != j])/2, len([(i,j) for i,j in sgraphs[1].edges if i != j])/2)
    if return_aic:
        aic = 0.
        print 'Calculating AIC'
        for i, D in enumerate(data_matrices):
            print 'Data matrix %s' % i
            S = cov(array(D)[selected_indices, :])
            aic += D.shape[1]*trace(dot(S, Thetas[i])) - D.shape[1]*log(det(Thetas[i])) + 2*sgraphs[i].nnz
        return aic, selected_indices, sgraphs
    return selected_indices, sgraphs


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

def CLAMSeed(edges, neighbors, k):
        cuts = defaultdict(float)
        volumes = defaultdict(float)
        totvolume = 0
        conductances = defaultdict(float)
        nodes = set()
        for i,j in edges:
            nodes.add(i)
            nodes.add(j)
            for n in set(neighbors[i] + neighbors[j]):
                cuts[n] += 1.
            volumes[i] += 1.
            volumes[j] += 1.
            totvolume += 2.
        for n in nodes:
            conductances[n] = cuts[n]/min(totvolume - cuts[n], volumes[n])
        F = np.ones([len(nodes),k])*0.1
        commidx = -1
        for n in nodes:
            ismin = True
            for n1 in neighbors[n]:
                if conductances[n1] > conductances[n]:
                    ismin = False
                    break
            if ismin:
                commidx = (commidx + 1) % k
                F[n,commidx] = 1
                for n1 in neighbors[n]:
                    F[n1,commidx] = 1
        if F[:,k-1].sum() < 1:
            print 'WARNING: Number of communities exceeds number of locally minimum communities!'
            print 'Consider reducing the number of communities'
        return F

class LaplacianCLAM():

    def __init__(self, alpha=20., tol=0.001, maxiter=20, max_num_comm=1000, lambda1=1, ncomm_crit='splitval', target_scale=1.):
        self.max_num_comm = max_num_comm
        self.alpha = alpha
        self.tol = tol
        self.maxiter = maxiter
        self.lambda1 = lambda1
        self.target_scale = target_scale
        self.ncomm_crit = ncomm_crit

    def _calculate_scale(self, S, ncomm):
        #return max(10, sqrt(ncomm))
        return self.target_scale/abs(np.array(S.values())).mean()
        if ncomm < 100:
            return max(1, ncomm/20)
        else:
            return 20

    def __call__(self, S, num_comm=None):
        if num_comm != None:
            num_comm_values = [num_comm]
        else:
            num_comm_values = self._get_num_comm_values_to_try(S)
        num_comm_values = [70]

        calc_lhood = (len(num_comm_values) > 1)

        curr_F = None
        curr_BIC = np.inf
        curr_llhood = -np.inf
        if self.ncomm_crit == 'crossval':
            train_neighbors, test_neighbors = S.sample_edges(0.2, return_neighbors=True)
        elif self.ncomm_crit == 'splitval':
            train_neighbors, test_neighbors = S.split_edges(int(len(S.edges)*0.8), return_neighbors=True)
        else:
            train_neighbors, test_neighbors = None, None
        for k in num_comm_values:
            #TODO self.scale should not be saved, instead returned
            self.scale = self._calculate_scale(S, k)
            print 'Testing for number of communities %s' % k
            print 'Seeding communities'
            F0 = CLAMSeed(S.edges, S.neighbors, k)
            #old_llhood = self._calculate_llhood(S, F0, edges=test_edges)
            #print 'Starting likelihood is %s' % old_llhood
            print 'Starting gradient descent'
            F, llhood = self._sgd(S, F0, train_neighbors=train_neighbors, test_neighbors=test_neighbors, calc_lhood=calc_lhood)
            print 'Number of communities %s' % k 
            print 'Likelihood %s' % llhood
            print 'BIC %s' % self._bic(llhood, S, F)
            #pdb.set_trace()
            if self.ncomm_crit == 'bic':
                if self._bic(llhood, S, F) < curr_BIC:
                    curr_BIC = self._bic(llhood, S, F)
                    curr_F = F
            if self.ncomm_crit == 'crossval' or self.ncomm_crit == 'splitval':
                if llhood > curr_llhood:
                    curr_llhood = llhood
                    curr_F = F
        self.scale = self._calculate_scale(S, curr_F.shape[1])
        return F
    
    def _calculate_membership_params(self, S, ncomm):
        # epsilon is the background probability of an edge
        epsilon = min(0.9, 1./(S.shape[0]**2))
        # delta will be the threshold to decide if F[i,j] is one or not
        delta = sqrt(1./(2*(1 - epsilon)))
        return epsilon, delta

    def get_membership_vectors(self, S, F, copy=True):
        epsilon, delta = self._calculate_membership_params(S, F.shape[1])
        #print 'epsilon %s, delta %s' % (epsilon, delta)
        #print 'F max %s' % (F.max())
        #print 'F MYH7 \n%s' % (F[3956,:])
        #print 'F somethin \n%s' % (F[1000,:])
        if copy:
            F_thresh = F.copy()
        else:
            F_thresh = F
        F_thresh[F_thresh < delta] = 0
        F_thresh[F_thresh != 0] = 1
        return F_thresh

    def get_overlap_matrix(self, S, F):
        overlap_matrix = np.zeros([F.shape[0], F.shape[0]])
        for i in xrange(F.shape[0]):
            for j in xrange(i, F.shape[0]):
                overlap_matrix[i,j] = np.dot(F[i,:], F[j,:]) + 1
                overlap_matrix[j,i] = overlap_matrix[i,j]
        return overlap_matrix

    def _calculate_llhood(self, S, Fin, neighbors=None):
        if neighbors is None:
            neighbors = S.neighbors
        res1 = 0
        res2 = 0
        F = self.get_membership_vectors(S, Fin)
        print 'F:Max\tMin\tAverage Sum'
        print '%s\t%s\t%s' % (F.max(), F.min(), F.sum(axis=1).mean())
        print 'scale: %s' % self.scale 
        for i in xrange(F.shape[0]):
            sumF_neighbors = 0
            for j in neighbors[i]:
                sumF_neighbors += -self.lambda1*self.scale/(np.dot(F[i,:],F[j,:]) + 1)*np.abs(S[i,j])
                sumF_neighbors += -np.log(np.dot(F[i,:], F[j,:]) + 1)
            res1 += sumF_neighbors -(F.shape[0] - len(neighbors[i]))*np.log(F[i,:].sum() + 1)
            #res1 += sumF_neighbors -(F.shape[0])*np.log(F[i,:].sum() + 1)

        for i in xrange(S.shape[0]):
            for j in xrange(i, S.shape[1]):
                res2 += -self.lambda1*self.scale/(np.dot(F[i,:],F[j,:]) + 1)*np.abs(S[i,j])
                res2 += -np.log(np.dot(F[i,:],F[j,:]) + 1)
        res2 *= 2
        print 'True %s, approx. %s' % (res2, res1)
        return res2



    def _bic(self, llhood, S, F):
        return -2*llhood + F.size*np.log(S.size)

    def _sgd(self, S, F0, train_neighbors=None, test_neighbors=None, calc_lhood=True):
        alpha = self.alpha
        n = F0.shape[0]
        prevF = np.zeros(F0.shape)
        currF = F0.copy()
        st = np.zeros(F0.shape)
        sampleindices = range(F0.shape[0])
        i = 0
        llhood = -np.inf
        currdiff = ((currF[currF > 0] - prevF[currF > 0])**2).mean()
        #currdiff = abs(currF - prevF).max()
        while currdiff > self.tol and i < self.maxiter:
            sys.stdout.write('===\nIteration %s ---- Current diff: %s\n' % (i, currdiff))
            prevF = currF.copy()
            #shuffle(sampleindices)
            for j, idx in enumerate(sampleindices):
                sys.stdout.write('\r[%d of %d]' % (j, F0.shape[0]))
                sys.stdout.flush()
                st = self._sgdgrad(S, currF, idx, st, neighbors=train_neighbors)
                if alpha*abs(st).max() > currF.mean():
                    alpha = currF.mean()/np.abs(st).max()
                    #print 'Reducing step size alpha to %s' % alpha
                currF += alpha*st
            currF[currF <= 0] = 1e-10
            currF[currF > 1] = 1
            i += 1
            print ' '
            currdiff = ((currF[currF > 0] - prevF[currF > 0])**2).mean()
            #currdiff = abs(currF - prevF).max()
        if calc_lhood:
            if test_neighbors is not None:
                llhood = self._calculate_llhood(S, currF, neighbors=test_neighbors)
            else:
                llhood = self._calculate_llhood(S, currF)
        else:
            llhood = 1
        return currF, llhood

                
    def _sgdgrad(self, S, F, i, res, neighbors=None):
        if neighbors is None:
            neighbors = S.neighbors
        """
        for j in xrange(n):
            res[k*i:k*i+k] = -0.5*F[j,:]/((dot(F[i,:], F[j,:]))**2)*abs(M[i,j]) + F[j,:]/dot(F[i,:], F[j,:])
        """
        sumF_neighbors = np.zeros([F.shape[1]])
        if i in neighbors:
            sumF_neighbors[:] = 0
            for j in neighbors[i]:
                sumF_neighbors += self.lambda1*self.scale*F[j,:]/((np.dot(F[i,:], F[j,:]) + 1)**2)*np.abs(S[i,j])
                sumF_neighbors += -F[j,:]/(np.dot(F[i,:], F[j,:]) + 1)
            res[i,:] = sumF_neighbors - (F.shape[0] - len(neighbors[i]))/(F[i,:].sum() + 1)
            #res[i,:] = sumF_neighbors - (F.shape[0])/(F[i,:].sum() + 1)
            
        """
        for j in xrange(F.shape[0]):
            res[i,:] += self.lambda1*self.scale*F[j,:]/((np.dot(F[i,:],F[j,:]) + 1)**2)*np.abs(S[i,j])
            res[i,:] += -F[j,:]/(np.dot(F[i,:],F[j,:]) + 1)
        """
        return res
    
    def _laplace_prob(self, x, k):
        return 1./(2.*k)*np.exp(-np.abs(x)/k)

    def _get_normalizing_constants(self, S, num_comm_range):
        Z_non_zero = scipy.sparse.lil_matrix(S.shape)
        Z_zero = self._laplace_prob(0, num_comm_range).sum()
        for i,j in S.edges:
            Z_non_zero[i,j] = self._laplace_prob(S[i,j], num_comm_range).sum()
        return Z_zero, Z_non_zero
    
    def _num_comm_prior(self):
        return 1./self.max_num_comm

    def _get_num_comm_values_to_try(self, S):
        print 'Getting number of communities'
        limit = min(S.shape[0], 500)
        return np.arange(10, limit, limit/7 - 1)
        num_comm_range = np.arange(10, self.max_num_comm, 10)
        Z_zero, Z_non_zero = self._get_normalizing_constants(S, num_comm_range)
        E_zero = 0.5*self._num_comm_prior()/Z_zero.sum()
        Var_zero = 0.25*self._num_comm_prior()*(self.max_num_comm)*(self.max_num_comm + 1)/Z_zero.sum() - E_zero**2
        E_pairwise = scipy.sparse.lil_matrix(S.shape)
        Var_pairwise = scipy.sparse.lil_matrix(S.shape)
        E_X = np.zeros(S.shape[0])
        Var_X = np.zeros(S.shape[0])
        
        for i, j in S.edges:
            if i != j:
                for k in num_comm_range:
                    E_pairwise[i,j] += (self._laplace_prob(S[i,j], k)*self._num_comm_prior()/Z_non_zero[i,j])*k
                    Var_pairwise[i,j] += (self._laplace_prob(S[i,j], k)*self._num_comm_prior()/Z_non_zero[i,j])*k**2
                Var_pairwise[i,j] -= E_pairwise[i,j]**2
        
        E_sum_neigh = 0
        Var_sum_neigh = 0
        for i, j in S.edges:
            if i != j:
                E_sum_neigh += E_pairwise[i,j]
                Var_sum_neigh += Var_pairwise[i,j]
        E_sum_neigh += (S.shape[0]**2 - len(S.edges))*E_zero
        Var_sum_neigh += (S.shape[0]**2 - len(S.edges))*Var_zero

        for i in xrange(S.shape[0]):
            E_X[i] = (S.shape[0]**2 - len(S.neighbors))*E_zero
            Var_X[i] = (S.shape[0]**2 - len(S.neighbors))*Var_zero
            for j in S.neighbors:
                E_X[i] += E_pairwise[i,j]
                Var_X[i] += Var_pairwise[i,j]
            #E_X[i] -= E_sum_neigh
            #Var_X[i] += Var_sum_neigh

        E = E_X.sum()# - E_sum_neigh
        Var = Var_X.sum()# + E_sum_neigh
        return [int(E_X.max() + i*E_X.max()/5.) for i in np.arange(-4, 1)]
        #return [E + i*np.sqrt(Var) for i in np.arange(-3, 3)]

class CLIP():

    def __init__(self, ncomm=None, maxiter=10, commalpha=10., commtol=0.001, commiter=50, lambda1=0.7, lambda2=0.005, mindegree=0, initthresh=0.5):
        self.maxiter = maxiter
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.initthresh = initthresh
        self.ncomm = ncomm
        self.mindegree = mindegree
        self.community_detector = LaplacianCLAM(alpha=commalpha, tol=commtol, maxiter=commiter, lambda1=self.lambda1)

    def __call__(self, Dtraits):
        currDtraits = Dtraits
        selected_indices, prec_matrices = self._initialize_prec_matrices(Dtraits)
        prev_prec_matrices = prec_matrices
        currDtraits = [D.ix[selected_indices,:] for D in currDtraits]
        for g in ['NPPA', 'NPPB', 'MYH7', 'MYBPC3', 'ATP2A2', 'PPP1R3A']:
            if g not in currDtraits[0].index:
                print '%s NOT in selected genes! >:|' % g
            else:
                print '%s in selected genes! =D' % g
        nnt_edges_prev = [len([(i,j) for i,j in M.edges if i != j])/2 for M in prec_matrices]
        print 'Number of non-trivial edges: %s' % ','.join([str(x) for x in nnt_edges_prev])
        print 'Number of variables %s' % selected_indices.sum()
        cov_matrices = [np.cov(X) for X in Dtraits]
        comm_vectors = [0]*len(currDtraits)
        overlap_matrices = [0]*len(currDtraits)
        penalty_matrices = [0]*len(currDtraits)
        llhood = -np.inf
        num_var = [selected_indices.sum()]
        num_comms = [None for i in xrange(len(Dtraits))]
        for niter in xrange(self.maxiter):
            # Calculate overlap matrices and community vectors for each trait matrix given precision matrix
            for i, Sinv in enumerate(prec_matrices):
                comm_vectors[i] = self.community_detector(Sinv, num_comm=num_comms[i])
                comm_vectors[i] = self.community_detector.get_membership_vectors(Sinv, comm_vectors[i])
                overlap_matrices[i] = self.community_detector.get_overlap_matrix(Sinv, comm_vectors[i])
                penalty_matrices[i] = self.community_detector.scale*self.lambda1/overlap_matrices[i]
                #if overlap_matrices[i].max() > 1:
                #    overlap_matrices[i] = overlap_matrices[i]/overlap_matrices[i].max()
                print 'Number of communities for %s: %s' % (i, comm_vectors[i].shape[1])
            num_comms = [v.shape[1] for v in comm_vectors]
            print 'Number of communities %s' % num_comms
            #if niter == 0:
                #print 'Overlaps for MYH7'
                #print overlap_matrices[0][3956,:]
                #print overlap_matrices[1][3956,:]
                #pdb.set_trace()

            
            # Calculate precision matrices for each trait matrix given overlap matrices
            prev_prec_matrices = prec_matrices
            selected_indices, prec_matrices = joint_graphical_lasso(currDtraits, penalty_matrices, lambda2=self.lambda2, return_whole_theta=True)
            num_var.append(selected_indices.sum())
            currDtraits = [D.ix[selected_indices,:] for D in currDtraits]
            llhood = self._calculate_llhood(prec_matrices, cov_matrices, comm_vectors, self.lambda2)

            nnt_edges_new = [len([(i,j) for i,j in M.edges if i != j])/2 for M in prec_matrices]

            print 'At iteration %s' % niter
            print 'Number of non-trivial edges: %s' % ','.join([str(x) for x in nnt_edges_new])
            print 'Number of variables %s' % selected_indices.sum()
            finished = True
            #for ne_new, ne_prev in zip(nnt_edges_new, nnt_edges_prev):
            #    if ne_new != ne_prev:
            #        finished = False
            print 'Diff'
            for i in xrange(len(prec_matrices)):
                tot_nnz = float(prev_prec_matrices[i].nnz)
                for n1, n2 in prec_matrices[i].edges:
                    if (n1,n2) not in prev_prec_matrices[i].edges:
                        tot_nnz += 1
                diff = (abs(prev_prec_matrices[i] - prec_matrices[i])**2).sum()/tot_nnz
                pec = (abs(nnt_edges_prev[i] - nnt_edges_new[i])/tot_nnz)
                print '%s: diff %s, %% edges changed %s' % (i, diff, pec)
                if diff > 0.001 and pec > 0.01:
                    finished = False
            nnt_edges_prev = nnt_edges_new

            if finished:
                break

        membership_vectors = [self.community_detector.get_membership_vectors(prec_matrices[i], comm_vectors[i]) for i in xrange(len(prec_matrices))]

        print num_var
        return currDtraits, prec_matrices, membership_vectors, llhood

    def _calculate_llhood(self, prec_matrices, cov_matrices, comm_vectors, lambda2):
        #TODO
        return 1
    
    def _initialize_prec_matrices(self, Dtraits):

        #TODO choose initial matrices correctly (cross-validating lambdas?)
        p = Dtraits[0].shape[0]
        #return joint_graphical_lasso(Dtraits, 0.47, lambda2=self.lambda2, mindegree=self.mindegree, return_whole_theta=False)
        pinit = []
        init_indices = np.array([False]*p)
        for i in xrange(len(Dtraits)):
            #selected_indices, invcov = invcov_shrink(Dtraits[i])
            selected_indices, invcov = corr(Dtraits[i], thresh=self.initthresh)
            pinit.append(invcov)
            init_indices = np.logical_or(init_indices, selected_indices)
        print 'Initializing with %s elements' % init_indices.sum()
        for i in xrange(len(Dtraits)):
            pinit[i] = SparseGraph(pinit[i][init_indices,:][:,init_indices])
        return init_indices, pinit

class Shrinkage(object):

    def __init__(self, method='pcor', thresh=0):
        self.method = method
        self.thresh = thresh

    def __call__(self, Dtraits):
        p = Dtraits[0].shape[0]
        res = []
        indices = np.array([False]*p)
        for i in xrange(len(Dtraits)):
            if self.method == 'pcor':
                selected_indices, mat = pcor_shrink(Dtraits[i], thresh=self.thresh)
            if self.method == 'cor':
                selected_indices, mat = pcor_shrink(Dtraits[i], thresh=self.thresh, cor=True)
            if self.method == 'naive':
                selected_indices, mat = corr(Dtraits[i], thresh=self.thresh)
            res.append(mat)
            indices = np.logical_or(indices, selected_indices)
        print 'Number of connected traits: %s' % indices.sum()
        for i in xrange(len(Dtraits)):
            res[i] = res[i][indices,:][:,indices]
        return res, [i for i, idx in enumerate(indices) if idx]


