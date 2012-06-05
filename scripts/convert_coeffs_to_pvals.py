import sys
import ett.io
import argparse
import random
from scipy import stats
from itertools import chain
from numpy import array
import pdb

parser = argparse.ArgumentParser()
parser.add_argument('coefficient_file', type=argparse.FileType('r'))
parser.add_argument('background_file', type=argparse.FileType('r'))
parser.add_argument('snp_coordinate_file', type=argparse.FileType('r'))
parser.add_argument('out_file',  type=argparse.FileType('w'))

args = parser.parse_args()

print 'Reading files'
snp2coordinates = ett.io.snp2coordinate(args.snp_coordinate_file)
coeffs, coeff_labels, coeff_snpids, coeff_in_coords = ett.io.parse_coeff_file(args.coefficient_file, snp2coordinates)
background_coeffs, background_coeff_labels, background_coeff_snpids, background_coeff_in_coords = ett.io.parse_coeff_file(args.background_file, snp2coordinates)

print 'Building distributions'
all_background_coeffs = abs(array([x for x in chain(*background_coeffs.values())]))
params = stats.norm.fit(all_background_coeffs)
background_dist = stats.norm(loc=params[0], scale=params[1]).pdf

snp_counts = {}
all_snpids = chain(*background_coeff_snpids.values())
N = float(len(background_coeff_snpids))
for id in all_snpids:
    if id in snp_counts:
	snp_counts[id] += 1
    else:
	snp_counts[id] = 1

print 'Doing the tests'
print 'Number of random tests were %s' % N
for cid, coefficients in coeffs.iteritems():
    print 'Doing %s with %s coefficients' % (cid, len(coefficients))
    minpval = 1
    minidx = -1
    args.out_file.write(str(cid))
    for i, id in enumerate(coeff_snpids[cid]):
	if id in snp_counts:
	    pval = snp_counts[id]/N
	else:
	    pval = 0.1/N
	if pval < minpval:
	    minpval = pval
	    minidx = i
	args.out_file.write('\t%s:%f' % (coeff_snpids[cid][i], pval))
    args.out_file.write('\n')
    print 'Minimum p-value was %s located in coordinates %s' % (minpval, coeff_in_coords[cid][minidx]) 

