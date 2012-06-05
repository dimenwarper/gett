import sys
import pdb
from optparse import OptionParser

parser = OptionParser('usage: python %prog genotypefile.ped snpfile.bim outfile')
parser.add_option('-i', '--idfile', dest='idfile', help='A file that specifies sample ids to be counted in the genotype matrix,\
                                                         one for each row. Default is all samples are taken into account.')
parser.add_option('-s', '--snpidfile', dest='snpidfile', help='A file that specifies SNPs to be counted in the genotype matrix,\
                                                         one for each row. Default is all SNPs are taken into account.')
parser.add_option('-f', '--skipfields', dest='skipfields', type='int', default=6,  help='Number of fields to skip before beginning of genotype values in \
										genotypefile.ped')
(options, args) = parser.parse_args()
if len(args) != 3:
    parser.error('Incorrect number of arguments')
genfile = open(args[0])
snpfile = open(args[1])
if options.idfile:
    idfile = open(options.idfile)
    allids = False
else:
    ids = []
    allids = True

snpindices = []
if options.snpidfile:
    snpidfile = open(options.snpidfile)
    allsnps = False
    #(major, minor) alleles
else:
    snps = [x.strip().split('\t')[-2:] for x in snpfile.readlines()]
    allsnps = True

outfile = open(args[2], 'w')

if not allids:
    ids = [x.strip() for x in idfile.readlines()]
    print 'Have %s ids in list' % len(ids)

if not allsnps:
    snpids = [x.strip() for x in snpidfile.readlines()]
    print 'Have %s snp ids  in list' % len(snpids)
    lines = snpfile.readlines()
    snps = [x.strip().split('\t')[-2:] for x in lines]
    for i, line in enumerate(lines):
	fields = line.strip().split('\t')
	if fields[1] in snpids:
	    snpindices.append(i)
count = 0
while True:
    line = genfile.readline()
    if not line:
        break
    fields = line.strip().replace('\t', ' ').split(' ')
    if allids or fields[0] in ids:
	count += 1
	outfile.write(' '.join(fields[:options.skipfields]))
	gens = fields[options.skipfields:]
	for i in range(0, len(gens), 2):
	    j = i/2
	    if allsnps or j in snpindices:
		if snps[j][1] == gens[i] or snps[j][1] == gens[i+1]:
		    if snps[j][1] == gens[i] and snps[j][1] == gens[i+1]:
			outfile.write(' 2')
		    else:
			outfile.write(' 1')
		else:
		    outfile.write(' 0')
	outfile.write('\n') 
    else:
	print 'Not found in list: '+fields[0]
print 'Found %s ids' % count
