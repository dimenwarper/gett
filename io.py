from numpy import * 
import pdb

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
    line = dfile.readlines()
    while line:
	fields = line.strip().split('\t')
	if numfieldsid > 1:
	    d[tuple(apply_for_keys(fields[:numfieldsid]))] = apply_for_values(fields[numfieldsid:])
    return d

