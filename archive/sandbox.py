import stadium
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import data
import mymath
import densities

fig = mpl.figure()
ax = Axes3D(fig)
ax.axis('equal')
s1 = stadium.stadium('thickradius',1.0,0.5)
print s1.thick
print s1.radius

s2 = stadium.stadium('thickradius',0.5,0.2)
print s2.thick
print s2.radius

height = 5

#s1.plot(ax,'r')
#s2.plot(ax,'g')

pos = np.array([0,0,0])
direct = np.array([0,0,0])

theta = pos
S0 = stadium.stadiumsolid(densities.Ds[0],pos,direct,'r',s1,s2,height)

S0.draw(ax)
S0.calcLocalProperties()

pos = np.array([0,0,0])
direct = np.array([np.pi/10,0,0])

theta = pos
print np.arange(2)
S1 = stadium.stadiumsolid(densities.Ds[0],pos,direct,'g',s1,s2,height)

S1.draw(ax)
S1.calcLocalProperties()

pos = np.array([0,0,0])
direct = np.array([np.pi/10,np.pi/10,0])

theta = pos
print np.arange(2)
S2 = stadium.stadiumsolid(densities.Ds[0],pos,direct,'b',s1,s2,height)

S2.draw(ax)
S2.calcLocalProperties()
pos = np.array([0,0,0])
direct = np.array([np.pi/10,np.pi/10,np.pi/2])

theta = pos
print np.arange(2)
S3 = stadium.stadiumsolid(densities.Ds[0],pos,direct,'k',s1,s2,height)

S3.draw(ax)
S3.calcLocalProperties()

# ax.set_aspect('equal', 'datalim')













if 0:
	theta = [np.linspace(0.0,np.pi/2.0,5)]
	x = s1.thick + s1.radius * np.cos(theta);
	y = s1.radius * np.sin(theta);

	xrev = x[:, ::-1]
	yrev = y[:, ::-1]

	X2 = np.concatenate( (x, -xrev, -x, xrev ), axis = 1 )
	Y2 = np.concatenate( (y, yrev, -y, -yrev ), axis = 1 )
	Z2 = np.zeros( (1,20) )

	POS = np.concatenate( (X2, Y2, Z2), axis = 0 )

	orienT = np.array([np.pi/2,np.pi/2,np.pi/2])
	orienT = np.array([0,0,np.pi/2])
	POS2 = mymath.Rotate3(orienT) * POS
		
	Xtoplot,Ytoplot,Ztoplot = np.vsplit(POS2,3)

	Xtoplot = np.array(np.concatenate( (Xtoplot, np.nan*Xtoplot) , axis = 0 ))
	Ytoplot = np.array(np.concatenate( (Ytoplot, np.nan*Ytoplot) , axis = 0 ))
	Ztoplot = np.array(np.concatenate( (Ztoplot, np.nan*Ztoplot) , axis = 0 ))

	c = 'r'

	ax.plot_surface( Xtoplot, Ytoplot, Ztoplot, color=c, alpha = 0.5 )


ax.plot( np.array([-1,1]) , np.array([0,0]), np.array([0,0]) )
ax.plot( np.array([0,0]) , np.array([-1,1]), np.array([0,0]) )
ax.plot( np.array([0,0]) , np.array([0,0]), np.array([-1,1]) )

ax.text(1,0,0,'x')
ax.text(0,1,0,'y')
ax.text(0,0,1,'z')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.axis('off')

ax.set_xlim3d(-3, 3)
ax.set_ylim3d(-3, 3)
ax.set_zlim3d(-3, 3)


# ax.axis('equal')

mpl.show()

