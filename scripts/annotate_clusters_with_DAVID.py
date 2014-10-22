import argparse
import pdb
import gett.io
from suds import WebFault
from gett.annotation import DAVIDannotate

parser = argparse.ArgumentParser()

parser.add_argument('geneexpressionfile', type=argparse.FileType('r'))
parser.add_argument('communityfile', type=argparse.FileType('r'))
parser.add_argument('outfile', type=argparse.FileType('w'))
parser.add_argument('--sizecutoff', type=int, default=5)

args = parser.parse_args()

s2efile = open('/home/tsuname/resources/hs_symbol2entrez.txt')
symbol2entrez = {}
line = s2efile.readline()
while line:
    f = line.strip().split('\t')
    if len(f) > 1:
	symbol2entrez[f[0]] = f[1]
    line = s2efile.readline()
samples, genenames, Mexop = gett.io.read_expression_matrix(args.geneexpressionfile)
nodesbycluster, edgesbycluster = gett.io.read_community(args.communityfile)

writehead = True
args.outfile.write('#First column is cluster id, the rest are tuples per term of the form:')
for cid, nodes in nodesbycluster.iteritems():
    if len(nodes) >= args.sizecutoff:
	print 'Doing cluster %s' % cid
	genelist = [symbol2entrez[genenames[i]] for i in nodes if genenames[i] in symbol2entrez]
	namelist = [genenames[i] for i in nodes]
	annotdict, dictlabels = DAVIDannotate(genelist, category='KEGG_PATHWAY,GOTERM_MF_ALL,GOTERM_BP_ALL,GOTERM_CC_ALL')
	if writehead:
	    args.outfile.write(':'.join(dictlabels) + '\n')
	    writehead = False
	args.outfile.write('%s' % cid)
	for term, vals in annotdict.iteritems():
	    args.outfile.write('\t' + term + ':' + ':'.join([str(x) for x in vals]))
	args.outfile.write('\n')
	
args.outfile.close()


