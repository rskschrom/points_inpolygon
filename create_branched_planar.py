'''
Code to generate 2D branched planar crystal polygons.

Robert Schrom @ 11/2017
'''
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# rotation
def rotate(x, y, angle):
    angle = angle*np.pi/180.
    xrot = np.cos(angle)*x-np.sin(angle)*y
    yrot = np.sin(angle)*x+np.cos(angle)*y
    return xrot, yrot

# flip over y-axis
def flipy(x, y):
    xflip = -x
    yflip = y
    return xflip, yflip

# get equation of line from p1 to p2
def points2eqn(p1x, p1y, p2x, p2y):
    m = (p2y-p1y)/(p2x-p1x)
    b = p1y-m*p1x
    return m, b

# get point of intersection of two lines
def intersection(m1, b1, m2, b2):
    xint = (b2-b1)/(m1-m2)
    yint = m1*xint+b1
    return xint, yint

# create branched planar crystal
def make_branched_planar(amax, ac, ag, ft, fb, fmb, nsb, diplen):
    # get x and y coordinates of bounding points
    #----------------------------------------------------
    # p1 - midpoint of ice core edge
    # p2 - intersection of ice core edge and main branch
    # p3 - intersection of main branch and tip
    # p4 - upper corner at amax
    #----------------------------------------------------
    wmb = 1./2.*fmb*ac
    wt = 1./2.*ft*amax

    p1x = 0.
    p1y = np.sqrt(3.)/2.*ac
    p2x = ac/2.-wmb
    p2y = p1y
    p3x = amax/2.-wmb
    p3y = np.sqrt(3.)/2.*amax
    p4x = amax/2.
    p4y = p3y

    # create xcoor and ycoor of half sector
    xcoor = np.array([p1x, p2x, p3x, p4x])
    ycoor = np.array([p1y, p2y, p3y, p4y])

    # figure out sub-branches
    wsb = fb/(nsb-1)*(amax-ac-wt-wmb)
    ssb = wsb*(1.-fb)/fb

    mbound, bbound = points2eqn(0., np.sqrt(3.)/2.*ag, amax/2.*(1.-ft), np.sqrt(3.)/2.*amax)

    for i in range(nsb):
        # points on main branch
        sb1x = p2x+i*(wsb+ssb)/2.
        sb1y = p2y+i*(wsb+ssb)*np.sqrt(3.)/2.
        sb4x = sb1x+wsb/2.
        sb4y = sb1y+wsb*np.sqrt(3.)/2.

        # get equation of line defining each sub-branch edge (60 degrees from main branch)
        m_sb = -np.sqrt(3.)
        b_sb_low = -m_sb*sb1x+sb1y
        b_sb_high = -m_sb*sb4x+sb4y

        # points off main branch
        sb2x, sb2y = intersection(mbound, bbound, m_sb, b_sb_low)
        sb3x, sb3y = intersection(mbound, bbound, m_sb, b_sb_high)

        # add small delx and dely so sub-branches don't touch
        delx = diplen
        dely = -diplen*np.sqrt(3.)

        # replace with point on x=0 if below bounding line from tip to ag
        if sb2y>b_sb_low:
            sb2y = b_sb_low
            sb2x = 0.
        if sb3y>b_sb_high:
            sb3y = b_sb_high
            sb3x = 0.

        sb2x = sb2x+delx
        sb2y = sb2y+dely
        sb3x = sb3x+delx
        sb3y = sb3y+dely

        # insert sub-branch into coordinate arrays
        sbxc = np.array([sb1x, sb2x, sb3x, sb4x])
        sbyc = np.array([sb1y, sb2y, sb3y, sb4y])

        xcoor = np.insert(xcoor, 2+i*4, sbxc)
        ycoor = np.insert(ycoor, 2+i*4, sbyc)

    # flip over half sector to create full sector
    xsec = np.concatenate((-xcoor[::-1], xcoor[1:]))
    ysec = np.concatenate((ycoor[::-1], ycoor[1:]))
    
    # rotate sector 60 degrees and concatenate with previous sector
    xrot, yrot = rotate(xsec, ysec, -60.)
    xhex = np.concatenate((xsec, xrot[1:]))
    yhex = np.concatenate((ysec, yrot[1:]))

    # repeat until we have the entire crystal
    for i in range(4):
        xrot, yrot = rotate(xsec, ysec, -(i+2)*60.)
        xhex = np.concatenate((xhex, xrot[1:]))
        yhex = np.concatenate((yhex, yrot[1:]))

    print len(xhex)
    return xhex, yhex

if __name__ == 'main':
    # set particle parameters
    amax = 2.
    ac = 0.2
    ag = 1.2
    ft = 0.4
    fb = 0.4
    fmb = 0.3
    nsb = 12

    # plot
    x, y = make_branched_planar(amax, ac, ag, ft, fv, fmb, nsb)
    stinds = np.arange(len(x))
    plt.plot(x, y)
    ax = plt.gca()
    ax.set_aspect(1.)
    ax.set_xlim([-amax, amax])
    ax.set_ylim([-amax, amax])

    ax.grid()
    plt.savefig('branched_planar.png')
