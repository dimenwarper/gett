from numpy import * 
import pdb

def read_genotype_matrix(genmatfile, skip_fields=6, sep=' ', restrict_samples=[]):
    labels = []
    genmat = []
    line = genmatfile.readline()
    while line:
	fields = line.strip().split(sep)
	if len(restrict_samples) == 0 or fields[0] in restrict_samples:
	    genmat.append([float(d) for d in fields[skip_fields:]])
	    labels.append(fields[:skip_fields])
	line = genmatfile.readline()
    return labels, array(genmat)

def read_expression_matrix(expfile, sep='\t'):
    header = expfile.readline().strip().split(sep)
    genenames = []
    Mexp = []
    line = expfile.readline()
    while line:
	fields = line.strip().split(sep)
	genenames.append(fields[0])
	a = [float(f) for f in fields[1:]]
	Mexp.append(a)
	line = expfile.readline()
    return header, genenames, array(Mexp)

def read_community(communityfile, sep='\t'):
    nodesbycluster = {}
    edgesbycluster = {}
    for line in communityfile.readlines():
	fields = line.strip().split(sep)
	e = (int(fields[1]), int(fields[2]))
	if e[0] != e[1]:
	    cluster = float(fields[0])
	    if cluster in nodesbycluster:
		nodesbycluster[cluster].add(e[0])
		nodesbycluster[cluster].add(e[1])
		edgesbycluster[cluster].append(e)
	    else:
		nodesbycluster[cluster] = set([e[0], e[1]])
		edgesbycluster[cluster] = [e]
    return nodesbycluster, edgesbycluster

def write_list(outfile, d, sep='\t'):
    for l in d:
	outfile.write(sep.join((str(x) for x in l)) + '\n')

def write_dict(outfile, d, split_lists=False, sep='\t'):
    for k, v in d.iteritems():
	if split_lists:
	    if hasattr(k, '__iter__'):
		l = sep.join((str(x) for x in k))
	    else:
		l = str(k)
	    if hasattr(v, '__iter__'):
		outfile.write(l + sep + sep.join((str(x) for x in v)) + '\n')
	    else:
		outfile.write(l + sep + str(v) + '\n')
	else:
	    outfile.write(str(k) + sep + str(v) + '\n')

def read_dict(dfile, numfieldsid=1, apply_for_keys=lambda x: x, apply_for_values=lambda x:x):
    d = {}
    line = dfile.readline()
    while line:
	fields = line.strip().split('\t')
	if numfieldsid > 1:
	    d[tuple(apply_for_keys(fields[:numfieldsid]))] = apply_for_values(fields[numfieldsid:])
        line = dfile.readline()
    return d

def snp2coordinate(snp_coordinate_file):
    snp2coordinates = {}
    line = snp_coordinate_file.readline()
    while line:
	fields = line.strip().split('\t')
	snp2coordinates[fields[1]] = (fields[0].replace('23', 'X'), int(fields[3]))
	line = snp_coordinate_file.readline()
    return snp2coordinates

def parse_coeff_file(coefficient_file, snp2coordinates):
    coeffs = {}
    coeff_labels = {}
    coeffs_in_coords = {}
    coeff_snpids = {}
    line = coefficient_file.readline()
    while line:
	fields= line.strip().split('\t')
	clustid = float(fields[0])
	coeffs[clustid] = [0]*len(fields[1:])
	coeffs_in_coords[clustid] = []
	coeff_labels[clustid] = ['']*len(fields[1:])
	coeff_snpids[clustid] = ['']*len(fields[1:])
	for i, f in enumerate(fields[1:]):
	    label, coeff = f.split(':')
	    coeff_snpids[clustid][i] = label
	    if label in snp2coordinates:
		coeff_labels[clustid][i] = 'chr%s:%s' % (snp2coordinates[label][0], snp2coordinates[label][1])
		coeffs_in_coords[clustid].append(list(snp2coordinates[label]) + [float(coeff)])
	    else:
		coeff_labels[clustid][i] = label
	    coeffs[clustid][i] = float(coeff) 
	line = coefficient_file.readline()
    return coeffs, coeff_labels, coeff_snpids, coeffs_in_coords






