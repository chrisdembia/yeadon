import matplotlib.pyplot as mpl
from pylab import *
import numpy as np
import stadium

s1 = stadium.stadium(10.0,4.0)
print s1.t
print s1.r

s2 = stadium.stadium(8.0,3.5)

theta = [np.linspace(0.0,np.pi/2.0,5)]

x = s1.t + s1.r * np.cos(theta);
y = s1.r * np.sin(theta);

xrev = x[:, ::-1]
yrev = y[:, ::-1]

X = np.concatenate( (x, -xrev, -x, xrev) )
Y = np.concatenate( (y, yrev, -y, -yrev) )
c = 'g'

# fill(X,Y,c,edgecolor='g', alpha = 0.5)

#fill(x,y,'b')
# show()


s1.plot()
