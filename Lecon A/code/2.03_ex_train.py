from roblib import *

def f(x,u):
    return (np.matrix([x[3,0]*cos(x[2,0]),     x[3,0]*sin(x[2,0]),  u[0,0],u[1,0]]).T)


def control(x, r, dr, d2r):
    A = np.matrix([ [-x[3,0]*sin(x[2,0]), cos(x[2,0])],
                    [x[3,0]*cos(x[2,0]) , sin(x[2,0])]   ])
    y = np.matrix([x[0,0], x[1,0]]).T
    dy = np.matrix([x[3,0]*cos(x[2,0]), x[3,0]*sin(x[2,0])]).T
    
    v = (r - y) + 2*(dr - dy) + d2r
    u = A.I @ v
    return u

ax = init_figure(-30,30,-30,30)

dt = 0.5
xa = np.matrix([0, 1, pi/3, 1]).T
xb = np.matrix([10, 10, pi/3, 2]).T
xc = np.matrix([10, 1, 0, 2]).T


w = 0.1
L = [15, 7]
d = 6


for t in arange(0,100,dt) :
    clear(ax)
    draw_tank(xa.A1)
    draw_tank(xb.A1)
    draw_tank(xc.A1)
    # x = x + dt*f(x,u)

    """ A """
    ra = np.matrix([L[0]*sin(w*t),
                    L[1]*cos(w*t)]).T
    dra = np.matrix([L[0]*w*cos(w*t),
                    -L[1]*w*sin(w*t)]).T
    d2ra = np.matrix([-L[0]*w*w*sin(w*t),
                    -L[1]*w*w*cos(w*t)]).T
    ua = control(xa, ra, dra, d2ra)
    xa = xa + dt*f(xa,ua)

    """ B """
    rb = np.matrix([xa[0,0] - d*cos(xa[2,0]),
                    xa[1,0] - d*sin(xa[2,0])]).T
    drb = np.matrix([xa[3,0]*cos(xa[2,0]) + d*ua[0,0]*sin(xa[2,0]),
                    xa[3,0]*sin(xa[2,0]) - d*ua[0,0]*cos(xa[2,0])]).T
    d2rb = np.matrix([ua[1,0]*cos(xa[2,0]) - ua[0,0]*xa[3,0]*sin(xa[2,0]) + d*ua[0,0]*ua[0,0]*cos(xa[2,0]),
                       ua[1,0]*sin(xa[2,0]) - ua[0,0]*xa[3,0]*cos(xa[2,0]) + d*ua[0,0]*ua[0,0]*sin(xa[2,0])]).T
    ub = control(xb, rb, drb, d2rb)
    xb = xb + dt*f(xb,ub)

    """ C """
    rc = np.matrix([xb[0,0] - d*cos(xb[2,0]),
                    xb[1,0] - d*sin(xb[2,0])]).T
    drc = np.matrix([xb[3,0]*cos(xb[2,0]) + d*ub[0,0]*sin(xb[2,0]),
                    xb[3,0]*sin(xb[2,0]) - d*ub[0,0]*cos(xb[2,0])]).T
    d2rc = np.matrix([ub[1,0]*cos(xb[2,0]) - ub[0,0]*xb[3,0]*sin(xb[2,0]) + d*ub[0,0]*ub[0,0]*cos(xb[2,0]),
                       ub[1,0]*sin(xb[2,0]) - ub[0,0]*xb[3,0]*cos(xb[2,0]) + d*ub[0,0]*ub[0,0]*sin(xb[2,0])]).T
    uc = control(xc, rc, drc, d2rc)
    xc = xc + dt*f(xc,uc)

    plt.plot(L[0]*sin(w*t), L[1]*cos(w*t), "ro")
    plt.plot(rb[0], rb[1], "ro")
    plt.plot(rc[0], rc[1], "ro")
pause(1)
