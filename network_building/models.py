import numpy as np
import ett.io
import rpy2.robjects as robjects
from collections import defaultdict
from sklearn.linear_model import lars_path
from sklearn import linear_model
from ett.linear.lasso import generalized_lasso
from ett.network_building.data_structures import SparseGraph

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
def CLAMseed(edges, neighbors, k):
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
        F = ones([len(nodes),k])*0.5 + 1e-10
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

    def __init__(alpha=10., tol=0.001, maxiter=20):
        self.alpha = alpha
        self.tol = tol
        self.maxiter = maxiter

    def __call__(S, num_comm=None):
        if num_comm == None:
            num_comm_values = [num_comm]
        else:
            comm_values = self._get_num_comm_values_to_try(S)

        curr_F = None
        curr_BIC = -inf
        for k in comm_values:
            print 'Seeding communities'
            F0 = CLAMSeed(S.edges, S.neighbors, k)
            F, llhood = self._sgd(F0, S)
            if self._bic(llhood, F) < curr_BIC:
                curr_BIC = self._bic(llhood, F)
                curr_F = F
        return curr_F

    def get_overlap_matrix(self, F):
        overlap_matrix = zeros([F.shape[0], F.shape[0]])
        for i in xrange(F.shape[0]):
            for j in xrange(i, F.shape[0]):
                overlap_matrix[i,j] = dot(F[i,:], F[j,:])
        return overlap_matrix

    def _bic(self, llhood, F):
        return -2*llhood + F.size*log(S.size)

    def _sgd(self, S, F0):
        alpha = self.alpha
        n = F0.shape[0]
        prevF = zeros(F0.shape)
        currF = F0.copy()
        sampleindices = range(F0.shape[0])
        i = 0
        llhood = -inf
        currdiff = ((currF - prevF)**2).max()
        while currdiff > self.tol and i < self.maxiter:
            print 'Iteration %s ---- Current diff: %s' % (i, currdiff)
            prevF = currF.copy()
            shuffle(sampleindices)
            #results = Parallel(n_jobs=100)(delayed(sgdgrad)(currF.ravel(), M, n, k, neighbors, idx) for idx in sampleindices[:100])
            results = [self._sgdgrad(S, currF, idx) for idx in sampleindices]
            for j, st in enumerate(results):
                if alpha*abs(st).max() > 0.7:
                    alpha = 0.7/abs(st).max()
                    print 'Reducing step size alpha to %s' % alpha
                currF -= alpha*st
                currF[currF <= 0] = 1e-10
                currF[currF > 1] = 1
            i += 1
            currdiff = ((currF - prevF)**2).max()
            llhood = self._calculate_llhood(S, currF)
        return currF, llhood

                
    def _sgdgrad(self, S, F, i):
        res = zeros(F.shape)
        """
        for j in xrange(n):
            res[k*i:k*i+k] = -0.5*F[j,:]/((dot(F[i,:], F[j,:]))**2)*abs(M[i,j]) + F[j,:]/dot(F[i,:], F[j,:])
        """
        sumF_neighbors = zeros([self.numcomm])
        if i in S.neighbors:
            for j in S.neighbors[i]:
                sumF_neighbors += -0.5*F[j,:]/((dot(F[i,:], F[j,:]) + 1)**2)*abs(S[i,j])
            res[i,:] = sumF_neighbors - 1/(F[i,:].sum() + 1)
        #print res[k*i:k*i+k] 
        return res

    def _calculate_llhood(self, S, F):
        res = 0
        sumF = F.sum(axis=0)
        logsumF = log(F.sum(axis=1))
        sumF_neighbors = 0
        for i in xrange(n):
            sumF_neighbors = 0
            for j in S.neighbors[i]:
                sumF_neighbors += 1/(dot(F[i,:],F[j,:]))*abs(S[i,j])*0.5
            res += sumF_neighbors + logsumF.sum() - log(F[i,:].sum())
        return res


        return 1
    
    def _laplace_prob(self, x, k):
        return 1/(2*k)*exp(-abs(x)/k)

    def _get_normalizing_constants(self, S, num_comm_range):
        Z_non_zero = scipy.sparse.lil_matrix(S.shape)
        Z_zero = self_laplace_prob(0, num_comm_range).sum()
        for i,j in S.edges():
            Z[i,j] = self._laplace_prob(S[i,j], num_comm).sum()
        return Z_zero, Z_non_zero

    def _get_num_comm_values_to_try(self, S):
        num_comm_range = arange(self.max_num_comm)
        Z_zero, Z_non_zero = self._get_normalizing_constants(S, num_comm_range)
        E_zero = 0.5*self._num_comm_prior()/Z_zero
        Var_zero = 0.25*self._num_comm_prior()*(self.max_num_comm)*(self.max_num_comm + 1)/Z_zero - E_zero**2
        E_pairwise = scipy.sparse.lil_matrix(S.shape)
        Var_pairwise = scipy.sparse.lil_matrix(S.shape)
        E_X = zeros(S.shape[0])
        Var_X = zeros(S.shape[0])
        
        for i,j in S.edges():
            for k in num_comm_range:
                E_pairwise[i,j] += (self._laplace_prob(S[i,j], k)*self._num_comm_prior()/Z_non_zero)*k
                Var_pairwise[i,j] += (self._laplace_prob(S[i,j], k)*self._num_comm_prior()/Z_non_zero)*k**2
            Var_pairwise[i,j] -= E_pairwise[i,j]**2
        
        E_sum_neigh = 0
        Var_sum_neigh = 0
        for i, j in S.edges():
            E_sum_neigh += E_pairwise[i,j]
            Var_sum_neigh += Var_pairwise[i,j]
        E_sum_neigh += (S.shape[0]**2 - len(S.edges()))*E_zero
        Var_sum_neigh += (S.shape[0]**2 - len(S.edges()))*Var_zero

        for i in xrange(S.shape[0]):
            E_X[i] = (S.shape[0]**2 - len(S.neighbors))*E_zero
            Var_X[i] = (S.shape[0]**2 - len(S.neighbors))*Var_zero
            for j in S.neighbors:
                E_X[i] += E_pairwise[i,j]
                Var_X[i] += Var_pairwise[i,j]
            E_X[i] -= 2*E_sum_neigh
            Var_X[i] += 4*Var_sum_neigh

        E = E_X.sum() - 2*E_sum_neigh
        Var = Var_X.sum() + 4*E_sum_neigh
        return [E + i*sqrt(Var) for i in arange(-3, 3)]

