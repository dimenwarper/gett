import sys
import pdb
from ett import utils
from ett.network_building import validation
from optparse import OptionParser
from numpy import *

usage = 'usage: python %prog [options] snp_file eqtl_test_file gtex_file output_file'
parser = OptionParser(usage)
options, args = parser.parse_args()
snp_file = open(args[0])
coeff_file = open(args[1])
gtex_file = open(args[2])
output_file = open(args[3], 'w')

print 'Building GTEx dictionary'

gtex_dict = validation.build_gtex_dict(gtex_file)

print 'Building snp2coordinates dictionary'
snp2coordinates = {}
line = snp_file.readline()
while line:
    fields = line.strip().split('\t')
    snp2coordinates[fields[1]] = [fields[0], int(fields[3])]
    line = snp_file.readline()

print 'Getting coefficients'
coeffs = {}
line = coeff_file.readline()
while line:
    fields= line.strip().split('\t')
    clustid = float(fields[0])
    coeffs[clustid] = [0]*len(fields[1:])
    gtex_line = ''
    for i, f in enumerate(fields[1:]):
	label, coeff = f.split(':')
        if label in snp2coordinates:
	    chrom, coord = snp2coordinates[label]
	coeffs[clustid][i] = [label, chrom, coord, float(coeff)] 
	if (chrom, coord) in gtex_dict:
	    gtex_line += '\t%s,%s,%s,%s' % (chrom, coord, coeff, ','.join(gtex_dict[(chrom, coord)]))
    if len(gtex_line) > 0:
	output_file.write('%s%s\n' % (clustid, gtex_line))
    line = coeff_file.readline()
output_file.close()
