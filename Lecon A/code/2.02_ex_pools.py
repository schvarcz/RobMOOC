from roblib import *

def draw_pools(x):
    x=x.A1.flatten()
    plot([0,0],[10,1],'black',linewidth=2)
    plot([-7,23],[0,0],'black',linewidth=5)
    plot([16,16],[1,10],'black',linewidth=2)
    plot([4,4,6,6],[10,1,1,10],'black',linewidth=2)
    plot([10,10,12,12],[10,1,1,10],'black',linewidth=2)
    P=array([[0,x[0]],[0,1],[-6,0],[22,0],[16,1],[16,x[2]],[12,x[2]],[12,1]
            ,[10,1],[10,x[1]],[6,x[1]],[6,1],[4,1],[4,x[0]]])
    draw_polygon(P,ax,'blue')
    P=array([[1,10],[1,x[0]],[1+0.1*u[0],x[0]],[1+0.1*u[0],10]])
    draw_polygon(P,ax,'blue')
    P=array([[13,10],[13,x[2]],[13+0.1*u[1],x[2]],[13+0.1*u[1],10]])
    draw_polygon(P,ax,'blue')


def alpha(h):
    q = 0.4*np.sign(h) + sqrt(2*9.81*np.absolute(h))
    return q

def f(x,u):
    xdot = np.matrix([-alpha(x[0,0]) - alpha(x[0,0] - x[1,0]) + u[0,0],
                  alpha(x[0,0]-x[1,0]) - alpha(x[1,0] - x[2,0]),
                  -alpha(x[2,0]) + alpha(x[1,0] - x[2,0]) + u[1,0]]).T
    return xdot

dt = 0.05
x = np.matrix([4, 5,2]).T
u = np.matrix([1, 2]).T
ax = init_figure(-10,25,-2,12)

ref  = np.matrix([10, 3]).T
dref = np.matrix([0, 0]).T
z = np.matrix([0, 0]).T

for t in arange(0,1,dt):
    y = np.matrix([x[0,0],x[2,0]]).T
    ref = ref + dt*dref
    z = z + dt*(ref-y)
    v = z + 2*(ref-y) + dref
    b = np.matrix([-alpha(x[0,0]) -  alpha(x[0,0] - x[1,0]),
                    -alpha(x[2,0]) + alpha(x[1,0] - x[2,0])]).T
    u = v - b
    x = x + dt*f(x,u)
    clear(ax)
    draw_pools(x)
    x = x + dt*f(x,u)
