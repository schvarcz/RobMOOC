# -*- coding: utf-8 -*-
from roblib import *
from matplotlib import pyplot as plt
import numpy as np

def f(x,u):
    return np.matrix([cos(x[2,0]), sin(x[2,0]), u]).T


fig = plt.figure()
dt = 0.5

x = np.matrix([-20, -10, 4]).T # initial conditions

a = np.matrix([-30, -4]).T

b = np.matrix([30, 6]).T

u = np.matrix([0])

thetabar=0
for t in arange(0,30,dt):
    phi = np.arctan2(b[1,0]-a[1,0],b[0,0]-a[0,0])
    m = np.matrix([x[0,0], x[1,0]]).T
    col0 = b-a
    col1 = m-a
    mat = np.matrix([[b[0,0]-a[0,0], m[0,0]-a[0,0]],
                     [b[1,0]-a[1,0], m[1,0]-a[1,0]]])

    e = np.linalg.det(mat)/np.linalg.norm(b-a)
    thetabar = phi - np.arctan(e)
    u = np.arctan(tan((thetabar - x[2,0])/2))
    x = x + dt*f(x,u)

    plt.clf()
    plt.xlim(-30,30)
    plt.ylim(-30,30)
    plt.plot([a[0,0], b[0,0]], [a[1,0],b[1,0]], color='magenta')
    draw_tank(x.A1,'red')
    plt.pause(0.01)
