# -*- coding: utf-8 -*-
from roblib import *
from matplotlib import pyplot as plt
import numpy as np

def f(x,u):
    return np.matrix([x[3,0]*cos(x[4,0])*cos(x[2,0]), x[3,0]*cos(x[4,0])*sin(x[2,0]), x[3,0]*sin(x[4,0])/3, u[0,0], u[1,0]]).T

def sawtooth(thetabar,theta):
    return np.arctan(tan((thetabar-theta)/2))

def angle(vdp):
    return np.arctan2(vdp[1,0],vdp[0,0])

def draw_field(xmin,xmax,ymin,ymax):
    Mx = arange(xmin,xmax,2)
    My = arange(ymin,ymax,2)
    X1,X2 = np.meshgrid(Mx,My)
    Vx = X2
    Vy = -(0.01*(X1*X1)-1)*X2-X1
    Vx = (1/(sqrt(Vx*Vx+Vy*Vy)))*Vx
    Vy = (1/(sqrt(Vx*Vx+Vy*Vy)))*Vy
    quiver(Mx,My,Vx,Vy)


dt = 0.05

x = np.matrix([0, 5, pi/2, 5, 0.5]).T # initial conditions

u = np.matrix([1, 1]).T

for t in arange(0,15,dt) :
    # displaying
    plt.pause(0.01)
    plt.clf()
    plt.xlim(-30,30)
    plt.ylim(-30,30)
    draw_car(x.A1)
    draw_field(-30,30,-30,30)

    # references
    vdp = np.matrix([ x[1,0], -(0.01*(x[0,0])**2-1)*x[1,0]-x[0,0] ]).T
    w = np.matrix([10, angle(vdp)]).T
    ubar = np.matrix([ w[0,0], 5*sawtooth(w[1,0],x[2,0])]).T
    u = 10*(ubar - np.matrix([x[3,0]*cos(x[4,0]), x[3,0]*sin(x[4,0])/3]).T)
    x = x + dt*f(x,u)
plt.show()
