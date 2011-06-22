from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = Axes3D(fig)
# ax = fig.gca(projection='3d')
# ax = fig.add_subplot(111, projection='3d')

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

# x = 10 * np.outer(np.cos(u), np.sin(v))
# y = 10 * np.outer(np.sin(u), np.sin(v))
# z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))
# ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b')

#ax.plot_surface(np.array([0,1,1,0]),np.array([0,0,1,1]),np.zeros((4,4)))
ax.plot_surface(np.array([0,1,1,0]),np.array([0,0,1,1]),np.zeros(4))
#ax.plot_surface(np.array([[0,1],[1,1]]),np.array([[0,0],[1,1]]),np.array([[0,0],[1,1]]))

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
