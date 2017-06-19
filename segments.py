import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# take polygon (repeated start point) points and return segments
def poly2seg(x_poly, y_poly):
    numpoints = len(x_poly)
    numsegs = numpoints-1
    x_seg = np.empty([2,numsegs])
    y_seg = np.empty([2,numsegs])
    x_seg[0,:] = x_poly[0:numsegs]
    x_seg[1,:] = x_poly[1:numsegs+1]
    y_seg[0,:] = y_poly[0:numsegs]
    y_seg[1,:] = y_poly[1:numsegs+1]
    return x_seg, y_seg

# function to get bounds of continuous overlapping lines
def get_overlap_bounds(seg_mins, seg_maxs, min_init, max_init):
    # find left edges of segments >= min_init and <= max_init
    min_jmax = min_init
    max_jmax = max_init
    num_overlap = 2
    ct = 0

    while (num_overlap>1)and(ct<29):
        j_inds = [(seg_mins>=min_jmax)&(seg_mins<=max_jmax)&(seg_maxs>=max_jmax)]
        min_j = seg_mins[j_inds]
        max_j = seg_maxs[j_inds]
        num_overlap = len(min_j)

        if num_overlap>1:
            jmax = np.argmax(max_j)
            min_jmax = min_j[jmax]
            max_jmax = max_j[jmax]
        ct = ct+1

    min_overlap = min_init
    max_overlap = max_jmax
    return min_overlap, max_overlap

# function to get start and end points of continuous overlapping line segments
def get_overlap_segments(seg_str, seg_end):
    # loop over groups of overlapping segments until there are no more
    str_copy = np.copy(seg_str)
    end_copy = np.copy(seg_end)
    num_add_seg = len(seg_str)
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
        seg_str = seg_str[add_seg_inds]
        seg_end = seg_end[add_seg_inds]
 
        # save overlapping segments to array
        lcomps[ct] = lcomp
        rcomps[ct] = rcomp
        ct = ct+1

    # plot
    #plt.figure(0)
    #for i in range(len(str_copy)):
    #    plt.plot([str_copy[i], end_copy[i]], [len(str_copy)-i, len(end_copy)-i], 'b-', lw=3.)

    #seg_ind = [len(seg_str)+1]*len(lcomps)

    #for i in range(len(lcomps)):
    #    plt.plot([lcomps[i], rcomps[i]], [len(str_copy)+1, len(str_copy)+1], 'm-', lw=3.)

    #plt.savefig('segments.png')

    return lcomps, rcomps

# calculate fractional coverage of overlapping segments
def get_coverage_fraction(left_edges, right_edges, domain_length):
    seg_lengths = right_edges-left_edges
    cov_frac = np.sum(seg_lengths)/domain_length
    return cov_frac

'''
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
'''
