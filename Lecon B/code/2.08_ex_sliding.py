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

def glissant(x, r, dr):
    A = np.matrix([ [-x[3,0]*sin(x[2,0]), cos(x[2,0])],
                    [x[3,0]*cos(x[2,0]) , sin(x[2,0])]   ])
    y = np.matrix([x[0,0], x[1,0]]).T
    dy = np.matrix([x[3,0]*cos(x[2,0]), x[3,0]*sin(x[2,0])]).T

    v = 100*sign(w-y+dw-dy)
    u = A.I @ v
    return u


fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
dt = 0.01

x = np.matrix([10, 0, 1,1]).T

u = np.matrix([1, 1]).T
L=10
s = arange(0,2*pi,0.01)
E = []
for t in arange(0,15,dt) :
    # displaying
    plt.pause(0.0000001)
    plt.cla()
    plt.xlim(-30,30)
    plt.ylim(-30,30)
    plt.plot(L*cos(s), L*sin(3*s),color='magenta')

    # references
    w   = L*np.matrix([cos(t), sin(3*t)]).T
    dw  = L*np.matrix([-sin(t), 3*cos(3*t)]).T
    ddw = L*np.matrix([-cos(t), -(3**2)*sin(3*t)]).T

    #u = control(x,w,dw,ddw)
    u = glissant(x,w,dw)
    draw_tank(x.A1,'red')

    E.append(abs(x[0,0]-w[0,0])+abs(x[1,0]-w[1,0]))
    draw_disk(w.A1,0.5,ax,"red")
    x = x + dt*f(x,u)

plt.plot(E, t,color='magenta')
