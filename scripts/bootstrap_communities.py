import argparse
import gett.io
from gett.network_building import confidence


parser = argparse.ArgumentParser()
parser.add_argument('nbootstraps', metavar='N_BOOTSTRAPS', type=int, help='Number of sampling iterations for bootstrap')
parser.add_argument('mincorr', metavar='MIN_CORR', type=float, help='Minimum correlation hard threshold')
parser.add_argument('expfile', metavar='EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('communityfile', metavar='COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('outfile', metavar='OUT_FILE', type=argparse.FileType('w'))

args = parser.parse_args()

print 'Parsing expression file'
header, genenames, Mexp = gett.io.read_expression_matrix(args.expfile)
print 'Parsing community file'
nodesbycommunity, communities = gett.io.read_community(args.communityfile)
print 'Doing bootstraps'
confidence_values = confidence.bootstrap_communities(Mexp, communities, args.nbootstraps, min_corr=args.mincorr)
gett.io.write_dict(args.outfile, confidence_values, split_lists=True)

