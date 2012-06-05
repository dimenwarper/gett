import argparse
import os
from pebl import data
from pebl import network
from pebl.learner import greedy

parser = argparse.ArgumentParser()
parser.add_argument('directory', metavar='DIR', type=str)
parser.add_argument('prefix', metavar='OUTPREFIX', type=str)
parser.add_argument('start', metavar='FROM', type=int)
parser.add_argument('end', metavar='TO', type=int)


args = parser.parse_args()

for f in os.listdir(args.directory)[args.start:args.end]:
    if 'struct' in f:
	continue
    structfile = open(args.directory + '/' + f.replace('.txt', '_struct.txt'))
    peblfile = open(args.directory + '/' + f)
    nodenames = peblfile.readline().strip().split('\t')
    peblfile.close()
    if len(nodenames) > 30:
	continue
    nodes = [data.Variable(name) for name in nodenames]
    edges = [[int(x) for x in l.strip().split('\t')] for l in structfile.readlines()]
    print 'Doing %s' % f
    print nodes
    print edges
    net = network.Network(nodes, edges=edges)
    dataset = data.fromfile(args.directory + '/' + f)
    try:
	dataset.discretize()
	if len(nodenames) <= 10:
	    learner = greedy.GreedyLearner(dataset, seed=net)
	else:
	    learner = greedy.GreedyLearner(dataset)
	res = learner.run()
#    res.outdir = args.directory + '/'
	res.tohtml(args.prefix + '/' + f.replace('.txt', '_html'))
    except Exception as e:
        print 'Could not process %s: exception was %s' % (f, e)

