import argparse
import ett.io
import ett.enrichment

parser = argparse.ArgumentParser()
parser.add_argument('--sizecutoff', type=int, default=5)
parser.add_argument('expfile', metavar='EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('communityfile', metavar='COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('outprefix', metavar='OUT_PREFIX', type=str)

args = parser.parse_args()

print 'Parsing expression file'
header, genenames, Mexp = ett.io.read_expression_matrix(args.expfile)
print 'Parsing community file'
nodesbycommunity, communities = ett.io.read_community(args.communityfile)
print 'Building universe dict'
universe = ett.enrichment.build_go_dict(genenames)
print 'Performing analysis'
for cid, nodes in nodesbycommunity.iteritems():
    if len(nodes) >= args.sizecutoff:
	print 'Doing %s' % cid
	selgenenames = [genenames[i] for i in nodes]
	selected = ett.enrichment.build_go_dict(selgenenames)
	term_res = ett.enrichment.go_enrichment(universe, selected)
	outfile = open('%s_%s.txt' % (args.outprefix, cid), 'w') 
	outfile.write('\n'.join(['\t'.join([str(x) for x in row]) for row in term_res]))
	outfile.close()

