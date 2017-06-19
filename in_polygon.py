import numpy as np
from segments import get_overlap_segments
from segments import get_coverage_fraction, poly2seg

# calculate bearings from point to segments
def dir_span(px, py, segx, segy):
    l1x = segx[0,:]-px
    l2x = segx[1,:]-px
    l1y = segy[0,:]-py
    l2y = segy[1,:]-py
    dir1 = np.arctan2(l1y, l1x)
    dir2 = np.arctan2(l2y, l2x)
    return dir1, dir2

# convert angle pairs from [-pi, pi] to segments between 0 and 1
def angles2segments(ang1, ang2):
    # convert to [0, 2*pi]
    ang1[ang1<0] = ang1[ang1<0]+2.*np.pi
    ang2[ang2<0] = ang2[ang2<0]+2.*np.pi

    # set left and right bounds of angles
    ang_left = np.copy(ang1)
    ang_right = np.copy(ang2)
    ang_left[ang1>ang2] = ang2[ang1>ang2]
    ang_right[ang1>ang2] = ang1[ang1>ang2]

    # dealias
    deal_cond = (np.abs(ang_left-ang_right)>np.pi)
    ang_temp = np.copy(ang_right[deal_cond])
    ang_right[deal_cond] = ang_left[deal_cond]
    ang_left[deal_cond] = 0.
    
    # add additional aliased segments from ang<2.*pi to 2.*np.pi
    ang_left = np.append(ang_left, ang_temp)
    ang_right = np.append(ang_right, np.linspace(np.pi*2., np.pi*2., len(ang_temp)))

    seg_left = ang_left/(2.*np.pi)
    seg_right = ang_right/(2.*np.pi)
    return seg_left, seg_right

# function to determine if point is in a polygon
def in_polygon(x_poly, y_poly, x_point, y_point):
    # compute direction span between the point and each polygon segment
    x_seg, y_seg = poly2seg(x_poly, y_poly)
    dir1, dir2 = dir_span(x_point, y_point, x_seg, y_seg)
    seg_left, seg_right = angles2segments(dir1, dir2)

    # get overlapping segment bounds and calculate covered fraction
    over_left, over_right = get_overlap_segments(seg_left, seg_right)
    cf = get_coverage_fraction(over_left, over_right, 1.)
    indicator = int(cf)

    return indicator
