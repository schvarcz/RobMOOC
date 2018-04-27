from roblib import *

fig = figure()
ax = Axes3D(fig)

def draw(x,r):
    Auv0 = np.matrix([ [0.0,0.0,10.0,0.0,0.0,10.0,0.0,0.0],
                  [-1.0,1.0,0.0,-1.0,-0.2,0.0,0.2,1.0],
                  [0.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0]])
    w0 = 0.1*Auv0

    Auv0 = np.vstack((Auv0, ones((1,Auv0.shape[1]))))
    w0 = np.vstack((w0, ones((1,Auv0.shape[1]))))

    E = eulermat(x[6,0],x[5,0],x[4,0])

    R = np.vstack((E, zeros((1,3))))
    Rw = np.hstack((R, np.matrix([r[0,0], r[1,0], r[2,0], 1]).T))
    R = np.hstack((R, np.matrix([x[0,0], x[1,0], x[2,0], 1]).T))

    Auv = R*Auv0
    w1 = Rw*w0

    ax.clear()
    ax.set_xlim3d(-25,25)
    ax.set_ylim3d(-15,25)
    ax.set_zlim3d(-10,25)
    ax.plot(Auv[0].A1,Auv[1].A1,Auv[2].A1,"b")
    ax.plot(Auv[0].A1,Auv[1].A1,0*Auv[2].A1,"k")
    ax.plot(w1[0].A1,w1[1].A1,w1[2].A1,"r")

def f(x,u):
    v=x[3,0]; ψ=x[4,0]; θ=x[5,0]; φ=x[6,0];
    return np.matrix([v*cos(θ)*cos(ψ),
                  v*cos(θ)*sin(ψ),
                  -v*sin(θ),
                  u[0,0],
                  (sin(φ)/cos(θ)) * v * u[1,0] + (cos(φ)/cos(θ)) * v * u[2,0],
                  cos(φ) * v * u[1,0] - sin(φ) * v * u[2,0],
                  -0.1 * sin(φ) * cos(θ) + tan(θ) * v * (sin(φ) * u[1,0] + cos(φ) * u[2,0])]).T

def control(x,r,dr,ddr):
    v = x[3,0]
    psi = x[4,0]
    theta = x[5,0]
    phi = x[6,0]
    ct = cos(theta)
    st = sin(theta)
    cf = cos(phi)
    sf = sin(phi)
    cp = cos(psi)
    sp = sin(psi)
    A1 = np.matrix([[ct*cp, -v*ct*sp, -v*st*cp],
                    [ct*sp, v*ct*cp, -v*st*sp],
                    [-st, 0, -v*ct]])
    A2 = np.matrix([[1, 0, 0],
                    [0, sf/ct, cf/ct],
                    [0, cf, -sf]])
    A = A1*A2
    dp = np.matrix([ct*cp, ct*sp, -st]).T
    p  = x[0:3]
    u  = A.I*(0.04*(r-p) + 0.4*(dr-dp) + ddr)
    return u

def setpoint(t):
    f1=0.01
    f2=6*f1
    f3=3*f1
    R=20
    r   = R*np.matrix([sin(f1*t)+sin(f2*t),
                       cos(f1*t)+cos(f2*t),
                       sin(f3*t)]).T
    dr  = R*np.matrix([f1*cos(f1*t)+f2*cos(f2*t),
                      -f1*sin(f1*t)-f2*sin(f2*t),
                       f3*cos(f3*t)]).T
    ddr = R*np.matrix([-(f1**2)*sin(f1*t)-(f2**2)*sin(f2*t),
                       -(f1**2)*cos(f1*t)-(f2**2)*cos(f2*t),
                       -(f3**2)*sin(f3*t)]).T
    return r, dr, ddr

if __name__ == '__main__':
    x = np.matrix([0,0,1,0.1,0,0,0]).T
    u = np.matrix([0,0,0.0]).T
    dt = 0.1
    for t in arange(0,10,dt):
        r, dr, ddr = setpoint(t)
        u = control(x,r,dr,ddr)
        x = x + dt*f(x,u)
        draw(x, r)
        plt.pause(0.001)
    plt.show()
