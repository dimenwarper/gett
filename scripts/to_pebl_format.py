import argparse
import ett.io
import pdb

parser = argparse.ArgumentParser()
parser.add_argument('expfile', metavar='EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('communityfile', metavar='COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('prefix', metavar='PREFIX', type=str)
parser.add_argument('size_cutoff', metavar='CUTOFF', default=5, type=int)

args = parser.parse_args()

print 'Parsing expression file'
header, genenames, Mexp = ett.io.read_expression_matrix(args.expfile)
print 'Parsing community file'
nodesbycommunity, communities = ett.io.read_community(args.communityfile)

for c in nodesbycommunity:
    nodes = nodesbycommunity[c]
    if len(nodes) < args.size_cutoff:
	print 'Skipping %s' % c
	continue
    print 'Doing %s' % c
    numsamples = Mexp.shape[1]
    numgenes = Mexp.shape[0]
    nodeids = [n for n in range(numgenes) if n in nodes]
    nodenames = [genenames[n] for n in nodeids]
    peblfile = open(args.prefix + str(c) + '.txt', 'w')
    peblfile.write('\t'.join(nodenames) + '\n')
    for i in range(numsamples):
	peblfile.write('\t'.join([str(x) for x in Mexp[:,i]]) + '\n')
    peblfile.close()
    structfile = open(args.prefix + str(c) + '_struct.txt', 'w')
    for edge in communities[c]:
	structfile.write('%s\t%s\n' % (nodeids.index(edge[0]), nodeids.index(edge[1])))
    structfile.close()

