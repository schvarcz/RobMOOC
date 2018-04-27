from roblib import *
from matplotlib import pyplot as plt
import numpy as np

l1, l2 = 4,3
Ls = np.matrix([l1,l2]).T
x = np.matrix([-1, 1]).T
c = np.matrix([1, 2]).T
r = 4
t = 1

def drawArm():
    rot1 = np.matrix([[np.cos(x[0,0]),0],
                        [np.sin(x[0,0]),0]])
    pts = rot1*Ls
    pts2 = y(x)
    plt.plot([0,pts[0,0]],[0,pts[1,0]], "k")
    plt.plot([pts[0,0],pts2[0,0]],[pts[1,0],pts2[1,0]], "k")

def drawCircle():
    draw_disk(c,r,ax,"cyan")

def A(x):
    return np.matrix([[-l1*np.sin(x[0,0]) - l2*np.sin(x.sum()), - l2*np.sin(x.sum())],
                    [l1*np.cos(x[0,0]) + l2*np.cos(x.sum()), l2*np.cos(x.sum())]])

def f(x):
    w  = c + r*np.matrix([cos(t), sin(t)]).T
    dw = r*np.matrix([-sin(t), cos(t)]).T
    v  = w - y(x) + dw
    plt.plot([c[0,0],w[0,0]],[c[1,0],w[1,0]],'black', linewidth = 1)
    return A(x).I*v

def y(x):
    rot = np.matrix([[np.cos(x[0,0]), np.cos(x.sum())],
                    [np.sin(x[0,0]),  np.sin(x.sum())]])
    return (rot*Ls)

plt.ion()
dt = 0.05
for t in arange(0,50.1,dt):
    plt.clf()
    ax = plt.subplot(111)
    print(f(x))
    x = x + dt*f(x)
    drawArm()
    drawCircle()
    plt.xlim(-4,8)
    plt.ylim(-4,8)
    plt.pause(0.01)
plt.show()
