from numpy import array
from collections import defaultdict
def guess_type(row):
    try:
        return [float(x) for x in row], 'float'
    except ValueError:
        return row, 'string'

def read_data_table(file, header=True, delimiter=','):
    line = file.readline()
    d = defaultdict(list)
    a = []
    if header:
	h = line.strip(' \n').split(delimiter)
	line = file.readline()
    else:
	h = []
    while line:
	f, type = guess_type(line.strip(' \n').split(delimiter))
	if type == 'float':
	    a.append(f)
	if not h:
	    h = ['V%s' % i for i in range(len(f))]
	#for i, key in enumerate(h):
	#    d[key].append(f[i])
        line = file.readline()
    return d, array(a) 

