import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# polygon shape of hexagon
def make_hexagon(a):
    xp = np.array([a, a/2., -a/2., -a, -a/2., a/2., a])
    yp = np.array([0., a*np.sqrt(3.)/2., a*np.sqrt(3.)/2., 0.,
                  -a*np.sqrt(3.)/2., -a*np.sqrt(3.)/2., 0.])
    return xp, yp

# stellar triangle given branch fraction width and segment points
def make_stellar_triangle(fbranch, p1, p2):
    # get normal and tangential directions to p12
    p12 = p2-p1
    midpoint = (p2+p1)/2.
    segmag = np.sqrt(np.sum((p12)**2.))
    n = np.array([-p12[1], p12[0]])/segmag
    t = p12/segmag

    s1 = p1+t*fbranch*segmag/2.
    s2 = midpoint+t*(1.-fbranch)*segmag/2.
    s3 = s2+segmag*(1.-fbranch)*(n*np.sqrt(3.)/2.-t/2.)
    return s1, s2, s3

# function to create polygon of stellar crystal with branch width fraction
def make_stellar(fbranch, a):
    # define hexagonal polygon
    x, y = make_hexagon(a)
    numhex = len(x)
    numstellar = 25
    xst = np.empty([numstellar])
    yst = np.empty([numstellar])
    xst[0] = x[0]
    yst[0] = y[0]
    stind = 0

    # loop through segments of hexagon and insert points for stellar triangles
    for i in range(numhex-1):
        p1 = np.array([x[i], y[i]])
        p2 = np.array([x[i+1], y[i+1]])
        s1, s2, s3 = make_stellar_triangle(fbranch, p1, p2)
        xst[stind+1] = s1[0]
        xst[stind+2] = s3[0]
        xst[stind+3] = s2[0]
        xst[stind+4] = p2[0]

        yst[stind+1] = s1[1]
        yst[stind+2] = s3[1]
        yst[stind+3] = s2[1]
        yst[stind+4] = p2[1]
        stind = stind+4
    return xst, yst

# get area fraction of stellar
def afrac_stellar(fbranch):
    afrac = 1.-(1.-fbranch)**2.
    return afrac

if __name__ == 'main':
    # plot
    x, y = make_hexagon(1.)
    xst, yst = make_stellar(0.5, 1.)
    stinds = np.arange(len(xst))
    plt.plot(x, y)
    plt.scatter(xst,yst,c=stinds,cmap='gist_rainbow',s=100)
    plt.plot(xst, yst)
    plt.savefig('stellar.png')
