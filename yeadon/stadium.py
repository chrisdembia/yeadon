import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import mymath

class stadium:
	'''Define a 2D stadium shape. First argument is the perimeter p, and the second is the total width w. If an optional third argument is specified as 1, then the first argument is the half length of the rectangle t, and the second argument is the radius of the semicircle ends. The third argument defaults to 0.'''
	def __init__(self,inID,in1,in2, alignment = 'ML' ):
		'''Must add error checking for negatives etc.'''
		if inID == 'perimwidth':
			self.perim = in1
			self.width = in2
			self.thick = (np.pi*self.width- self.perim) /(2.0*np.pi-4.0)
			self.radius = (self.perim - 2.0*self.width)   /(2.0*np.pi-4.0)
		elif inID == 'depthwidth':
			self.width = in2
			self.perim = 2.0*in2 + (np.pi - 2.0)*in1
			self.thick = (np.pi*self.width - self.perim) /(2.0*np.pi-4.0)
			self.radius = (self.perim - 2.0*self.width)    /(2.0*np.pi-4.0)
		elif inID == 'perim':
			self.perim = in1
			self.width = self.perim/np.pi
			self.thick = 0.0
			self.radius = self.perim/(2.0*np.pi)
		elif inID == 'thickradius':
			self.thick = in1
			self.radius = in2
			self.perim = 4.0*self.thick + 2.0*np.pi*self.radius
			self.width = 2.0*self.thick + 2.0*self.radius
		else:
			print "Error: stadium not defined properly, must use inID pw, dw, or p"
		
		if self.radius <= 0 or self.thick < 0:
			print "Error: a stadium is defined incorrectly, r must be positive and t must be nonnegative. r = ", self.radius, " and t = ", self.thick, "."

		if alignment == 'AP':
			print "do something"
		elif alignment != 'AP' and alignment != 'ML':
			print "Error: stadium alignment is not valid, must be either AP or ML"

	def plot(self,ax,c):
		theta = [np.linspace(0.0,np.pi/2.0,5)]
		x = self.thick + self.radius * np.cos(theta);
		y = self.radius * np.sin(theta);
		xrev = x[:, ::-1]
		yrev = y[:, ::-1]
		X2 = np.concatenate( (x, -xrev, -x, xrev ), axis = 1 )
		Y2 = np.concatenate( (y, yrev, -y, -yrev ), axis = 1 )
		X3 = np.concatenate( (X2, np.nan*X2), axis = 0 )
		Y3 = np.concatenate( (Y2, np.nan*Y2), axis = 0 )
		ax.plot_surface(X3,Y3, np.zeros((2,20)), color=c, alpha = 0.5 )
		
class solid:
	def __init__(self,label,density,pos,orient,RotMat):
		self.label = label
		self.density = density
		self.pos = pos
		self.orient = orient
		self.RotMat = RotMat
	def draw(self,ax,c):
		print "cannot draw base class"

