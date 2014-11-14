from __future__ import division
import sys
import pandas as pd
import pdb
import numpy as np
import scipy.stats
import statsmodels.api as sm
from scipy.stats import zscore
from itertools import chain
from matplotlib.pylab import *
from numpy.linalg import lstsq
from scipy import interpolate


def correct_covariates(Dtrait, Dcov, variables):
    Dcomb = pd.merge(Dtrait.T, Dcov.T, left_index=True, right_index=True).T
    Dcorr = Dtrait.copy()
    traits = Dtrait.columns.values.tolist()
    print 'Correcting for %s' % variables
    for idx, i in enumerate(Dtrait.index):
        sys.stdout.write('\rTrait %d of %d' % (idx, Dtrait.shape[0]))
        sys.stdout.flush()
        if len(variables) == 1:
            rlm_model = sm.RLM(Dcomb.loc[i,:], zscore(array(Dcomb.loc[variables,:]).T))
        else:
            rlm_model = sm.RLM(Dcomb.loc[i,:], zscore(array(Dcomb.loc[variables,:]).T, axis=0))
        rlm_results = rlm_model.fit()
        Dcorr.loc[i,:] = rlm_results.resid
        """
        if idx > 1:
            f, axarr = subplots(3,2)
            axarr[0,0].scatter(Dtrait.loc['EIF1AY',:], Dtrait.loc['OSBP', :])
            axarr[0,1].scatter(Dcorr.loc['EIF1AY',:], Dcorr.loc['OSBP', :])
            axarr[1,0].hist([x for x in Dtrait.loc['EIF1AY',:] if not isnan(x)])
            axarr[1,1].hist([x for x in Dcorr.loc['EIF1AY',:] if not isnan(x)])
            axarr[2,0].hist([x for x in Dtrait.loc['OSBP',:] if not isnan(x)])
            axarr[2,1].hist([x for x in Dcorr.loc['OSBP',:] if not isnan(x)])
            f2, axarr2 = subplots(3,2)
            axarr2[0,0].scatter(Dcomb.loc['gender',:], Dcomb.loc['OSBP', :])
            axarr2[1,0].scatter(Dcomb.loc['age',:], Dcomb.loc['OSBP', :])
            axarr2[2,0].scatter(Dcomb.loc['site',:], Dcomb.loc['OSBP', :])
            axarr2[0,1].scatter(Dcomb.loc['gender',:], Dcomb.loc['EIF1AY', :])
            axarr2[1,1].scatter(Dcomb.loc['age',:], Dcomb.loc['EIF1AY', :])
            axarr2[2,1].scatter(Dcomb.loc['site',:], Dcomb.loc['EIF1AY', :])
            show()
            exit()
        """
    return Dcorr


def select_traits_by_variance(Dtraits, frac=0.25):
    trait_vars = np.zeros([Dtraits[0].shape[0]])
    for i in xrange(Dtraits[0].shape[0]):
        data = [x for x in chain(*[D.values[i,:].tolist() for D in Dtraits])]
        trait_vars[i] = np.array(data).std()**2
    cutoff = scipy.stats.mstats.mquantiles(trait_vars, prob=[1-frac])[0]
    return [D.ix[np.where(trait_vars > cutoff)[0],:] for D in Dtraits]

def zscores(D):
    for i in D.index:
        D.loc[i,:] = (D.loc[i,:] - D.loc[i,:].mean())/D.loc[i,:].std()
    return D

def boxcox_normalize(D):
    for i in D.index:
        D.loc[i,:], _ = scipy.stats.boxcox(D.loc[i,:])
    return D
