from matplotlib.pylab import *
from collections import defaultdict
from itertools import chain

def _normalize_dict_quantile(d):
    vals = d.values()
    vals = array(vals)
    mean = vals.mean()
    std = vals.std()
    dn = {}
    """
    for k in d:
        dn[k] = log(d[k])/log(vals.max())
    maxval = max(dn.values())
    minval = min(dn.values())

    #for k, v in dn.iteritems():
    #    dn[k] = (v + 0.5)/maxval
    """
    sorted_vals = sorted(list(set(vals)))
    ref = arange(0, 1, 1./len(sorted_vals))
    for k in d:
        idx = sorted_vals.index(d[k])
        dn[k] = ref[idx]
    return dn

def _normalize_dict_max(d):
    maxval = float(max(d.values()))
    dn = dict([(k, val/maxval) for k, val in d.iteritems()])
    return dn
    

def get_roles(lcs, gcs):
    lc_mean = array(lcs.values()).mean()
    gc_mean = array(gcs.values()).mean()
    lc_mean, gc_mean  = 0.5, 0.5
    roles = {}
    for n, lc in lcs.iteritems():
        gc = gcs[n]
        if lc > lc_mean:
            if gc > gc_mean:
                roles[n] = 'C-hub'
            else:
                roles[n] = 'L-hub'
        else:
            if gc > gc_mean:
                roles[n] = 'S-hub'
            else:
                roles[n] = 'N-hub'
    return roles


class NetworkStatistics(object):
    def __init__(self, nodesbycommunity, edgesbycommunity, directed=True):
        self._sizecutoff = 5
        
        self.community_distribution = defaultdict(int)
        self.degree_distribution = defaultdict(int)
        self.degrees = defaultdict(int)
        self.community_degrees = defaultdict(int)
        self.nt_community_degrees = defaultdict(int)
        self.gcs = defaultdict(int)
        self.lcs = defaultdict(int)
        self.number_of_nt_communities = 0.
        self.number_of_edges = len(set(chain(*[va for k, va in edgesbycommunity.iteritems()])))
        # Maximum intra-modular degrees (mids)
        self.mids = defaultdict(int)


        curr_mids = defaultdict(int)
        if directed:
            self.causal_flow = defaultdict(int)
            for c, edges in edgesbycommunity.iteritems():
                for n1, n2 in edges:
                    self.causal_flow[n1] -= 1
                    self.causal_flow[n2] += 1
        for c, edges in edgesbycommunity.iteritems():
            if c == 'background':
                continue
            for n1, n2 in edges:
                curr_mids[n1] = 0.
                curr_mids[n2] = 0.
            for n1, n2 in edges:
                self.degrees[n1] += 1.
                self.degrees[n2] += 1.
                curr_mids[n1] += 1. 
                curr_mids[n2] += 1.
            #self.degrees[n1] /= len(nodesbycommunity[c])
            #self.degrees[n2] /= len(nodesbycommunity[c])
            #curr_mids[n1] /= len(nodesbycommunity[c])
            #curr_mids[n2] /= len(nodesbycommunity[c])
            for n1, n2 in edges:
                if curr_mids[n1] > self.mids[n1]:
                    self.mids[n1] = curr_mids[n1] 
                if curr_mids[n2] > self.mids[n2]:
                    self.mids[n2] = curr_mids[n2] 
        for c, nodes in nodesbycommunity.iteritems():
            self.community_distribution[len(nodes)] += 1
            for n in nodes:
                self.community_degrees[n] += 1
            if len(nodes) >= self._sizecutoff:
                for n in nodes:
                    self.nt_community_degrees[n] += 1
                self.number_of_nt_communities += 1
        for n, deg in self.degrees.iteritems():
            self.lcs[n] = deg
            if n not in self.gcs:
                self.gcs[n] = 0.
            self.degree_distribution[deg] += 1

        for n, cd in self.nt_community_degrees.iteritems():
            self.gcs[n] = float(cd)
            if n not in self.lcs:
                self.lcs[n] = 0

        self.normalized_lcs = _normalize_dict_quantile(self.lcs)
        self.normalized_gcs = _normalize_dict_quantile(self.gcs)
        self.roles = get_roles(self.normalized_lcs, self.normalized_gcs)

        self.number_of_communities = float(len(nodesbycommunity))

        self.normalized_community_degrees = dict([(k,v/self.number_of_communities) for k,v in self.community_degrees.iteritems()])
        self.noramlized_nt_community_degrees = dict([(k,v/self.number_of_nt_communities) for k,v in self.nt_community_degrees.iteritems()])
        self.normalized_mids = _normalize_dict_max(self.mids)
        self.normalized_degrees = _normalize_dict_max(self.degrees)

class StatsDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.std = {}


class ResamplingNetworkStatistics(object):
    def __init__(self, nodesbycommunity_list, edgesbycommunity_list):
        self.network_stats_list = []
        for i in xrange(len(nodesbycommunity_list)):
            self.network_stats_list.append(NetworkStatistics(nodesbycommunity_list[i], edgesbycommunity_list[i]))
        for stats_name in self.network_stats_list[0].__dict__:
            if type(self.network_stats_list[0].__dict__[stats_name]) in [dict, defaultdict]:
                self._calculate_resampling_stats_dict(stats_name)
        for stats_name in ['number_of_edges', 'number_of_nt_communities', 'number_of_communities']:
            self._calculate_resampling_stats(stats_name)

    def _calculate_resampling_stats(self, stats_name):
        stats_list = [nw_stats.__dict__[stats_name] for nw_stats in self.network_stats_list]
        self.__dict__[stats_name] = mean(stats_list)
        self.__dict__[stats_name + '_std'] = std(stats_list)
        
    def _calculate_resampling_stats_dict(self, stats_name):
        stats_dictionaries = [nw_stats.__dict__[stats_name] for nw_stats in self.network_stats_list]
        str_type = (type(stats_dictionaries[0].values()[0]) == str)
        self.__dict__[stats_name] = StatsDict()
        for key in stats_dictionaries[0].keys():
            values = []
            for stats_dict in stats_dictionaries:
                if key in stats_dict:
                    values.append(stats_dict[key])
            if str_type:
                counts = defaultdict(int)
                for value in values:
                    counts[value] += 1
                max_count = max(counts.values())
                max_count_value = [value for value, count in counts.iteritems() if max_count == count][0]
                frac = counts[max_count_value]/float(len(values))
                self.__dict__[stats_name][key] = max_count_value
                self.__dict__[stats_name].std[key] = frac
            else:
                self.__dict__[stats_name][key] = mean(values)
                self.__dict__[stats_name].std[key] = std(values)



