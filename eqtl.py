import sys
import utils
import pickle
from optparse import OptionParser
from numpy import *
from scikits.learn.glm import Lasso

usage = 'usage: python %prog [options] gene_exp_file genotpye_matrix_file output_file'
parser = OptionParser(usage)
parser.add_option('-a', '--alpha', dest='alpha', default=0.1, type='float')
parser.add_option('-f', '--from', dest='start', default=0, type='int')
parser.add_option('-s', '--start', dest='runstart', default=0, type='int')
parser.add_option('-e', '--stop', dest='runstop', default=0, type='int')
parser.add_option('-r', '--gtyperows', dest='rows', default=0, type='int')
parser.add_option('-c', '--gtypecols', dest='cols', default=0, type='int')

options, args = parser.parse_args()
if len(args) != 4:
    parser.error('Incorrect number of options')

genfile = open(args[0])
genmatfile = open(args[1])
resultfile = open(args[2], 'w')
coeffile = open(args[3], 'w')

print 'Reading files'

eigenmat = loadtxt(genfile, delimiter=' ')
if options.rows == 0 and options.cols == 0:
    genmat = loadtxt(genmatfile, delimiter=' ')
else:
    print 'Fixed matrix values detected'
    genmat = zeros([options.rows, options.cols])  
    for i in range(options.rows):
	fields = genmatfile.readline().strip().split(' ')
	for j, ff in enumerate(fields):
	    genmat[i,j] = float(ff)

print 'Finished reading files...'
lassos = []
dims = shape(eigenmat)
if options.runstart == 0 and options.runstop == 0:
    iterrange = range(dims[1])
else:
    iterrange = range(options.start, options.stop)
for i in iterrange:
    lasso = Lasso(alpha=options.alpha)
    lasso.fit(genmat[:,options.start:], eigenmat[:,i])
    print lasso
    print lasso.coef_.max()
    coeffile.write(' '.join([str(x) for x in lasso.coef_]) + '\n')
    lassos.append(lasso)

pickle.dump(lassos,resultfile)
