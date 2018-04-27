# -*- coding: utf-8 -*-
from roblib import *
from math import atan, atan2

def draw(x,u,ax):
    x,u        = x.flatten(),u.flatten()
    plane    = array([[0,  0, 6, 0,  0, 0,   0,   1, 6, 0],
                      [0, -1, 0, 1, -1, 0,   0,   0, 0, 0],
                      [0,  0, 0, 0,  0, 0,   1, 0.2, 0, 0],
                      [1,  1, 1, 1,  1, 1,   1,   1, 1, 1]])
    e        = 0.5
    flap  = array([[-e,  0, 0, -e, -e],[-e, -e, e,  e, -e],
                      [ 0,  0, 0,  0,  0],[ 1,  1, 1,  1,  1]])

    R        = hstack((     eulermat(-x[3],-x[4],x[5]),
                            array([[x[0],x[1],-x[2]]]).T
                     ))
    R        = vstack((R,array([[0, 0, 0, 1]])))

    def draw_flap(ua,s):
        R1  = hstack((eulermat(0,ua,0),array([[0,s,0]]).T))
        R1  = vstack((R1,array([[0,0,0,1]])))
        flap1  = R @ R1 @ flap
        ax.plot(flap1[0,:],flap1[1,:],flap1[2,:],'red')
        return

    plane    = R @ plane

    # ax.clear()
    L=15
    ax.set_xlim3d(-L,L)
    ax.set_ylim3d(-L,L)
    ax.set_zlim3d(-L/10,L)
    draw_flap(-u[1]+u[2],1-e)    #left flap
    draw_flap(-u[1]-u[2],e-1)    #right flap
    ax.plot(plane[0,:],plane[1,:],plane[2,:],'blue')          # drone
    ax.plot(plane[0,:],plane[1,:],0*plane[2,:],'black')       # ombre du drone
    ax.plot(Cx0,Cy0,Cz0,'green')                              # cercle consigne

def f(x,u):
    v     = x[6:9]
    w     = x[9:12]
    x,u=x.flatten(),u.flatten()
    V     = norm(v)
    α = arctan(x[8]/x[6])
    β  = arcsin(x[7]/V)
    φ,θ,ψ = x[3],x[4],x[5]
    cf,sf,ct,st,tt,ca,sa,cb,sb = cos(φ),sin(φ),cos(θ),sin(θ),tan(θ),cos(α),sin(α),cos(β),sin(β)
    Fa= 0.002*(V**2)*array([[-ca*cb,ca*sb,sa],[sb,cb,0],[-sa*cb,sa*sb,-ca]])  \
            @  \
            array([[4+(-0.3+10*α+10*w[1,0]/V+2*u[2]+0.3*u[1])**2+abs(u[1])+3*abs(u[2])],
                   [-50*β + 10*(w[2,0]-0.3*w[0,0])/V],
                   [10+500*α+400*w[1,0]/V+50*u[2]+10*u[1]]])

    return vstack((
                         eulermat(φ,θ,ψ) @ v,
                         eulerderivative(φ,θ,ψ)@ w,
                         9.81*array([[-st],[ct*sf],[ct*cf]])+Fa+array([[u[0]],[0],[0]]) - cross(w.T,v.T).T,
                         array([ -w[2]*w[1]+0.1*(V**2)*(-β -2*u[2]+(-5*w[0]+w[2])/V),
                                w[2]*w[0]+0.1*(V**2)*(-0.1-2*α+0.2*u[2]-3*u[1]-30*w[1]/V),
                                0.1*w[0]*w[1]+0.1*(V**2)*(β+0.5*u[2]+0.5*(w[0]-2*w[2])/V)])
                         ))

def control(x):
    v = norm(x[6:9])
    phi, theta, psi = x[3], x[4], x[5]
    thetabar = -0.2*atan(0.1*(zbar-x[2]))
    psibar = atan2(x[1], x[0]) + 0.5*pi+atan((norm(x[0:2]) - rbar)/50)
    phibar = 0.5*atan(5*atan(tan(0.5*(psibar-psi))))
    u = array([[5*(1+2/pi*atan(vbar-v))],
              [-0.3*(2/pi*atan(5*(thetabar-theta)) + np.absolute(sin(phi)))],
              [-0.3*(2/pi)*atan(phibar-phi)]])
    return u


fig   = figure()
ax    = Axes3D(fig)

x = array([[0, 0, -5, 0, 0, 0, 30, 0, 0, 0, 0, 0]]).T   #x=[x;y;z;phi;theta;psi;v;w]
dt = 0.02
vbar,zbar,rbar = 15,-50,100

u = array([[10, 0, 0]]).T

a    = arange(0,2*pi+0.1, 0.1)
Cx0, Cy0, Cz0 = rbar*np.cos(a), rbar*np.sin(a), [-zbar]*len(a) #circle to follow
k=0
for t in arange(0,50,dt):
    u = control(x)
    x = x + dt*f(x,u)
    if k%20 == 0:
        draw(x, u, ax)
        ax.set_xlim3d(-100,100)
        ax.set_ylim3d(-100,100)
        ax.set_zlim3d(-100,100)
        plt.pause(0.001)
    k = k + 1
plt.show()
