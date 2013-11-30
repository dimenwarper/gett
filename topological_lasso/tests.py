from generalized_lasso import generalized_lasso
from graphical_lasso import centralized_graphical_lasso
from matplotlib.pylab  import *
import ett.io

print 'Testing generalized_lasso'
A = randn(4,40)
y = randn(4)
D = rand(3,40)
def lasso_fun(x):
    return norm(dot(A,x) - y) + abs(dot(D, x).sum())

res = generalized_lasso(A, y, D, 1)
print 'Lasso result, evaluated in lasso function: %s' % lasso_fun(res)
print 'Random number, evaluated in lasso function: %s' % lasso_fun(randn(len(res)))


print 'Testing centralized_graphical_lasso'
# Read the heart failure eqtl dataset!
#samples, genenames, Mexp = ett.io.read_expression_matrix(open('../hf_eqtl/full_exp_varcutoff_50.txt'))
print 'Finished reading'
Mexp = randn(400,20000)
D = eye(Mexp.shape[0])
covariance, precision = centralized_graphical_lasso(Mexp.T, D, max_iter=1000)
print covariance
print precision
