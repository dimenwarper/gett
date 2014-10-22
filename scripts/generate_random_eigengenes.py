import sys
import gett.io
import argparse
import numpy.linalg
import numpy.random
import random

parser = argparse.ArgumentParser()
parser.add_argument('communityfile', metavar='COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('expfile', metavar='EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('numsamples', metavar='N', type=int)
parser.add_argument('outfile', metavar='OUT_FILE', type=argparse.FileType('w'))
parser.add_argument('--sizecutoff', default=5, type=int)

args = parser.parse_args()
print 'Parsing expression file'
header, genenames, Mexp = gett.io.read_expression_matrix(args.expfile)
print 'Parsing community file'
nodesbycommunity, communities = gett.io.read_community(args.communityfile)

sizes = [len(nodes) for nodes in nodesbycommunity.values() if len(nodes) >= args.sizecutoff]

for i in range(args.numsamples):
    size = random.choice(sizes)
    genes = numpy.random.random_integers(0, high=len(genenames)-1, size=size)
    eigengene = numpy.linalg.svd(Mexp[genes, :])[2][0]
    args.outfile.write('%s\t' % i + '\t'.join([str(f) for f in eigengene]) + '\n')
