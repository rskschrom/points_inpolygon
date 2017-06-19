import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from create_stellar import make_stellar
from in_polygon import in_polygon

# rotate x and y points
def rotate(x, y, angle):
    ang_rad = angle/180.*np.pi
    xrot = x*np.cos(ang_rad)-y*np.sin(ang_rad)
    yrot = x*np.sin(ang_rad)+y*np.cos(ang_rad)
    return xrot, yrot

# calculate bearing from point 1 to point 2
def bearing(p1, p2):
    p12 = p2-p1
    bearing = np.arctan2(p12[1], p12[0])
    return bearing

# dealias angle 2 from angle 1 to angle 2
def dealias(ang1, ang2):
    if np.abs(ang2-ang1)>np.pi:
        ang2 = ang2+np.pi*2.
    return ang2

# test if point is in polygon
def inpolygon(poly_x, poly_y, point_x, point_y):
    # get path from first segment (s12)
    point = np.array([point_x, point_y])
    s1 = np.array([poly_x[0], poly_y[0]])
    s2 = np.array([poly_x[1], poly_y[1]])
    ang1 = bearing(point, s1)
    ang2 = bearing(point, s2)

    ang2 = dealias(ang1, ang2)
    path = np.array([ang1, ang2])
    print path

    # loop over polygon points
    for i in range(len(poly_x)-2):
        s = np.array([poly_x[i+2], poly_y[i+2]])
        ang1 = ang2
        ang2 = bearing(point, s)
        ang2 = dealias(ang1, ang2)

        # add ang2 as edge of path if it is beyond current edge
        if ang2 > path[1]:
            path[1] = ang2
        elif ang2 < path[0]:
            path[0] = ang1
        print path, ang1, ang2

    path_length = (path[1]-path[0])/(2.*np.pi)
    indicate = 0.
    err_tol = 0.01
    if np.abs(path_length-1.)<err_tol:
        indicate = 1.
    print indicate, path_length

    return indicate

# create polygon of stellar crystal
a = 1.
fbranch = 0.6
#x = np.array([a, a, -a, -a, a])
#y = np.array([-a, a, a, -a, -a])
#x = np.array([-a, -a, a, a, -a])
#y = np.array([a, -a, -a, a, a])
x, y = make_stellar(fbranch, a)
x, y = rotate(x, y, 30.)

# test points
numxp = 200
numyp = 200
x2d, y2d = np.meshgrid(np.linspace(-1.5, 1.5, numxp),
                       np.linspace(-1.5, 1.5, numyp), indexing='ij')
xp = x2d.flatten()
yp = y2d.flatten()
indicator = np.empty([numxp*numyp])

for i in range(numxp*numyp):
    #xtest = xp[i]
    #ytest = yp[i]
    #print 'doing point {:0d}, location: ({:.2f}, {:.2f})'.format(i, xtest, ytest)
    indicator[i] = in_polygon(x, y, xp[i], yp[i])

#plot
plt.scatter(xp, yp, c=indicator, cmap='Accent', s=1, edgecolor='')
plt.plot(x, y, 'r--', linewidth=3.)

ax = plt.gca()
ax.set_aspect(1.)

ax.grid()
plt.savefig('new_poly.png')
