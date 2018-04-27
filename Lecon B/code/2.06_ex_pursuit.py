from roblib import *

def f(x,u):
    return np.matrix([u[0,0]*cos(x[2,0]),
                      u[0,0]*sin(x[2,0]),
                      u[1,0]]).T

def control(xa,xb,v):
    x = np.matrix([[ cos(xa[2,0]), sin(xa[2,0]), 0],
                   [-sin(xa[2,0]), cos(xa[2,0]), 0],
                   [            0,            0, 1]]) * (xb - xa)

    A = np.matrix([[-1, x[1,0]], [ 0,-x[0,0]]])
    b = v[0,0]*np.matrix([ cos(x[2,0]), sin(x[2,0]) ]).T
    temp = x[0:2,0].reshape((2,1))
    w = np.matrix([10,0]).T
    dw = np.matrix(np.zeros((2,1)))
    return A.I*(w - temp + dw - b)

dt = 0.1

xa = np.matrix([-10, -10,0]).T
xb = np.matrix([ -5,  -5, 0]).T


for t in arange(0,10,dt) :
    plt.pause(0.01)
    plt.clf()
    plt.xlim(-30,30)
    plt.ylim(-30,30)

    v = np.matrix([3, sin(0.2*t)]).T
    u = control(xa,xb,v)

    draw_tank(xa.A1, "blue")
    draw_tank(xb.A1, "red")
    xa = xa + dt*f(xa,u)
    xb = xb + dt*f(xb,v)
plt.show()
