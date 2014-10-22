from suds.client import Client
import gett.io
from gett.settings import * 


def ENCODEannotate(snps, interval_thd=10):
    regdb = {}
    print 'Reading RegulomeDB files'
    regdb['cat1'] = gett.io.read_coord_file(open(REGULOME_DB_CAT1))
    regdb['cat2'] = gett.io.read_coord_file(open(REGULOME_DB_CAT2))
    regdb['cat3'] = gett.io.read_coord_file(open(REGULOME_DB_CAT3))
    res = {'cat1':[], 'cat2':[], 'cat3':[]}
    names = ['cat1', 'cat2', 'cat3']
    print 'Starting annotation'
    totsnps = float(len(snps))
    currperc = 0
    for j, s in enumerate(snps):
	perccomp = int(10*j/totsnps)
	if perccomp > currperc:
	    currperc = perccomp
	    print 'Completed: %s%%' % (currperc*10)
	for i in xrange(3):
	    for pos in regdb[names[i]][s[0]]:
		if s[1] >= pos - interval_thd and s[1] <= pos + interval_thd:
		    res[names[i]].append(s)
    return res



def DAVIDannotate(genelist, idType='ENTREZ_GENE_ID', bglist='', bgName = 'Background1',listName='List1', species='Homo sapiens', \
                  category = 'abcd,BBID,BIOCARTA,COG_ONTOLOGY,INTERPRO,KEGG_PATHWAY,OMIM_DISEASE,PIR_SUPERFAMILY,SMART,SP_PIR_KEYWORDS,UP_SEQ_FEATURE', thd=0.01, ct=2):
    flagBg = len(bglist) > 0
    if flagBg:
	print 'Use file background.'
    else:
        print 'Use default background.'
    client = Client('http://david.abcc.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl')
    print 'User Authentication:',client.service.authenticate('tsuname@stanford.edu')
    listType = 0
    print 'Percentage mapped(list):', client.service.addList(','.join(genelist),idType,listName,listType)
    if flagBg:
        listType = 1
        print 'Percentage mapped(background):', client.service.addList(','.join(bglist),idType,bgName,listType)
    print 'Use categories:', client.service.setCategories(category)
    chartReport = client.service.getChartReport(thd,ct)
    chartRow = len(chartReport)
    print 'Total chart records:',chartRow
    resdict = {}
    dictlabels = ['category', 'pval', 'fold', 'benjamini', 'FDR']
    for row in chartReport:
	rowDict = dict(row)
	termName = str(rowDict['termName'])
	categoryName = str(rowDict['categoryName'])
	ease = str(rowDict['ease'])
	foldEnrichment = str(rowDict['foldEnrichment'])
	benjamini = str(rowDict['benjamini'])
	FDR = str(rowDict['afdr'])
	rowList = [categoryName,ease,foldEnrichment,benjamini,FDR]
	resdict[termName] = rowList
    return resdict, dictlabels

        
