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
numxp = 100
numyp = 100
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
plt.scatter(xp, yp, c=indicator, cmap='Accent', s=30, edgecolor='')
plt.plot(x, y, 'r--', linewidth=3.)

ax = plt.gca()
ax.set_aspect(1.)

ax.grid()
plt.savefig('new_poly.png')
