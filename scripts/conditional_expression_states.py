import matplotlib
#matplotlib.use('Agg')
import argparse
import pdb
import ett.io
from ett.network_building import tools
import scipy.stats
import ett.network_building.significance
from itertools import chain
from matplotlib.pylab import *
from ett.plotting import manhattan
from scipy.stats.kde import gaussian_kde
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('caseexpfile', metavar='CASE_EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('controlexpfile', metavar='CONTROL_EXPRESSION_FILE', type=argparse.FileType('r'))
parser.add_argument('casecommunityfile', metavar='CASE_COMMUNITY_FILE', type=argparse.FileType('r'))
parser.add_argument('--genenames', type=str, default=None)
parser.add_argument('--nsigma', default=2., type=float)
parser.add_argument('outfileprefix', metavar='OUTFILE_PREFIX')

args = parser.parse_args()

def get_gene_states(regindices, geneindices, baselines, sigmas):
    regdict = {'upreg':set(), 'nochange':set(), 'downreg':set()}
    for g in geneindices:
        meanexp = caseMexp[g,regindices].mean() 
        if meanexp > baselines[g] + args.nsigma * sigmas[g]:
            regdict['upreg'].add(g)
        elif meanexp < baselines[g] - args.nsigma * sigmas[g]:
            regdict['downreg'].add(g)
        else:
            regdict['nochange'].add(g)
    return regdict

def mode_discovery(samp):
    kde = gaussian_kde(samp)
    kde.covariance_factor = lambda: kde.silverman_factor()/1.7
    kde._compute_covariance()
    step = (max(samp) - min(samp))/100.
    prevval = kde(min(samp))
    prevx = min(samp)
    modes = []
    ascending = True
    r = arange(min(samp), max(samp), step)
    for x in r:
        if kde(x) <= prevval and ascending and kde(x) > 0.15:
            modes.append(prevx)
            ascending = False
        if kde(x) >  prevval:
            ascending = True
        prevx = x
        prevval = kde(x)
    #print modes
    #hist(samp, 50, color='b', alpha=0.6, normed=1)
    #plot(r, kde(r), 'r')
    #show()
    return modes

print 'Parsing expression files'
caseheader, casegenenames, caseMexp = ett.io.read_expression_matrix(args.caseexpfile)
controlheader, controlgenenames, controlMexp = ett.io.read_expression_matrix(args.controlexpfile)
print 'Parsing community files'
casenodesbycluster, caseedgesbycluster = ett.io.read_community(args.casecommunityfile)

all_case_nmodes = {}
all_control_nmodes = {}

def conditional_states(genename):
    controlidx = controlgenenames.index(genename)
    caseidx = casegenenames.index(genename)
    caseindices = []
    for c, nodes in casenodesbycluster.iteritems():
        if caseidx in nodes:
            caseindices += nodes
    caseindices = list(set(caseindices))
    print 'Doing %s' % genename
    
    print 'Testing multimodality'

    modes_controls = mode_discovery(controlMexp[controlidx,:])
    modes_cases = mode_discovery(caseMexp[caseidx,:])

    all_control_nmodes[genename] = len(modes_controls)
    all_case_nmodes[genename] = len(modes_cases)

    print 'Getting conditional expression states'

    baseline = controlMexp[controlidx,:].mean()
    sigma = controlMexp[controlidx,:].std()

    baselines = controlMexp.mean(axis=1)
    sigmas = controlMexp.std(axis=1)

    upregindices = [i for i in xrange(caseMexp.shape[1]) if caseMexp[caseidx, i] > baseline + args.nsigma * sigma]
    downregindices = [i for i in xrange(caseMexp.shape[1]) if caseMexp[caseidx, i] < baseline - args.nsigma * sigma]
    if len(upregindices) == 0 or len(downregindices) == 0:# or (len(modes_cases) == 1 and len(modes_controls) == 1):
        return
    else:
        print 'Found conditional states of gene %s for sigma change treshold %s!!' % (genename, args.nsigma)
    upregdict = {'upreg':set(), 'downreg':set()}
    downregdict = {'upreg':set(), 'downreg':set()}

    upregdict = get_gene_states(upregindices, caseindices, baselines, sigmas)
    downregdict = get_gene_states(downregindices, caseindices, baselines, sigmas)

    outfile = open(args.outfileprefix + '%s_expression_states.txt' % genename.replace('/','_'), 'w')
    outfile.write('Number of modes in controls: %s\n' % len(modes_controls))
    outfile.write('Number of modes in cases: %s\n' % len(modes_cases))
    outfile.write('Modes in controls: %s\n' % modes_controls)
    outfile.write('Modes in cases: %s\n' % modes_cases)
    outfile.write('Number of genes in the neighborhood of %s: %s\n' % (genename, len(caseindices)))
    outfile.write('For upregulated %s\n' % genename)
    outfile.write('Number of samples with upregulated %s: %s\n' % (genename, len(upregindices)))
    outfile.write('Upregulated genes: %s\n' % ','.join([casegenenames[i] for i in upregdict['upreg']]))
    outfile.write('Downregulated genes: %s\n' % ','.join([casegenenames[i] for i in upregdict['downreg']]))
    outfile.write('Genes with no change: %s\n' % ','.join([casegenenames[i] for i in upregdict['nochange']]))
    outfile.write('For downregulated %s\n' % genename)
    outfile.write('Number of samples with downregulated %s: %s\n' % (genename, len(downregindices)))
    outfile.write('Upregulated genes: %s\n' % ','.join([casegenenames[i] for i in downregdict['upreg']]))
    outfile.write('Downregulated genes: %s\n' % ','.join([casegenenames[i] for i in downregdict['downreg']]))
    outfile.write('Genes with no change: %s\n' % ','.join([casegenenames[i] for i in downregdict['nochange']]))
    outfile.close()

if args.genenames:
    genenames = args.genenames.strip().split(',')
else:
    genenames = casegenenames

for g in genenames:
    conditional_states(g)
pickle.dump(all_case_nmodes, open(args.outfileprefix + '/cases_nmodes.pickle', 'w'))
pickle.dump(all_control_nmodes, open(args.outfileprefix + '/controls_nmodes.pickle', 'w'))
