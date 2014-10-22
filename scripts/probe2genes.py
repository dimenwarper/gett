import sys
import pdb
import pickle
from scipy.stats import stats
from numpy import array
affy2entrez = pickle.load(open(sys.argv[3]))
f = open(sys.argv[1])
o = open(sys.argv[2], 'w')
l = f.readline()
ff = l.strip(' \n').split()
probes = ff[2:]
genecols = {}
for i,p in enumerate(probes):
    if not p in affy2entrez:
        print 'ID not found' + p
        continue
    gene = affy2entrez[p].replace('"','')
    if gene in genecols.keys():
        genecols[gene].append(i)
    else:
        genecols[gene] = [i]
o.write(l[0]+','+l[1]+',')
for i, g in enumerate(genecols):
    o.write(g)
    if i < len(genecols)-1:
        o.write(',')
    else:
        o.write('\n')
print 'Number of probes'
print len(probes)
i = 0
while True:
    i += 1
    l = f.readline()
    if not l:
        break
    fields = l.strip(' \n').split()
    a = array([float(x) for x in fields[2:]])
    o.write(fields[0]+','+fields[1]+',')
    for j, g in enumerate(genecols):
        o.write(str(stats.scoreatpercentile(a[genecols[g]], 50)))
        if j < len(genecols)-1:
            o.write(',')
        else:
            o.write('\n')
    