class stadiumsolid(solid):
	def __init__(self,label,density,pos,orient,RotMat,stadium0,stadium1,height):
		solid.__init__(self,label,density,pos,orient,RotMat)
		self.stads = [stadium0,stadium1]
		self.height = height
		# DEPENDS IF IT'S ML OR NOT

		self.calcLocalProperties()
		
	def calcLocalProperties(self):
		D = self.density
		h = self.height
		r0 = self.stads[0].radius
		t0 = self.stads[0].thick
		r1 = self.stads[1].radius
		t1 = self.stads[1].thick
		a = (r1 - r0)/r0
		if ( t0 == 0 ):
			b = 1.0
		else:
			b = (t1 - t0)/t0 # DOES NOT WORK FOR CIRCLES!!! 
		self.Mass = D*h*r0*(4.0*t0*self.F1(a,b) + np.pi*r0*self.F1(a,a))
		zcom = D*(h**2.0)*(4.0*r0*t0*self.F2(a,b) + np.pi*(r0**2.0)*self.F2(a,a))/self.Mass
		self.localCOM = np.array([[0.0],[0.0],[zcom]])
		self.absCOM = self.pos + self.RotMat * self.localCOM
		
		# moments of inertia
		Izcom = D*h*(4.0*r0*(t0**3.0)*self.F4(a,b)/3.0 + np.pi*(r0**2.0)*(t0**2.0)*self.F5(a,b) + 4.0*(r0**3.0)*t0*self.F4(b,a) + np.pi*(r0**4.0)*self.F4(a,a)*0.5)
		
		Iy = D*h*(4.0*r0*(t0**3.0)*self.F4(a,b)/3.0 + np.pi*(r0**2.0)*(t0**2.0)*self.F5(a,b) + 8.0*(r0**3.0)*t0*self.F4(b,a)/3.0 + np.pi*(r0**4.0)*self.F4(a,a)*0.25) + D*(h**3.0)*(4.0*r0*t0*self.F3(a,b) + np.pi*(r0**2.0)*self.F3(a,a))
		# CAUGHT AN ERROR IN YEADON'S PAPER HERE
		Iycom = Iy - self.Mass*(zcom**2.0)
		
		Ix = D*h*(4.0*r0*(t0**3.0)*self.F4(a,b)/3.0 + np.pi*(r0**4.0)*self.F4(a,a)*0.25) + D*(h**3.0)*(4.0*r0*t0*self.F3(a,b) + np.pi*(r0**2.0)*self.F3(a,a))
		
		Ixcom = Iy - self.Mass*(zcom**2.0)
	
		self.localI = np.mat([[Ixcom,0.0,0.0],
		                      [0.0,Iycom,0.0],
		                      [0.0,0.0,Izcom]])

	def draw(self,ax,c):
		'''Draws stadium solid according to ....EDIT'''	
		X0,Y0,Z0,X0toplot,Y0toplot,Z0toplot = self.makePos(0)
		X1,Y1,Z1,X1toplot,Y1toplot,Z1toplot = self.makePos(1)

		for idx in np.arange(X0.size-1):
			Xpts = np.array([[X0[0,idx],X0[0,idx+1]],[X1[0,idx],X1[0,idx+1]]])
			Ypts = np.array([[Y0[0,idx],Y0[0,idx+1]],[Y1[0,idx],Y1[0,idx+1]]])
			Zpts = np.array([[Z0[0,idx],Z0[0,idx+1]],[Z1[0,idx],Z1[0,idx+1]]])
			ax.plot_surface( Xpts, Ypts, Zpts, color = c, alpha = 0.5, edgecolor = '')

		# draw stad0
		ax.plot_surface( X0toplot, Y0toplot, Z0toplot, color=c, alpha = 0.5 )
		
		# draw stad1
		ax.plot_surface( X1toplot, Y1toplot, Z1toplot, color=c, alpha = 0.5 )
		
		ax.text(self.absCOM[0],self.absCOM[1],self.absCOM[2],self.label)
		
	def makePos(self,i):
		theta = [np.linspace(0.0,np.pi/2.0,5)]
		x = self.stads[i].thick + self.stads[i].radius * np.cos(theta);
		y = self.stads[i].radius * np.sin(theta);

		xrev = x[:, ::-1]
		yrev = y[:, ::-1]

		X = np.concatenate( (x, -xrev, -x, xrev ), axis = 1 )
		Y = np.concatenate( (y, yrev, -y, -yrev ), axis = 1 )
		Z = i*self.height*np.ones( (1,20) )

		POSES = np.concatenate( (X, Y, Z), axis = 0 )
		POSES = self.RotMat * POSES
		X,Y,Z = np.vsplit(POSES,3)
		
		X = X + self.pos[0]
		Y = Y + self.pos[1]
		Z = Z + self.pos[2]
		
		Xtoplot = np.array(np.concatenate( (X, np.nan*X) ) )
		Ytoplot = np.array(np.concatenate( (Y, np.nan*Y) ) )
		Ztoplot = np.array(np.concatenate( (Z, np.nan*Z) ) )
		
		return X,Y,Z,Xtoplot,Ytoplot,Ztoplot

	def F1(self,a,b):
		'''See Yeadon 1990-ii Appendix 2.'''
		return 1.0 + (a+b)*0.5 + a*b/3.0
	def F2(self,a,b):
		'''See Yeadon 1990-ii Appendix 2.'''
		return 0.5 + (a+b)/3.0 + a*b*0.25
	def F3(self,a,b):
		'''See Yeadon 1990-ii Appendix 2.'''
		return 1.0/3.0 + (a+b)/4.0 + a*b*0.2
	def F4(self,a,b):
		'''See Yeadon 1990-ii Appendix 2.'''
		return 1.0 + (a+3.0*b)*0.5 + (a*b + b**2.0) + (3.0*a*b**2.0 + b**3.0)*0.25 + a*(b**3.0)*0.2
	def F5(self,a,b):
		'''See Yeadon 1990-ii Appendix 2.'''
		return 1.0 + (a+b) + (a**2.0 + 4.0*a*b + b**2.0)/3.0 + a*b*(a+b)*0.5 + (a**2.0)*(b**2.0)*0.2
		
class semiellipsoid(solid):
	def __init__(self,label,density,pos,orient,RotMat,baseperim,height):
		solid.__init__(self,label,density,pos,orient,RotMat)
		self.baseperimeter = baseperim
		self.radius = self.baseperimeter/(2.0*np.pi)
		self.height = height

		self.calcLocalProperties()
		
	def draw(self,ax,c):
		'''Code is modified from matplotlib documentation for mplot3d.'''
		N = 30
		u = np.linspace(0, 2.0 * np.pi, N)
		v = np.linspace(0, np.pi/2.0, N)

		x = self.radius * np.outer(np.cos(u), np.sin(v))
		y = self.radius * np.outer(np.sin(u), np.sin(v))
		z = self.height * np.outer(np.ones(np.size(u)), np.cos(v))
		
		for i in np.arange(N):
			for j in np.arange(N):
				POS = np.array([[x[i,j]],[y[i,j]],[z[i,j]]])
				POS = self.RotMat * POS
				x[i,j] = POS[0,0]
				y[i,j] = POS[1,0]
				z[i,j] = POS[2,0]
			
		x = self.pos[0,0] + x
		y = self.pos[1,0] + y
		z = self.pos[2,0] + z		

		# must rotate the x y and z
		ax.plot_surface(x, y, z, rstride=4, cstride=4, color=c, alpha = 0.5, edgecolor ='')
		
		ax.text(self.absCOM[0],self.absCOM[1],self.absCOM[2],self.label)
	
	def calcLocalProperties(self):
		D = self.density
		r = self.radius
		h = self.height
		self.Mass = D*2.0/3.0*np.pi*(r**2)*h
		self.localCOM = np.array([[0.0],[0.0],[3.0/8.0*h]])
		self.absCOM = self.pos + self.RotMat * self.localCOM
		
		Izcom = D*4.0/15.0*np.pi*(r**4.0)*h
		Iycom = D*np.pi*( 2.0/15.0*(r**2.0)*h*(r**2.0+h**2.0) - 3.0/32.0*(r**2.0)*(h**3.0) )
		Ixcom = Iycom
		self.localI = np.mat([[Ixcom,0.0,0.0],
		                      [0.0,Iycom,0.0],
		                      [0.0,0.0,Izcom]])
		

