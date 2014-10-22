import matplotlib
matplotlib.use('Agg')
import argparse
import pdb
import gett.io
from gett.network_building import tools
import scipy.stats
import gett.network_building.significance
from itertools import chain
from matplotlib.pylab import *
from gett.plotting import manhattan

parser = argparse.ArgumentParser()
parser.add_argument('caseexpfile', metavar='CASE_EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('controlexpfile', metavar='CONTROL_EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('casecommunityfile', metavar='CASE_COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('controlcommunityfile', metavar='CONTROL_COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('snpcoordinatefile', metavar='SNP_COORDINATE_FILE', type=argparse.FileType('r'))
parser.add_argument('controlcoefficientfile', metavar='CASE_COEFFICIENT_FILE', type=argparse.FileType('r'))
parser.add_argument('casecoefficientfile', metavar='CONTROL_COEFFICIENT_FILE', type=argparse.FileType('r'))
parser.add_argument('outfileprefix', metavar='OUTFILE_PREFIX')

args = parser.parse_args()

def get_highest_degree_node(community):
    maxdeg = -1
    node = -1
    degrees = {}
    for edge in community:
	n1 = edge[0]
	n2 = edge[1]
	for n in (n1, n2):
	    if n not in degrees:
		degrees[n] = 1
	    else:
		degrees[n] += 1
    for n in degrees:
	if degrees[n] > maxdeg:
            maxdeg = degrees[n]
	    node = n
    return node

def get_number_of_clusters_by_node(nodesbycluster):
    clustersizebynode = {}
    for cluster, nodes in nodesbycluster.iteritems():
        if len(nodes) >= 5:
	    for node in nodes:
		if node not in clustersizebynode:
		    clustersizebynode[node] = 0
		clustersizebynode[node] += 1
    return clustersizebynode

print 'Parsing expression files'
caseheader, casegenenames, caseMexp = gett.io.read_expression_matrix(args.caseexpfile)
controlheader, controlgenenames, controlMexp = gett.io.read_expression_matrix(args.controlexpfile)
print 'Parsing community files'
casenodesbycluster, caseedgesbycluster = gett.io.read_community(args.casecommunityfile)
controlnodesbycluster, controledgesbycluster = gett.io.read_community(args.controlcommunityfile)

allcontroledges = set([x for x in chain(*controledgesbycluster.values())])
allcaseedges = set([x for x in chain(*caseedgesbycluster.values())])
allnodes = range(len(casegenenames))

print 'Building snp2coordinates dictionary'
snp2coordinates = {}
line = args.snpcoordinatefile.readline()
while line:
    fields = line.strip().split('\t')
    snp2coordinates[fields[1]] = [fields[0], fields[3]]
    line = args.snpcoordinatefile.readline()

print 'Getting coefficients'
def parse_coeffs(coeff_file, snp2coordinates):
    coeffs = {}
    coeff_labels = {}
    line = coeff_file.readline()
    while line:
	fields= line.strip().split('\t')
	clustid = float(fields[0])
	coeffs[clustid] = [0]*len(fields[1:])
	for i, f in enumerate(fields[1:]):
	    label, coeff = f.split(':')
	    chrom, coord = snp2coordinates[label]
	    coeffs[clustid][i] = [label, chrom, coord, float(coeff)] 
	line = coeff_file.readline()
    return coeffs, coeff_labels

casecoeffs, casecoefflabels = parse_coeffs(args.casecoefficientfile, snp2coordinates)
controlcoeffs, controlcoefflabels = parse_coeffs(args.controlcoefficientfile, snp2coordinates)

def get_genetic_controller_coeffs(clust_list, coeffs):
    snps = {}
    for c in clust_list:
	if c not in coeffs:
	    print '%s not in coeffs' % c
	    continue
	for snpid, chrom, coord, coeff in coeffs[c]:
	    if snpid not in snps:
		snps[snpid] = [chrom, float(coord), abs(coeff)]
	    else:
		snps[snpid][2] += abs(coeff)
    return snps

print 'Getting topology properties'
print 'Getting number of communities by gene'
gene_topology_list = []
case_clusters_by_node = get_number_of_clusters_by_node(casenodesbycluster)
control_clusters_by_node = get_number_of_clusters_by_node(controlnodesbycluster)
for i in xrange(len(casegenenames)):
    if i in case_clusters_by_node and i in control_clusters_by_node:
	name = casegenenames[i]
	gene_topology_list.append([name, case_clusters_by_node[i], control_clusters_by_node[i]])

print 'Sorting topology list by differential topology properties'
case_sorted_topology_list = sorted(gene_topology_list, key=lambda entry: entry[1] - entry[2], reverse=True)
control_sorted_topology_list = sorted(gene_topology_list, key=lambda entry: entry[2] - entry[1], reverse=True)
case_topology_genes = [casegenenames.index(x[0]) for x in case_sorted_topology_list[:100]]
control_topology_genes = [casegenenames.index(x[0]) for x in control_sorted_topology_list[:100]]
case_topology_clusts = [n for n in casenodesbycluster if n in case_topology_genes]
control_topology_clusts = [n for n in controlnodesbycluster if n in control_topology_genes]

print 'Obtaining genetic controllers for these clusters'
case_controllers_topology = get_genetic_controller_coeffs(case_topology_clusts, casecoeffs)
control_controllers_topology = get_genetic_controller_coeffs(control_topology_clusts, controlcoeffs)

print 'Writing to outfiles'
topfile = open(args.outfileprefix + 'cases__by_topology.txt', 'w')
topfile.write('#Gene\tMembership clusters in cases\tMembership clusters in controls\n')
gett.io.write_list(topfile, case_sorted_topology_list)

topfile = open(args.outfileprefix + 'control__by_topology.txt', 'w')
topfile.write('#Gene\tMembership clusters in cases\tMembership clusters in controls\n')
gett.io.write_list(topfile, control_sorted_topology_list)

print 'Plotting manhattan plot of controllers'

figure(1)
ax = axes()
manhattan(case_controllers_topology.values(), ax, lines=True) 
savefig(args.outfileprefix + 'cases_topology_controllers.png')
clf()
ax = axes()
manhattan(control_controllers_topology.values(), ax, lines=True) 
savefig(args.outfileprefix + 'controls_topology_controllers.png')


