from roblib import *

def f(x,u):
    θ = x[2]
    return array([cos(θ), sin(θ), u])

ax = init_figure(-60,60,-60,60)
m  = 20
X  = 20*randn(3,m)
dt = 0.2

for t in arange(0,100,dt):
    clear(ax)
    for i in range(m):
        H = zeros((2, 2*(m-1)))
        k = 0
        for j in range(m):
            if j != i:
                v = array([cos(X[2,j]),sin(X[2,j])])
                H[:,k] = v
                k += 1
                dp = array([X[0,i]-X[0,j], X[1,i]-X[1,j]])
                v  = -0.01*dp + dp*20/(norm(dp)**3)
                v  = v/norm(v)
                H[:,k] = v
                k += 1

        Hbar = mean(H,1)
        u = sawtooth(angle(Hbar)-X[2,i])
        X[:,i] = X[:,i] + dt*f(X[:,i],u)
        draw_tank(X[:,i],"darkblue")
