from collections import defaultdict
"""
These fields correspond to biogrid tab2 format columns
"""
biogrid_fields = {'symbol':[7,8], 'publication':14, 'type':12}
def build_biogrid_dict(dbfile, key='symbol'):
    line = dbfile.readline()
    interactions = {}
    publications = defaultdict(list)
    while line:
	if line.strip()[0] != '#':
	    fields = line.strip().split('\t')
	    a = fields[biogrid_fields[key][0]].strip()
	    b = fields[biogrid_fields[key][1]].strip()
	    if (a,b) in interactions: 
		interactions[(a,b)]['type'].append(fields[biogrid_fields['type']])
	    elif (b,a) in interactions:
		interactions[(b,a)]['type'].append(fields[biogrid_fields['type']])
	    else:
		interactions[(a,b)] = {'type':[fields[biogrid_fields['type']]]}
	    publications[(a,b)].append(fields[biogrid_fields['publication']])
	line = dbfile.readline()
    for a,b in publications.keys():
	publications[(b,a)] = publications[(a,b)]
    for a,b in interactions.keys():
	interactions[(b,a)] = interactions[(a,b)]
    return interactions, publications

def build_gtex_dict(dbfile):
    line = dbfile.readline()
    res = {}
    while line:
	if line.strip()[0] != '#':
	    fields = line.strip().split('\t')
	    res[(fields[3], int(fields[4]))] = fields[:3] + fields[5:]
	line = dbfile.readline()
    return res


