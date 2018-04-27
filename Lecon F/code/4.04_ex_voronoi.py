from roblib import *
from numpy.linalg import norm, inv

def draw_circle(c,r,ax,col):
    e = Arc(c, 2*r, 2*r, angle=0, theta1=0, theta2=360)
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    e.set_edgecolor(col)


fig = figure(0)
ax = fig.add_subplot(111, aspect='equal')

m = 20
P = 10*rand(2,m)

C = np.zeros((3,1))
K = np.zeros((3,1))
for i in range(0,m-2):
    for j in range(i+1,m-1):
        for k in range(j+1,m):
            A = P[:,(i,j,k)]
            c = inv(np.hstack((2*np.transpose(A),-np.ones((3,1))))) @ np.transpose(np.sum(A*A,0))
            r = np.sqrt(norm(c[0:2])**2 - c[2])

            valid = True
            for q in range(0,m):
                valid = valid and (q==i or q==j or q==k or (norm(P[:,q]-c[0:2])>r))

            if valid:
                #draw_circle(c[0:2],r,ax,'blue')
                #plt.plot(c[0],c[1],'+m')
                #plt.plot(A[0,(0,1,2,0)],A[1,(0,1,2,0)],'red')

                C = np.hstack((C, array([[c[0]],[c[1]],[c[2]]])))
                K = np.hstack((K, np.matrix([i,j,k]).T))

for i in range(K.shape[1]):
    for j in range(K.shape[1]):
        a = K[0,i] in K[:,j]
        b = K[1,i] in K[:,j]
        c = K[2,i] in K[:,j]
        if (a + b + c) == 2:
            plt.plot(C[0,(i,j)],C[1,(i,j)],'green')

plt.plot(P[0],P[1],'or')

plt.xlim(-5,15)
plt.ylim(-5,15)
plt.show()