class CLIP():

    def __init__(self, ncomm=None, maxiter=10, commalpha=10., commtol=0.001, commiter=10):
        self.community_detector = LaplacianCLAM(alpha=commalpha, tol=commtol, maxiter=commiter)

    def __call__(self, Dtraits):
        prec_matrices = self._initialize_prec_matrices(Dtraits)
        cov_matrices = [cov(X) for X in Dtraits]
        comm_vectors = [0]*len(Dtraits)
        overlap_matrices = [0]*len(Dtraits)
        lambda2 = 0.1
        llhood = -inf
        for niter in xrange(self.maxiter):
            # Calculate overlap matrices and community vectors for each trait matrix given precision matrix
            for i, Sinv in enumerate(prec_matrices):
                comm_vectors[i] = self.community_detector(Sinv)
                overlap_matrices[i] = self.community_detector(comm_vectors[i])
            # Calculate precision matrices for each trait matrix given overlap matrices
            prec_matrices = joint_graphical_lasso(Dtraits, overlap_matrices, lambda2=lambda2)
            llhood = self._calculate_llhood(prec_matrices, cov_matrices, comm_vectors, lambda2)
    return prec_matrices, comm_vectors, llhood

    def _calculate_llhood(self, prec_matrices, cov_matrices, comm_vectors, lambda2):
        #TODO
        return 1

    def _initialize_prec_matrices(Dtraits):
        #TODO choose initial matrices correctly (cross-validating lambdas?)
        return joint_graphical_lasso(Dtraits, 0.15, lambda2=0.1)
