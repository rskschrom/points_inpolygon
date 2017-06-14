import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# create random line segments
numseg = 10
seg_width = np.random.rand(numseg)*0.2+0.1
seg_str = np.random.rand(numseg)*0.7
seg_end = seg_str+seg_width

# get minimum left edge
lcomp = np.min(seg_str)
lcomp_ind = np.argmin(seg_str)
rcomp = seg_end[lcomp_ind]
print lcomp, rcomp

# find left edges >= lcomp and <= rcomp
lcontain_inds = [(seg_str>=lcomp)&(seg_str<=rcomp)]
rgt_contain = seg_end[lcontain_inds]
rcomp = np.max(rgt_contain)
print lcomp, rcomp

for i in range(numseg):
    # plot
    plt.plot([seg_str[i], seg_end[i]], [numseg-i, numseg-i], 'b-', lw=3.)
plt.scatter(lcomp, numseg-lcomp_ind, c='r', s=300)
plt.scatter(rcomp, numseg-lcomp_ind, c='g', s=300)
plt.savefig('segments.png')

