import pdb
import argparse
import ett.io
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('expfile_sp1', type=argparse.FileType('r'))
parser.add_argument('expfile_sp2', type=argparse.FileType('r'))
parser.add_argument('commfile_sp1', type=argparse.FileType('r'))
parser.add_argument('commfile_sp2', type=argparse.FileType('r'))
parser.add_argument('--sizecutoff', type=int, default=5)
parser.add_argument('--homologene', type=bool, default=False)
parser.add_argument('--taxid1', type=int, default=0)
parser.add_argument('--taxid2', type=int, default=0)
parser.add_argument('homfile', type=argparse.FileType('r'))
parser.add_argument('outfile', type=argparse.FileType('w'))

args = parser.parse_args()
print 'Parsing expression files'
samples_sp1, genenames_sp1, Mexp_sp1 = ett.io.read_expression_matrix(args.expfile_sp1)
samples_sp2, genenames_sp2, Mexp_sp2 = ett.io.read_expression_matrix(args.expfile_sp2)
print 'Parsing community files'
nodesbycluster_sp1, edgesbycluster_sp1 = ett.io.read_community(args.commfile_sp1)
nodesbycluster_sp2, edgesbycluster_sp2 = ett.io.read_community(args.commfile_sp2)

print 'Species 1 has %s communities' % len(nodesbycluster_sp1)
print 'Species 2 has %s communities' % len(nodesbycluster_sp2)

homcount = defaultdict(int)
max_hom_nets = {}
homdict = defaultdict(list)

if args.homologene:
    homdict_sp1 = defaultdict(set)
    homdict_sp2 = defaultdict(set)

line = args.homfile.readline()

while line:
    fields = line.strip().split('\t')
    if args.homologene:
	if int(fields[1]) == args.taxid1:
	    homdict_sp1[fields[3].lower()].add(fields[0])
	if int(fields[1]) == args.taxid2:
	    homdict_sp2[fields[3].lower()].add(fields[0])
    else:
	homdict[fields[0].lower()].append(fields[1].lower())
    line = args.homfile.readline()

pdb.set_trace()
for cidsp1, nodessp1 in nodesbycluster_sp1.iteritems():
    if len(nodessp1) > args.sizecutoff:
	print 'Doing %s with %s number of nodes' % (cidsp1, len(nodessp1))
	for cidsp2, nodessp2  in nodesbycluster_sp2.iteritems():
	    if len(nodessp2) > args.sizecutoff:
		namessp1 = [genenames_sp1[n] for n in nodessp1]
		namessp2 = [genenames_sp2[n] for n in nodessp2]
		count = 0
		for n1 in namessp1:
		    for n2 in namessp2:
			if args.homologene:
			    if len(homdict_sp2[n2.lower()] & homdict_sp1[n1.lower()]) > 0:
				count += 1
			else:
			    if n2.lower() in homdict[n1.lower()]:
				count += 1
		if count > homcount[cidsp1]:
		    homcount[cidsp1] = count
		    max_hom_nets[cidsp1] = (namessp1, namessp2, count, count/float(len(namessp1))) 

print 'Sorting nets by homology count'
sorted_nets = sorted(max_hom_nets.values(), key=lambda x: x[2], reverse=True)

print 'Writing to output file'
args.outfile.write('#Species 1 cluster genes\tSpecies 2 cluster genes\tHomology count\tPercentage of homology\tSize species 1 cluster\t Size species 2 cluster\n')
for nodessp1, nodessp2, count, percentage in sorted_nets:
    args.outfile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (','.join(nodessp1), ','.join(nodessp2), count, percentage, len(nodessp1), len(nodessp2)))
args.outfile.close()


