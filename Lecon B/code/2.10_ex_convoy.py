from roblib import *

def f(x,u):
    return (np.matrix([x[3,0]*cos(x[2,0]),     x[3,0]*sin(x[2,0]),  u[0,0], u[1,0], x[3,0]]).T)


def control(x, r, dr, d2r = None):
    A = np.matrix([ [-x[3,0]*sin(x[2,0]), cos(x[2,0])],
                    [ x[3,0]*cos(x[2,0]) , sin(x[2,0])]   ])
    y = np.matrix([x[0,0], x[1,0]]).T
    dy = np.matrix([x[3,0]*cos(x[2,0]), x[3,0]*sin(x[2,0])]).T

    if d2r == None:
        v = (r - y) + (dr - dy)
    else:
        v = (r - y) + 2*(dr - dy) + d2r
    u = A.I @ v
    return u

ax = init_figure(-30,30,-30,30)

dt = 0.1
m = 6
xa = np.matrix([0, 1, pi/3, 1, 0]).T
X = np.matrix([4*arange(m), ones(m), ones(m), ones(m), zeros(m)]).T #Xs, Ys, Thetas, Vs
S   = np.matrix(zeros((1,5)))
ds = 0.1
w = 0.1
L = [20, 5]
d = 5
elipse = [L[0]*cos(np.linspace(0.,2*pi,30)), L[1]*sin(np.linspace(0.,2*pi,30))]

for t in arange(0,100,dt) :
    clear(ax)
    draw_tank(xa.A1)

    """ A """
    ra = np.matrix([L[0]*sin(w*t),
                    L[1]*cos(w*t)]).T
    dra = np.matrix([L[0]*w*cos(w*t),
                    -L[1]*w*sin(w*t)]).T
    d2ra = np.matrix([-L[0]*w*w*sin(w*t),
                      -L[1]*w*w*cos(w*t)]).T
    ua = control(xa, ra, dra, d2ra)
    xa = xa + dt*f(xa,ua)
    if xa[4,0] > ds:
        S = np.vstack((S, xa.T))
        xa[4,0] = 0

    plt.plot(L[0]*sin(w*t), L[1]*cos(w*t), "ro")
    plot(elipse[0],elipse[1])

    for i in range(1,m):
        xi = X[i].T
        j = S.shape[0]-d*i/ds
        if j>0:
            xai = S[j-1].T
            ri = np.matrix([xai[0,0], xai[1,0]]).T
            dri = xa[3,0]*np.matrix([cos(xai[2,0]), sin(xai[2,0])]).T
            ui  = control(xi,ri,dri)
        else:
            ui = np.matrix([0.2, 0]).T
        xi = xi + dt*f(xi,ui)
        X[i]  = xi.T
        draw_tank(xi.A1, "black")

pause(1)
