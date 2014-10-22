"""
This is essentially due to Brent Pedersen (https://github.com/brentp)
with some modifications by Pablo Cordero 
"""
from itertools import groupby, cycle
import pdb
from operator import itemgetter
from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np

def _gen_data(fhs, columns, sep):
    """
    iterate over the files and yield chr, start, pvalue
    """
    for fh in fhs:
        for line in fh:
            if line[0] == "#": continue
            toks = line.split(sep)
            yield toks[columns[0]], int(toks[columns[1]]), float(toks[columns[2]])

def chr_cmp(a, b):
    a = a.lower().replace("_", ""); b = b.lower().replace("_", "")
    achr = a[3:] if a.startswith("chr") else a
    bchr = b[3:] if b.startswith("chr") else b

    try:
        return cmp(int(achr), int(bchr))
    except ValueError:
        if achr.isdigit() and not bchr.isdigit(): return -1
        if bchr.isdigit() and not achr.isdigit(): return 1
        # X Y
        return cmp(achr, bchr)


def chr_loc_cmp(alocs, blocs):
    return chr_cmp(alocs[0], blocs[0]) or cmp(alocs[1], blocs[1])


"""
data is an iterator of tuples that with: chromosome, position, value.
"""
def manhattan(data, ax, apply_on_values=lambda x:x, colors='bk', sep='\t', lines=False, ymax=None, size=2):

    xs = []
    ys = []
    cs = []
    colors = cycle(colors)
    xs_by_chr = {}
    last_x = 0
    sorted_data = sorted(data, cmp=chr_loc_cmp)

    for seqid, rlist in groupby(sorted_data, key=itemgetter(0)):
        color = colors.next()
        rlist = list(rlist)
        region_xs = [last_x + r[1] for r in rlist]
        xs.extend(region_xs)
        ys.extend([r[2] for r in rlist])
        cs.extend([color] * len(rlist))

        xs_by_chr[seqid] = (region_xs[0] + region_xs[-1]) / 2

        # keep track so that chrs don't overlap.
        last_x = xs[-1]

    xs_by_chr = [(k, xs_by_chr[k]) for k in sorted(xs_by_chr.keys(), cmp=chr_cmp)]

    xs = np.array(xs)
    ys = apply_on_values(np.array(ys))

    #ax = f.add_axes((0.1, 0.09, 0.88, 0.85))

    if lines:
        ax.vlines(xs, 0, ys, colors=cs, alpha=0.5)
    else:
        ax.scatter(xs, ys, s=size, c=cs, alpha=0.8, edgecolors='none')

    plt.axis('tight')
    plt.xlim(0, xs[-1])
    if ymax is not None: plt.ylim(ymax=ymax)
    plt.xticks([c[1] for c in xs_by_chr], [c[0] for c in xs_by_chr], rotation=-90, size=8.5)

def netQTLplot(hubs, hub_connections, all_snps, data, ax, colors='bk', hub_color='red', nohubpos=False):
    all_snps_grouped = groupby(all_snps, key=itemgetter(0))
    last_x = 0
    xs_by_chr = {}
    offset_by_chr = {}
    colors_by_chr = {}
    colors = cycle(colors)
    chroms = []
    for chrom, poslist in all_snps_grouped:
        chroms.append(chrom)
        colors_by_chr[chrom] = colors.next()
        poslist = list([p[1] for p in poslist])
        mx = max(poslist)
        mn = min(poslist)
        med = last_x + (mx - mn)/2
        xs_by_chr[chrom] = med
        offset_by_chr[chrom] = last_x + mn
        last_x += mx
    plt.xlim(0, last_x)
    if nohubpos:
        hub_rad = 0.5
        data_rad = 0.1
        hub_pos = dict([(h[0], i+1) for i, h in enumerate(hubs)])
    else:
        hub_rad = last_x * 0.003
        data_rad = last_x * 0.0004
        plt.ylim(0, last_x)
        hub_pos = dict([(name, offset_by_chr[chrom] + pos) for name, chrom, pos, val in hubs])
    # Draw data
    for chrom, pos, hub, val in data:
        coord = (offset_by_chr[chrom] + pos, hub_pos[hub])
        data_circle = patches.Circle(coord, radius=data_rad*val, color=colors_by_chr[chrom], linewidth=0)
        ax.add_artist(data_circle)
    # Draw links between hubs
    for hub1, hub2, color in hub_connections:
        pos1 = hub_pos[hub1]
        pos2 = hub_pos[hub2]
        mnpos = min(pos1, pos2)
        height = abs(pos2 - pos1)
        arc = patches.Arc((0, mnpos + height/2), height/5, height, theta1=90, theta2=270, color=color, linewidth=0.5)
        arc.set_clip_on(False)
        ax.add_artist(arc)
    # Draw hubs
    for name, chrom, pos, val in hubs:
        center = (1, hub_pos[name])
        hub_circle = patches.Circle(center, radius=hub_rad*val, color=hub_color, linewidth=0)
        hub_circle.set_clip_on(False)
        ax.add_artist(hub_circle)
    plt.xticks([xs_by_chr[c] for c in chroms], [c for c in chroms], rotation=-90, size=8.5)
    if nohubpos:
        pass
        #ax.axes.get_yaxis().set_visible(False)
    else:
        plt.yticks([xs_by_chr[c] for c in chroms], [c for c in chroms], size=8.5)
    plt.show()
