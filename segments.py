import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# function to get bounds of continuous overlapping lines
def get_overlap_bounds(seg_mins, seg_maxs, min_init, max_init):
    # find left edges of segments >= min_init and <= max_init
    min_jmax = min_init
    max_jmax = max_init
    num_overlap = 2

    while (num_overlap>1):
        j_inds = [(seg_str>=min_jmax)&(seg_str<=max_jmax)&(seg_end>=max_jmax)]
        min_j = seg_str[j_inds]
        max_j = seg_end[j_inds]
        num_overlap = len(min_j)
        jmax = np.argmax(max_j)
        min_jmax = min_j[jmax]
        max_jmax = max_j[jmax]
        print num_overlap, min_init, min_jmax, max_jmax

    min_overlap = min_init
    max_overlap = max_jmax
    return min_overlap, max_overlap

# create random line segments
numseg = 10
seg_width = np.random.rand(numseg)*0.1+0.1
seg_str = np.random.rand(numseg)*0.7
seg_end = seg_str+seg_width

for i in range(numseg):
    # plot
    plt.plot([seg_str[i], seg_end[i]], [numseg-i, numseg-i], 'b-', lw=3.)

# loop over groups of overlapping segments until there are no more
num_add_seg = numseg
lcomps = np.ma.masked_all([numseg])
rcomps = np.ma.masked_all([numseg])

while num_add_seg>0:
    # get minimum left edge
    lcomp = np.min(seg_str)
    lcomp_ind = np.argmin(seg_str)
    rcomp = seg_end[lcomp_ind]
    print lcomp, rcomp

    # find left edges >= lcomp and <= rcomp
    lcomp, rcomp = get_overlap_bounds(seg_str, seg_end, lcomp, rcomp)
    print lcomp, rcomp

    plt.scatter(lcomp, numseg-lcomp_ind, c='r', s=300)
    plt.scatter(rcomp, numseg-lcomp_ind, c='g', s=300)

    # determine if there are additional segments to be analyzed
    add_seg_inds = np.arange(num_add_seg)[seg_str>rcomp]
    num_add_seg = len(add_seg_inds)
    print add_seg_inds, num_add_seg
    seg_str = seg_str[add_seg_inds]
    seg_end = seg_end[add_seg_inds]

plt.savefig('segments.png')
