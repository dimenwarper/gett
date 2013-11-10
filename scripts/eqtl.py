import sys
import pdb
from ett import utils
import pickle
from optparse import OptionParser
from numpy import *
from sklearn.linear_model import Lasso
from sklearn.linear_model import LassoCV

usage = 'usage: python %prog [options] gene_exp_file genotype_matrix_file snp_file genotyped_samples_file output_file'
parser = OptionParser(usage)
parser.add_option('-a', '--alpha', dest='alpha', default=0, type='float')
parser.add_option('-s', '--start', dest='runstart', default=0, type='int')
parser.add_option('-e', '--stop', dest='runstop', default=0, type='int')
parser.add_option('-c', '--cv', dest='cv', default=0, type='int', help='Perform regressions with cross validation to find regularization parameter')
parser.add_option('-k', '--skipfields', dest='skipfields', default=6, type='int')

options, args = parser.parse_args()
if len(args) != 5:
    parser.error('Incorrect number of options')

genfile = open(args[0])
genmatfile = open(args[1])
snpfile = open(args[2])
gensamplesfile = open(args[3])
resultfile = open(args[4], 'w')

print 'Reading files'

eigenmat = []

genotyped_samples =[l.strip() for l in gensamplesfile.readlines()]
exp_samples = genfile.readline().strip().split('\t') 
order = []
for i, s in enumerate(genotyped_samples):
    if s in exp_samples:
	order.append(exp_samples.index(s))

line= genfile.readline()
clusterids = []
while line:
    fields = line.strip().split('\t')
    clusterids.append(fields[0])
    exps = fields[1:]
    eigenmat.append([float(exps[i]) for i in order])
    line = genfile.readline()

eigenmat = array(eigenmat)

genmat = []

genmat_genids = []
genorder = []
for line in genmatfile.readlines():
    fields = line.strip().split(' ')
    if fields[0] in genotyped_samples and fields[0] in exp_samples:
        genmat.append([float(d) for d in fields[options.skipfields:]])
        genmat_genids.append(fields[0])

for i,s, in enumerate(genotyped_samples):
    if s in genmat_genids:
	genorder.append(genmat_genids.index(s))

eigenmat_genids = [exp_samples[i] for i in order]
genmat_genids = [genmat_genids[i] for i in genorder]
genmat = array(genmat)
snps = [l.strip() for l in snpfile.readlines()]

print 'Finished reading files...'
dims = shape(eigenmat)
if options.runstart == 0 and options.runstop == 0:
    iterrange = range(dims[0])
else:
    iterrange = range(options.runstart, options.runstop)
for i in iterrange:
    if options.alpha != 0:
	lasso = Lasso(alpha=options.alpha)
    else:
	lasso = LassoCV(cv=options.cv)
    print 'Doing %s' % i
    lasso.fit(genmat[genorder, :], eigenmat[i,:])
    coefs = array(lasso.coef_)
    indices = abs(coefs).argsort()[::-1]
    print 'Max coeff: %s' % coefs.max()
    print 'Params: %s' % lasso
    resultfile.write('%s\t' % clusterids[i] +'\t'.join(['%s:%s' % (snp, coeff) for snp, coeff in zip([snps[i] for i in indices], coefs[indices]) if coeff != 0.]) + '\n')
