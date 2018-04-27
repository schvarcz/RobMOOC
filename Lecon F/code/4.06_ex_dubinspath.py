from roblib import *
import numpy as np
from numpy import asarray
from math import atan2

def sawtooth2(x,d):
    return d*pi+(x+pi-d*pi)%(2*pi)-pi

def angle2(u,v):
    return sawtooth2(atan2(v[1,0],v[0,0])-atan2(u[1,0],u[0,0]),0)

def draw_circle(c,r,ax,col):
    e = Arc(c, 2*r, 2*r, angle=0, theta1=0, theta2=360)
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    e.set_edgecolor(col)

def path(a, b, r, epsa, epsb, ax):
    ca = a[0:2,:] + epsa*r*np.matrix([-sin(a[2,0]), cos(a[2,0])]).T
    cb = b[0:2,:] + epsb*r*np.matrix([-sin(b[2,0]), cos(b[2,0])]).T

    plt.plot([ca[0,0],cb[0,0]], [ca[1,0],cb[1,0]], "ko")
    draw_circle(ca, r, ax, 'k')
    draw_circle(cb, r, ax, 'b')

    if epsa*epsb == -1:
        e112 = 0.25*norm(cb-ca)**2 - r**2
        if e112 < 0:
            return float("inf")
        e11 = sqrt(e112)
        alpha = -epsa*atan2(e11, r)
    elif epsa*epsb == 1:
        e11 = 0.5*norm(cb-ca)
        alpha = -epsa*np.pi/2

    da = ca + (r/norm(cb-ca))* np.matrix([[cos(alpha), -sin(alpha)],
                                          [sin(alpha),  cos(alpha)]])*(cb-ca)
    db = cb + epsa*epsb*(da - ca)
    betaA = sawtooth2(angle2(a[0:2] - ca, da-ca), epsa)
    betaB = sawtooth2(angle2(db-cb, b[0:2] - cb), epsb)

    draw_arc(asarray(ca), asarray(a[0:2,:]), betaA,"black")
    draw_arc(asarray(cb), asarray(b[0:2,:]),-betaB,"black")
    plt.plot([da[0,0],db[0,0]],[da[1,0],db[1,0]],"r", linewidth=2.0)
    return r*abs(betaA)+r*abs(betaB) + 2*e11

fig = figure(0)

r=10
a, b, ech = np.matrix([-25,0,pi/2]).T, np.matrix([25,0,pi/2]).T, 50


pltN = 1
minL, minCode = float("inf"), ""
for epsa in arange(-1,2,2):
    for epsb in arange(-1,2,2):
        ax = fig.add_subplot(220 + pltN, aspect='equal')
        ax.set_xlim(-ech,ech)
        ax.set_ylim(-ech,ech)
        draw_tank(a.A1,"black")
        draw_tank(b.A1,"blue")
        L = path(a, b, r, epsa, epsb, ax)
        ax.set_title("L"+str(pltN))
        if L < minL:
            minL, minCode = L, "L"+str(pltN)
        pltN += 1

print(minCode + " is the minimum path.")

plt.show()
