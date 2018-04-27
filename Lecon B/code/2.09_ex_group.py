from roblib import *

def f(x,u):
    return (np.matrix([x[3,0]*cos(x[2,0]),     x[3,0]*sin(x[2,0]),  u[0,0],u[1,0]]).T)


def control(x, r, dr, d2r):
    A = np.matrix([ [-x[3,0]*sin(x[2,0]), cos(x[2,0])],
                    [x[3,0]*cos(x[2,0]) , sin(x[2,0])]   ])
    y = np.matrix([x[0,0], x[1,0]]).T
    dy = np.matrix([x[3,0]*cos(x[2,0]), x[3,0]*sin(x[2,0])]).T

    v = (r - y) + 2*(dr - dy) + d2r
    u = A.I*v
    return u


m  = 20
X  = 10*randn(4,m)
a  = 0.1
dt = 0.5

for t in arange(0,40,dt):
    plt.pause(0.001)
    plt.clf()
    plt.xlim(-50,50)
    plt.ylim(-50,50)
    for i in range(m):
        delta = 2*i*pi/m
        theta = a*t

        D = np.matrix([[20+15*sin(a*t),  0],
                       [             0, 20]])

        dD = np.matrix([[15*a*cos(a*t), 0],
                        [            0, 0]])

        ddD = np.matrix([[-15*(a**2)*sin(a*t), 0],
                         [                  0, 0]])

        R = np.matrix([[cos(theta), -sin(theta)],
                       [sin(theta),  cos(theta)]])

        dR = a*np.matrix([[-sin(theta), -cos(theta)],
                          [cos(theta),  -sin(theta)]])

        ddR = -a**2*R
        # refs
        c = np.matrix([cos(a*t+delta),sin(a*t+delta)]).T
        dc = a*np.matrix([-sin(a*t+delta),cos(a*t+delta)]).T
        ddc = -(a**2)*c

        w = R*D*c
        dw = R*D*dc + R*dD*c + dR*D*c
        ddw = R*D*ddc + R*ddD*c + ddR*D*c + 2*(R*dD*dc) + 2*(dR*dD*c) + 2*(dR*D*dc)

        x = X[:,i].reshape(4,1)
        draw_tank(x,'b')
        u = control(x,w,dw,ddw)
        x = x + dt*f(x,u)
        X[:,i]  = x.flatten()

        plt.plot(w[0,0], w[1,0],'r+')

plt.show()
