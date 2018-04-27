# -*- coding: utf-8 -*-
from roblib import *
from matplotlib import pyplot as plt
import numpy as np

def f(x,u):
    return np.matrix([5*cos(x[2,0]), 5*sin(x[2,0]), u]).T

def control(x):
    alpha = np.arctan2(x[1,0],x[0,0])
    phi = np.pi + x[2,0] - alpha
    if cos(phi) < (2**0.5)/2:
        u = 1
    else:
        u = -sin(phi)
    return u


fig = figure(0)
ax = fig.add_subplot(111, aspect='equal')
dt = 0.3

x = np.matrix([15, 20, 1]).T # initial conditions
a = np.matrix([-30, -4]).T
b = np.matrix([30, 6]).T

u = 0.1

thetabar = 0
for t in arange(0,50,dt) :
    # displaying
    plt.pause(0.01)
    plt.cla()
    plt.xlim(-30,30)
    plt.ylim(-30,30)
    draw_disk([0,0], 10, ax, col="green")

    # controlling
    if u==1:
        color = 'blue'
    else:
        color = 'red'

    draw_tank(x.A1,color)

    u = control(x)
    x = x + dt*f(x,u)
plt.show()
