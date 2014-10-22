import argparse
import pdb
import gett.io
from gett.network_building import tools
import scipy.stats
import gett.network_building.significance
from itertools import chain

parser = argparse.ArgumentParser()
parser.add_argument('caseexpfile', metavar='CASE_EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('controlexpfile', metavar='CONTROL_EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('casecommunityfile', metavar='CASE_COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('controlcommunityfile', metavar='CONTROL_COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('snp_coordinate_file', metavar='SNP_COORDINATE_FILE', type=argparse.FileType('r'))
parser.add_argument('coefficient_file', metavar='COEFFICIENT_FILE', type=argparse.FileType('r'))
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
def preservation_metric_wrapper(edges):
    return tools.preservation_metric(edges, allcontroledges)

print 'Building snp2coordinates dictionary'
snp2coordinates = {}
line = args.snp_coordinate_file.readline()
while line:
    fields = line.strip().split('\t')
    snp2coordinates[fields[1]] = [fields[0], fields[3]]
    line = args.snp_coordinate_file.readline()

print 'Getting coefficients'
coeffs = {}
coeff_labels = {}
line = args.coefficient_file.readline()
while line:
    fields= line.strip().split('\t')
    clustid = float(fields[0])
    coeffs[clustid] = [0]*len(fields[1:])
    for i, f in enumerate(fields[1:]):
	label, coeff = f.split(':')
        chrom, coord = snp2coordinates[label]
	coeffs[clustid][i] = [label, chrom, coord, float(coeff)] 
    line = args.coefficient_file.readline()

def get_genetic_controller_coeffs(clust_list):
    snps = {}
    for c in clust_list:
	if c not in coeffs:
	    print '%s not in coeffs' % c
	    continue
	for snpid, chrom, coord, coeff in coeffs[c]:
	    if snpid not in snps:
		snps[snpid] = [chrom, coord, abs(coeff)]
	    else:
		snps[snpid][2] += abs(coeff)
    return snps
print 'Calculating SAM d statistics'
samd = gett.network_building.significance.SAM_d(controlMexp, caseMexp)
print 'Obtaining significant clusters by preservation metric'
sig_by_pres = gett.network_building.significance.significance_by_randomiziation(allnodes, allcaseedges, casenodesbycluster, caseedgesbycluster, preservation_metric_wrapper, size_cutoff=10)
print 'Obtaining genetic controllers of these clusters'
controllers_pres = get_genetic_controller_coeffs([item[0] for item in sig_by_pres])
print 'Ordering these clusters by SAM d statistic'
for item in sig_by_pres:
    item.append(samd[list(casenodesbycluster[item[0]])].mean())
sorted_sig_by_pres = sorted(sig_by_pres, key=lambda item: abs(item[2]), reverse=True)
print 'Obtaining significant clusters by inverse preservation metric'
sig_by_invpres = gett.network_building.significance.significance_by_randomiziation(allnodes, allcaseedges, casenodesbycluster, caseedgesbycluster, preservation_metric_wrapper, compare=lambda randmeas , meas: randmeas < meas, size_cutoff=10)
print 'Obtaining genetic controllers of these clusters'
controllers_invpres = get_genetic_controller_coeffs([item[0] for item in sig_by_invpres])
print 'Ordering these clusters by SAM d statistic'
for item in sig_by_invpres:
    item.append(samd[list(casenodesbycluster[item[0]])].mean())
sorted_sig_by_invpres = sorted(sig_by_invpres, key=lambda item: abs(item[2]), reverse=True)


print 'Reading OMIM'
all_omim_genes = gett.network_building.significance.all_OMIM_genes()
print 'Tagging case genes by OMIM'
omim_genes = gett.network_building.significance.tag_by_genenames(range(len(casegenenames)), casegenenames, all_omim_genes)
print 'Tagging case genes by differential expression'
diff_genes = gett.network_building.significance.tag_by_differential_expression(caseMexp, controlMexp)
print 'Obtaining significant clusters by OMIM'
sig_by_omim = gett.network_building.significance.significance_by_enrichment(casenodesbycluster, range(len(casegenenames)), omim_genes, size_cutoff=5)
print 'Obtaining genetic controllers of these clusters'
controllers_omim = get_genetic_controller_coeffs([x[0] for x in sig_by_omim])
print 'Obtaining significant clusters by differential expression'
sig_by_diff = gett.network_building.significance.significance_by_enrichment(casenodesbycluster, range(len(casegenenames)), diff_genes, size_cutoff=5)
print 'Obtaining genetic controllers of these clusters'
controllers_diff = get_genetic_controller_coeffs([x[0] for x in sig_by_diff])

for s in (sig_by_omim, sig_by_diff, sorted_sig_by_pres, sorted_sig_by_invpres):
    for i, item in enumerate(s):
	 s[i] =  list(item) + [casegenenames[get_highest_degree_node(caseedgesbycluster[item[0]])], ','.join([casegenenames[n] for n in casenodesbycluster[item[0]]])] 

print 'Getting topology properties'
print 'Getting community hubs'
highest_deg_nodes_cases = [casegenenames[get_highest_degree_node(v)] for k, v in caseedgesbycluster.iteritems()]
highest_deg_nodes_controls = [controlgenenames[get_highest_degree_node(v)] for k, v in controledgesbycluster.iteritems()]
gene_topology_list = []
case_clusters_by_node = get_number_of_clusters_by_node(casenodesbycluster)
control_clusters_by_node = get_number_of_clusters_by_node(controlnodesbycluster)
print 'Getting number of clusters by node'
for i in xrange(len(casegenenames)):
    if i in case_clusters_by_node and i in control_clusters_by_node:
	name = casegenenames[i]
	is_root_in_cases = 0
	if name in highest_deg_nodes_cases:
	    is_root_in_cases = 1
	is_root_in_controls = 0
	if name in highest_deg_nodes_controls:
	    is_root_in_controls = 1
	case_deg = case_clusters_by_node[i]
	control_deg = control_clusters_by_node[i]
	gene_topology_list.append([name, case_deg, is_root_in_cases, control_deg, is_root_in_controls])

print 'Sorting topology list by differential topology properties'
sorted_topology_list = sorted(gene_topology_list, key=lambda entry: 0.5*abs(entry[3] - entry[1]) + 0.5*abs(entry[2] - entry[4]), reverse=True)
topology_genes = [casegenenames.index(x[0]) for x in sorted_topology_list[:10]]
topology_clusts = [n for n in casenodesbycluster if n in topology_genes]
print 'Obtaining genetic controllers for these clusters'
controllers_topology = get_genetic_controller_coeffs(topology_clusts)

print 'Writing to outfiles'
gett.io.write_list(open(args.outfileprefix + '_by_OMIM.txt', 'w'), sig_by_omim)
gett.io.write_list(open(args.outfileprefix + '_by_OMIM_controllers.txt', 'w'), controllers_omim.values())
gett.io.write_list(open(args.outfileprefix + '_by_differential.txt', 'w') , sig_by_diff)
gett.io.write_list(open(args.outfileprefix + '_by_preservation.txt', 'w') , sorted_sig_by_pres)
gett.io.write_list(open(args.outfileprefix + '_by_inverse_preservation.txt', 'w') , sorted_sig_by_invpres)
gett.io.write_list(open(args.outfileprefix + '_by_differential_controllers.txt', 'w'), controllers_diff.values())
topfile = open(args.outfileprefix + '_by_topology.txt', 'w')
topfile.write('#Gene\tMembership clusters in cases\tIs hub in cases\tMembership clusters in controls\tIs hub in controls\n')
gett.io.write_list(topfile, sorted_topology_list)
gett.io.write_list(open(args.outfileprefix + '_by_topology_controllers.txt', 'w'), controllers_topology.values())
gett.io.write_list(open(args.outfileprefix + '_by_preservation_controllers.txt', 'w') , controllers_pres.values())
gett.io.write_list(open(args.outfileprefix + '_by_inverse_preservation_controllers.txt', 'w') , controllers_invpres.values())

