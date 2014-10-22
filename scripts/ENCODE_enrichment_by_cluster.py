import gett.io
import argparse
import gett.io
from gett.annotation import ENCODEannotate
from scipy.stats import fisher_exact 

parser = argparse.ArgumentParser()

parser.add_argument('snpcoordinatefile', type=argparse.FileType('r'))
parser.add_argument('regressionfile', type=argparse.FileType('r'))
parser.add_argument('--bgsnpfile', type=argparse.FileType('r'), default=None)
parser.add_argument('--usetotalasbg', type=bool, default=False)
parser.add_argument('outfile', type=argparse.FileType('w'))

args = parser.parse_args()

print 'Reading input files'
snp2coordinates = gett.io.snp2coordinate(args.snpcoordinatefile)
coeffs, coeff_labels, coeff_snpids, coeff_in_coords = gett.io.parse_coeff_file(args.regressionfile, snp2coordinates)

def get_snp_counts(snplist):
    annotated_bgsnps = ENCODEannotate(snplist)
    cat_bgsnps = {}
    cat_bgsnps['cat1'] = len(annotated_bgsnps['cat1'])
    cat_bgsnps['cat2'] = len(annotated_bgsnps['cat2'])
    cat_bgsnps['cat3'] = len(annotated_bgsnps['cat3'])
    return cat_bgsnps


print 'Getting regulomeDB category counts for background SNPs'
if args.bgsnpfile:
    bgsnps = gett.io.read_coord_file(args.bgsnpfile)
    cat_bgsnps = get_snp_counts(bgsnps)
    tot_bgsnps = len(bgsnps)
else:
    if args.usetotalasbg:
	bgsnps = set([])
	for cid, coords in coeff_in_coords.iteritems():
	    bgsnps = bgsnps.union(set([tuple(c) for c in coords]))
	cat_bgsnps = get_snp_counts(bgsnps)
	tot_bgsnps = len(bgsnps)
    else:
	cat_bgsnps = {}
        # Number of snps in each category, given regulomedb
	cat_bgsnps['cat1'] = 39432
	cat_bgsnps['cat2'] = 407796
	cat_bgsnps['cat3'] = 318297
	tot_bgsnps = 12e6 # Number of snps in dbsnp, approx


args.outfile.write('#Cluster id\tCategory 1 significance:oddsratio\tCategory 2 significance:oddsratio\t\
                    Category 3 significance:oddsratio\n')

for cid, coords in coeff_in_coords.iteritems():
    print 'Doing %s' % cid
    annotated_snps = ENCODEannotate(coords)
    tot_snps = len(coords)
    cats = ['cat1', 'cat2', 'cat3']
    args.outfile.write('%s' % cid)
    for c in cats:
	cat_snps = len(annotated_snps[c])
	contingency_table = [[cat_snps, cat_bgsnps[c]], [tot_snps - cat_snps, tot_bgsnps - cat_bgsnps[c]]]
	print contingency_table
	oddsratio, pval = fisher_exact(contingency_table)
	args.outfile.write('\t%s:%s' % (pval, oddsratio))
    args.outfile.write('\n')

args.outfile.close()
