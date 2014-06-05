import argparse
import ett.io_utils
from ett.network_building import causality
import pdb


parser = argparse.ArgumentParser()
parser.add_argument('expfile', metavar='EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('communityfile', metavar='COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('genmatfile', metavar='GENOTYPE_MATRIX_FILE', type=argparse.FileType('r'))
parser.add_argument('regressedfile', metavar='REGRESSED_SNPS_FILE', type=argparse.FileType('r'))
parser.add_argument('snpfile', metavar='SNP_BIM_FILE', type=argparse.FileType('r'))
parser.add_argument('--skip', type=int, help='Number of columns to skip when parsing genotype matrix', default=6)
parser.add_argument('--minsnps', metavar='MIN_NUM_SNPS', type=int, help='Minimum number of SNPs that a module must have to be directed', default=5)
parser.add_argument('outfile', metavar='OUT_FILE', type=argparse.FileType('w'))

args = parser.parse_args()

print 'Parsing expression file'
samples, genenames, Mexp = ett.io_utils.read_expression_matrix(args.expfile)
samples = [s.replace('.CEL', '') for s in samples]
print 'Parsing community file'
nodesbycommunity, communities = ett.io_utils.read_community(args.communityfile)
print 'Parsing bim snp file'
snpdict = dict([(line.strip().split('\t')[1], i) for i, line in enumerate(args.snpfile.readlines())])

print 'Parsing regressed snps file'
restrict_snps = {}
line = args.regressedfile.readline()
while line:
    fields = line.strip().split('\t')
    restrict_snps[float(fields[0])] = [snpdict[f.split(':')[0]] for f in fields[1:] if f.split(':')[0] in snpdict]
    line = args.regressedfile.readline()
print 'Parsing genotype matrix file'
labels, Mgen = ett.io_utils.read_genotype_matrix(args.genmatfile, skip_fields=args.skip)
indices = [i for i, l in enumerate(labels) if l[0] in samples]
Mgen = Mgen[indices, :]
print 'Calculating directionality' 
indices = [samples.index(l[0]) for l in labels if l[0] in samples]
for c, edges in communities.iteritems():
    if len(nodesbycommunity[c]) >= 5:
	print 'Doing %s with length %s' % (c, len(nodesbycommunity[c]))
	if c in restrict_snps and len(restrict_snps[c]) >= args.minsnps:
            print '%s is in coefficient file and has %s SNPs' % (c, len(restrict_snps[c]))
	    new_edges = causality.direct_edges(Mexp[:, indices], edges, Mgen, restrict_snps=restrict_snps[c])
            print len(new_edges)
	    for e in new_edges:
		args.outfile.write('%s\t%s\t%s\n' % (c, e[0], e[1]))

args.outfile.close()


