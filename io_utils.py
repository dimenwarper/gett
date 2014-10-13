from numpy import * 
import pdb
from collections import defaultdict
import pandas as pd

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


def read_expression_matrix(*args, **kwargs):
    kwargs['as_array'] = True
    return read_trait_matrix(*args, **kwargs)

def read_trait_matrix(tfile, sep='\t', get_rid_of_NAs=True, merge_same_ids=False, as_array=False, transpose=False):
    header = tfile.readline().strip().split(sep)
    genenames = []
    M = []
    line = tfile.readline()
    numfields = len(line.strip().split(sep))
    while line:
	fields = line.strip().split(sep)
	a = [float("nan") if f == 'NA' or f == '' else float(f) for f in fields[1:]]
        if a:
            M.append(a)
            genenames.append(fields[0])
	line = tfile.readline()
    M = array(M)
    if transpose:
        M = M.T
        tmp = header
        header = genenames
        genenames = tmp
    if get_rid_of_NAs:
        good_cols = [i for i in range(M.shape[1]) if sum(isnan(M[:,i])) == 0 ] 
	M = M[:, good_cols]
        header = [header[i] for i in good_cols]
    else:
	M = nan_to_num(M)
    if merge_same_ids:
        gindices = defaultdict(list)
        for i, g in enumerate(genenames):
            gindices[g].append(i)
        true_size = len(gindices)
        new_M = zeros([true_size, M.shape[1]])
        for i, g in enumerate(gindices):
            new_M[i,:] = median(M[gindices[g],:], axis=0)
        del(M)
        M = new_M
        genenames = gindices.keys()
    if as_array:
        return header, genenames, M
    else:
        return pd.DataFrame(M, index=genenames, columns=header)

# This is the old way of reading community files; it's now deprecated
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
    for c, nodes in nodesbycluster.iteritems():
        nodesbycluster[c] = list(nodes)
    return nodesbycluster, edgesbycluster

# Use this instead
def read_communities(communityfile, edgefile=None, sep='\t'):
    nodesbycluster = read_dict(communityfile, sep=sep, header=False)
    if edgefile is not None:
        edgesbycluster = defaultdict(list)
        for line in edgefile.readlines():
            fields = line.strip().split(sep)
            e = (int(fields[0]), int(fields[1]))
            for c, nodes in nodesbycluster:
                if e[0] in nodes and e[1] in nodes:
                    edgesbycluster[c].append(e)
        return nodesbycluster, edgesbycluster
    else:
        return nodesbycluster

def write_communities(communityfile, d, sep='\t', type='vector'):
    if type == 'vector':
        # d is a matrix with the community membership vectors
        # each row is a community, each column is a node memberships
        ddict = defaultdict(list)
        for i in xrange(d.shape[0]):
            for j in xrange(d.shape[1]):
                if d[i, j] != 0:
                    ddict[i].append(j)
    elif type == 'dict':
        ddict = d
    else:
        raise ValueError('Invalid type for writing communities')
    write_dict(communityfile, ddict, sep=sep, split_lists=True)

def write_edges(edgefile, M, sep='\t', names=None, directed=False, weighted=True):
    if names is not None:
        get_name = lambda i: names[i]
    else:
        get_name = lambda i: i
    if directed:
        for i in xrange(M.shape[0]):
            for j in xrange(M.shape[1]):
                if M[i,j] != 0:
                    if weighted:
                        edgefile.write('%s%s%s%s%s\n' % (get_name(i), sep, get_name(j), sep, M[i,j]))
                    else:
                        edgefile.write('%s%s%s\n' % (get_name(i), sep, get_name(j)))
    else:
        for i in xrange(M.shape[0]):
            for j in xrange(i+1, M.shape[1]):
                if M[i,j] != 0:
                    if weighted:
                        edgefile.write('%s%s%s%s%s\n' % (get_name(i), sep, get_name(j), sep, M[i,j]))
                    else:
                        edgefile.write('%s%s%s\n' % (i, sep, j))

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

def read_edges(dfile, sep='\t', indices=None, symmetric=False):
    edges = {}
    index_cache = {}
    for l in dfile.readlines():
        if l[0] != '#':
            fields = l.strip().split(sep)
            if indices is not None:
                if fields[0] not in index_cache:
                    f1 = indices.index(fields[0])
                    index_cache[fields[0]] = f1
                else:
                    f1 = index_cache[fields[0]]
                if fields[1] not in index_cache:
                    f2 = indices.index(fields[1])
                    index_cache[fields[1]] = f2
                else:
                    f2 = index_cache[fields[1]]
                edges[(f1, f2)] = float(fields[2])
                if symmetric:
                    edges[(f2, f1)] = float(fields[2])
            else:
                edges[(fields[0], fields[1])] = float(fields[2])
                if symmetric:
                    edges[(fields[1], fields[0])] = float(fields[2])
    return edges
def read_dict(dfile, numfieldsid=1, apply_for_keys=lambda x: x, apply_for_values=lambda x:x, sep='\t', header=True):
    d = {}
    if header:
        header = dfile.readline().strip().split(sep)
    line = dfile.readline()
    while line:
        if line[0] != '#':
            fields = line.strip().split(sep)
            if numfieldsid > 1:
                d[tuple(apply_for_keys(fields[:numfieldsid]))] = apply_for_values(fields[numfieldsid:])
            else:
                d[apply_for_keys(fields[0])] = apply_for_values(fields[numfieldsid:])
        line = dfile.readline()
    if header:
        return header, d
    else:
        return d

def snp2coordinate(snp_coordinate_file, getlist=False):
    snp2coordinates = {}
    line = snp_coordinate_file.readline()
    snplist = []
    while line:
	fields = line.strip().split('\t')
        if getlist:
            snplist.append((fields[0].replace('23', 'X'), int(fields[3])))
	snp2coordinates[fields[1]] = (fields[0].replace('23', 'X'), int(fields[3]))
	line = snp_coordinate_file.readline()
    if getlist:
        return snp2coordinates, snplist
    else:
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

def read_coord_file(f, delim='\t', chrcol=0, poscol=1, endcol=None):
    line = f.readline()
    coords = defaultdict(list)
    while line:
	fields = line.strip().split(delim)
	if not endcol:
	    chrom = fields[chrcol].upper().replace('CHR','')
	    coords[chrom].append(int(fields[poscol]))
	else:
	    chrom = fields[chrcol].upper().replace('CHR','')
	    coords[chrom].append([int(fields[poscol]), int(fields[endcol])])
	line = f.readline()
    return coords

def save_step(objs, names, suffix='', type='dataframe'):
    new_names = []
    for obj, name in zip(objs, names):
        new_name = '%s%s.txt' % (name[:name.rfind('.')], suffix)
        if type == 'dataframe':
            print 'Saving dataframe %s' % name
            obj.to_csv(open(new_name, 'w'), sep='\t')
            new_names.append(new_name)
    return new_names
