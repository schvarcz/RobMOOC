from roblib import *
from math import atan2, atan

def f(x,u):
    x,u = x.flatten(),u.flatten()
    θ = x[2]; v = x[3]; w = x[4]; deltar = u[0]; deltasmax = u[1];
    w_ap = array([[awind*cos(psi-θ) - v],
                    [awind*sin(psi-θ)]])
    psi_ap = np.arctan2(w_ap[1,0], w_ap[0,0])
    a_ap = norm(w_ap)
    sigma = cos(psi_ap) + cos(deltasmax)
    if sigma < 0 :
        deltas = pi + psi_ap
    else :
        deltas = -sign(sin(psi_ap))*deltasmax
    fr = p[4]*v*sin(deltar)
    fs = p[3]*a_ap* sin(deltas - psi_ap)
    dx = v*cos(θ) + p[0]*awind*cos(psi)
    dy = v*sin(θ) + p[0]*awind*sin(psi)
    dv = (fs*sin(deltas)-fr*sin(deltar)-p[1]*v**2)/p[8]
    dw = (fs*(p[5]-p[6]*cos(deltas)) - p[7]*fr*cos(deltar) - p[2]*w*v)/p[9]
    xdot = array([ [dx],[dy],[w],[dv],[dw]])
    return xdot


def control(x,q):
    theta = x[2,0]
    m = np.array([[x[0,0], x[1,0]]]).T
    phi = atan2(b[1,0]-a[1,0], b[0,0]-a[0,0])

    e = np.vstack(((b-a)/norm(b-a), m-a))
    mat = np.array([[b[0,0]-a[0,0], m[0,0]-a[0,0]],[b[1,0]-a[1,0], m[1,0]-a[1,0]]])
    e = np.linalg.det(mat)/np.linalg.norm(b-a)
    if np.absolute(e)>r:
        q = np.sign(e)

    thetabar = phi - atan(e/r)
    if cos(psi-thetabar)+cos(zeta) < 0:
        thetabar = pi + psi - zeta*q
    deltar = (2/np.pi)*atan(tan(0.5*(theta-thetabar)))
    deltasmax = pi/4*(cos(psi-thetabar)+1)
    u = array([[deltar, deltasmax]]).T
    return u, q

fig = figure(0)
ax = plt.subplot(111, aspect='equal')

x = array([[10, 20, -3, 1, 0]]).T  #x=(x,y,θ,v,w)
p = [0.1, 1, 6000, 1000, 2000, 1, 1, 2, 300, 10000]

psi = 3*pi/2
dt = 0.1
awind = 2
r = 10
zeta = np.pi/4


a = np.array([[-100],[-5]])
b = np.array([[100],[20]])

u = array([[0, 1]]).T
q = 1
deltas = 0

for t in arange(0,50,dt):
    u, q = control(x,q)
    x = x + dt*f(x,u)

    plt.cla()
    plt.plot([a[0,0],b[0,0]],[a[1,0],b[1,0]],'red')
    draw_sailboat(x,deltas,u[0,0],psi,awind)
    ax.set_xlim([-100,100])
    ax.set_ylim([-60,60])
    plt.pause(0.001)

plt.ioff()
plt.show()
