from roblib import *
from math import atan2, atan

def f(x,u):
    x,u  = x.flatten(), u.flatten()
    v,θ = x[2],x[3]
    return array([ [ v*cos(θ) ],[ v*sin(θ) ], [u[0]], [u[1]]])

def draw_field():
    Mx    = arange(xmin,xmax,0.2)
    My    = arange(ymin,ymax,0.2)
    X1,X2 = meshgrid(Mx,My)
    Nq1 = X1 - qhat[0,0]
    Nq2 = X2 - qhat[1,0]
    VX = vhat[0,0] - 2*(X1 - phat[0,0]) + Nq1/((Nq1**2+Nq2**2)**(3./2.))
    VY = vhat[1,0] - 2*(X2 - phat[1,0]) + Nq2/((Nq1**2+Nq2**2)**(3./2.))
    R = sqrt(VX**2+VY**2)
    quiver(Mx,My,VX/R,VY/R)

x    = array([[2,1,1,0]]).T #x,y,v,θ
dt   = 0.1
fig  = figure()
ax   = fig.add_subplot(111, aspect='equal')
xmin, xmax, ymin, ymax = -0, 10, -0, 10

for t in arange(0,7,dt):
    pause(0.001)
    cla()
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)

    phat = array([[t],[t]])
    qhat = array([[4.5+0.1*t],[5]])
    vhat = array([[1],[1]])

    nq = x[0:2] - qhat
    w = vhat - 2*(x[0:2]-phat) + nq/(norm(nq)**3)

    vbar, thetabar = norm(w), atan2(w[1,0],w[0,0])

    u = array([[vbar - x[2,0]],
               [10*atan(tan(0.5*(thetabar - x[3,0])))] ])

    x = x + dt*f(x,u)

    draw_tank(x[[0,1,3]],'red',0.2)
    plt.plot(phat[0,0], phat[1,0], "go", linewidth=3)
    plt.plot(qhat[0,0], qhat[1,0], "ro", linewidth=3)
    draw_field()
