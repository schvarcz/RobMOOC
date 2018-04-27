from roblib import *
from numpy import prod

fig = figure(0)
ax = fig.add_subplot(111, aspect='equal')

def f(x,u):
    return np.matrix([ x[3,0]*cos(x[2,0]), x[3,0]*sin(x[2,0]), u[0,0], u[1,0]]).T

def control(x,w,dw):
    A = np.matrix([[-x[3,0]*sin(x[2,0]), cos(x[2,0])],
                   [ x[3,0]*cos(x[2,0]), sin(x[2,0])]])
    y = np.matrix([ x[0,0], x[1,0] ]).T
    dy = np.matrix([ x[3,0]*cos(x[2,0]) , x[3,0]*sin(x[2,0]) ]).T
    return A.I * ((w - y) + (dw - dy))

def b(i,n,t):
    return prod(range(1,n+1))/(prod(range(1,i+1))*prod(range(1,n-i+1))) * (1-t)**(n-i) * (t**i)

def db(i,n,t):
    if n==i:
        return n*t**(n-1)
    elif i==0:
        return n*(1-t)**(n-1)
    return prod(range(1,n+1))/(np.prod(range(1,i+1))*prod(range(1,n-i+1))) * (i*(1-t)**(n-i)*t**(i-1) - (n-i)*(1-t)**(n-i-1) * t**i)

def setpoint(t):
    return np.sum([ b(i,n,t)*P[i,:] for i in range(0,n+1)], axis=0).T

def dsetpoint(t):
    return np.sum([db(i,n,t)*P[i,:] for i in range(0,n+1)], axis=0).T


P = np.matrix([[1,1,1,1,2, 3,4,5,4,8,10,8],
               [1,4,7,9,10,8,6,4,0,0,0,8]]).T
n = P.shape[0]-1

plot(P.T[0].A1, P.T[1].A1, 'or')
dt = 0.1
k = 0

A1 = np.matrix([[2,0],[4,2],[2,7]])
A2 = np.matrix([[7,2],[8,3],[3,10]])
draw_polygon(A1,ax,'green')
draw_polygon(A2,ax,'green')

tmax = 50
x = np.matrix([0,0,0,1]).T
ax.set_xlim(-1,11)
ax.set_ylim(-1,11)
for t in arange(0,tmax,dt):

    w = setpoint(t/tmax)
    dw = (1.0/tmax)*dsetpoint(t/tmax)
    u = control(x,w,dw)

    x = x + dt*f(x,u)

    plot(w[0],w[1], 'c.')
    if k % 10 == 0:
        draw_tank(x.A1,'darkblue',0.2)
        plt.pause(0.0001)
    k += 1

draw_tank(x.A1,'darkblue',0.2)
plt.show()
