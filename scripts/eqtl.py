import sys
import pdb
import utils
import pickle
from optparse import OptionParser
from numpy import *
from sklearn.linear_model import Lasso

usage = 'usage: python %prog [options] gene_exp_file genotype_matrix_file snp_file genotyped_samples_file output_file'
parser = OptionParser(usage)
parser.add_option('-a', '--alpha', dest='alpha', default=0.1, type='float')
parser.add_option('-s', '--start', dest='runstart', default=0, type='int')
parser.add_option('-e', '--stop', dest='runstop', default=0, type='int')
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

for line in genmatfile.readlines():
    fields = line.strip().split(' ')
    if fields[0] in exp_samples:
        genmat.append([float(d) for d in fields[options.skipfields:]])

genmat = array(genmat)

snps = [l.strip() for l in snpfile.readlines()]

print 'Finished reading files...'
dims = shape(eigenmat)
if options.runstart == 0 and options.runstop == 0:
    iterrange = range(dims[0])
else:
    iterrange = range(options.runstart, options.runstop)
for i in iterrange:
    lasso = Lasso(alpha=options.alpha)
    print 'Doing %s' % i
    lasso.fit(genmat, eigenmat[i,:])
    print lasso
    print lasso.coef_.max()
    coefs = array(lasso.coef_)
    indices = abs(coefs).argsort()[::-1]
    resultfile.write('%s\t' % clusterids[i] +'\t'.join(['%s:%s' % (snp, coeff) for snp, coeff in zip([snps[i] for i in indices], coefs[indices]) if coeff != 0.]) + '\n')
