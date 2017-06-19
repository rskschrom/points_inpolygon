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

# function to get start and end points of continuous overlapping line segments
def get_overlap_segments(seg_str, seg_end):
    # loop over groups of overlapping segments until there are no more
    num_add_seg = numseg
    lcomps = np.ma.masked_all([num_add_seg])
    rcomps = np.ma.masked_all([num_add_seg])
    ct = 0

    while num_add_seg>0:
        # get minimum left edge
        lcomp = np.min(seg_str)
        lcomp_ind = np.argmin(seg_str)
        rcomp = seg_end[lcomp_ind]

        # find left edges >= lcomp and <= rcomp
        lcomp, rcomp = get_overlap_bounds(seg_str, seg_end, lcomp, rcomp)

        # determine if there are additional segments to be analyzed
        add_seg_inds = np.arange(num_add_seg)[seg_str>rcomp]
        num_add_seg = len(add_seg_inds)
        print add_seg_inds, num_add_seg
        seg_str = seg_str[add_seg_inds]
        seg_end = seg_end[add_seg_inds]
 
        # save overlapping segments to array
        lcomps[ct] = lcomp
        rcomps[ct] = rcomp
        ct = ct+1

    return lcomps, rcomps

# calculate fractional coverage of overlapping segments
def get_coverage_fraction(left_edges, right_edges, domain_length):
    seg_lengths = right_edges-left_edges
    cov_frac = np.sum(seg_lengths)/domain_length
    return cov_frac

# create random line segments
numseg = 10
seg_width = np.random.rand(numseg)*0.1+0.03
seg_str = np.random.rand(numseg)*0.7
seg_end = seg_str+seg_width

lcomps, rcomps = get_overlap_segments(seg_str, seg_end)
cov_frac = get_coverage_fraction(lcomps, rcomps, 1.)
print cov_frac

# plot
for i in range(numseg):
    plt.plot([seg_str[i], seg_end[i]], [numseg-i, numseg-i], 'b-', lw=3.)

seg_ind = [numseg+1]*len(lcomps)
#plt.scatter(lcomps, seg_ind, c='r', s=300)
#plt.scatter(rcomps, seg_ind, c='g', s=300)

for i in range(len(lcomps)):
    plt.plot([lcomps[i], rcomps[i]], [numseg+1, numseg+1], 'm-', lw=3.)

plt.savefig('segments.png')
