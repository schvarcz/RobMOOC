from roblib import *

def f(x,u):
    θ = x[2,0]
    return array([[cos(θ)],[sin(θ)],[u]])

def control(x):
    thetabar = pi/2 + 10*pi
    thetatilde = thetabar - x[2,0]

    u = np.mod(thetatilde+pi,2*pi) - pi                # Question 1
    u = np.mod(thetatilde,2*pi)                        # Question 2
    u = np.mod(thetatilde,2*pi) - 2*pi + 0.1*randn(1)  # Question 3
    return u

x  = array([[0],[0],[0]])
dt = 0.05
ax = init_figure(-10,10,-10,10)

for t in arange(0,30,dt):
    pause(0.001)
    cla()
    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)
    u = control(x)
    x = x + dt*f(x,u)
    draw_tank(x,'red',0.3)
