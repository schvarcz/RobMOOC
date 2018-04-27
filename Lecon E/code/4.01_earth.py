# -*- coding: utf-8 -*-
from roblib import *
pi = np.pi


def T(lx,ly,ρ):
    return ρ*array([
        [cos(ly)*cos(lx)],
        [cos(ly)*sin(lx)],
        [sin(ly)],
    ])

def draw_earth():
    a = pi/10
    Lx = arange(0, 2*pi+a, a)
    Ly = arange(-pi/2, pi/2+a, a)
    M1 = T(0,-pi/2,ρ)
    for ly1 in Ly:
        for lx1 in Lx:
            M1 = hstack((M1, T(lx1,ly1,ρ)))
    M2 = T(0,-pi/2,ρ)
    for lx1 in Lx:
        for ly1 in Ly:
             M2 = hstack((M2, T(lx1,ly1,ρ)))
    plot3D(ax,M1,"blue")
    plot3D(ax,M2,"blue")


def draw_rob(x, col, size):
    x = x.flatten()
    lx,ly,ψ = x[0],x[1],x[2]
    M = array([
        [ 0,  0,  10,  0,   0,   10,   0,   0, ],
        [ -1,  1,  0, -1,  -0.2,  0,  0.2,  1, ],
        [ 0,  0,   0,  0,   1,    0,   1,   0, ] ])

    Rlatlong = array([
        [ -sin(lx), -sin(ly)*cos(lx), cos(ly)*cos(lx)],
        [ cos(lx) , -sin(ly)*sin(lx), cos(ly)*sin(lx)],
        [ 0       ,      cos(ly)    ,     sin(ly)    ] ])

    M = Rlatlong @ eulermat(0,0,ψ) @ M
    M=translate_motif(M,T(lx,ly,ρ))
    plot3D(ax, M, col, size)

def draw(xa,x):
    draw_earth()
    draw_rob(xa,'red',2)
    draw_rob(x,'black',2)

def f(x,u):
    x = x.flatten()
    lx,ly,ψ = x[0],x[1],x[2]
    return array([[cos(ψ)/(ρ*cos(ly))], [sin(ψ)/ρ], [u]])


fig = figure()
ax = Axes3D(fig)
ρ = 30
dt = 0.1
xa = array([[2],[0],[0]])
x = array([[1],[1],[1]])
e = 1


for t in arange(0,100,dt):
    cla()
    ax.set_xlim3d(-ρ,ρ)
    ax.set_ylim3d(-ρ,ρ)
    ax.set_zlim3d(-ρ,ρ)

    draw(xa,x)

    ua = 0.1*randn(1)
    xa = xa + dt*f(xa,ua)
    dx = xa - x
    A = array([[cos(x[2,0]), dx[0,0]*cos(x[1,0])],
               [sin(x[2,0]), dx[1,0]]])
    u = np.linalg.det(A)
    x = x + dt*f(x,u)
    plt.pause(0.001)

plt.show()
