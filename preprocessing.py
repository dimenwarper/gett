import pandas as pd
import pdb
import numpy as np
import scipy.stats.mstats
from itertools import chain
import statsmodels.api as sm

def correct_covariates(Dtrait, Dcov, variables):
    Dcomb = pd.merge(Dtrait.T, Dcov.T, left_index=True, right_index=True).T
    Dcorr = Dtrait.copy()
    traits = Dtrait.columns.values.tolist()
    for v in variables:
        print 'Correcting for %s' % v
        for i in Dtrait.index:
            #rlm_model = sm.RLM(Dcomb.loc[i,:], Dcomb.loc[v,:])
            rlm_model = sm.RLM(Dcomb.loc[v,:], Dcomb.loc[i,:])
            rlm_results = rlm_model.fit()
            Dcorr.loc[i,:] = rlm_results.resid
    return Dcorr


def select_traits_by_variance(Dtraits, frac=0.25):
    trait_vars = np.zeros([Dtraits[0].shape[0]])
    for i in xrange(Dtraits[0].shape[0]):
        data = [x for x in chain(*[D.values[i,:].tolist() for D in Dtraits])]
        trait_vars[i] = np.array(data).std()**2
    cutoff = scipy.stats.mstats.mquantiles(trait_vars, prob=[1-frac])[0]
    return [D.ix[np.where(trait_vars > cutoff)[0],:] for D in Dtraits]

def zscores(D):
    return (D - D.mean())/D.std()
