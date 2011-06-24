import solid
import numpy as np
import inertia
import mymath
class segment:
	def __init__(self,label,pos,RotMat,solids,color):
		self.label = label
		self.pos = pos
		self.RotMat = RotMat
		self.solids = solids
		self.nSolids = len(self.solids) 
		self.color = color
		
		# must set the position of constituent solids before being able to calculate relative/local properties.
		self.setOrientations()
		
		self.calcRelProperties()
		
	def setOrientations(self):
		'''Sets the position (self.pos) and rotation matrix (self.RotMat) for all solids in the segment by calling each constituent solid's setOrientation method. The position of the i-th solid, expressed in the fixed human reference frame, is given by the sum of the segment's base position and the directed height of all the solids of the segment up to the i-th solid.
		'''
		# pos and RotMat for first solid
		self.solids[0].setOrientation(self.pos,self.RotMat)
		
		# pos and RotMat for remaining solids
		for i in np.arange(self.nSolids):
			if i != 0:
				pos = self.solids[i-1].pos + self.solids[i-1].height * self.RotMat * mymath.zunit
				self.solids[i].setOrientation(pos,self.RotMat)
			
	def calcRelProperties(self):
		# mass
		self.Mass = 0.0
		for s in self.solids:
			self.Mass += s.Mass
		
		# relative position of each solid w.r.t. segment orientation and 
		# segment's origin
		self.solidpos = []
		self.solidpos.append( np.zeros( (3,1) ) )
		for i in np.arange(self.nSolids):
			if i != 0:
				self.solidpos.append( self.solidpos[i-1] + self.solids[i-1].height * mymath.zunit )

		# center of mass of each solid w.r.t. segment orientation and
		# segment's origin
		self.solidCOM = []	
		self.solidCOM.append( self.solids[0].relCOM )
		for i in np.arange(self.nSolids):
			if i != 0:
				self.solidCOM.append( self.solidpos[i] + self.solids[i].relCOM )

		# relative center of mass
		relmoment = np.zeros( (3,1) )
		for i in np.arange(self.nSolids):
			relmoment += self.solids[i].Mass * self.solidCOM[i]
		self.relCOM = relmoment / self.Mass
		
		# relative Inertia
		self.relInertia = np.mat(np.zeros( (3,3) ))
		for i in np.arange(self.nSolids):
			dist = self.solidCOM[i] - self.relCOM
			self.relInertia += np.mat(inertia.parallel_axis(self.solids[i].relInertia,self.solids[i].Mass,[dist[0,0],dist[1,0],dist[2,0]]))
			
	def calcProperties(self):

		# center of mass
		self.COM = self.pos + self.RotMat * self.relCOM

		# inertia in frame f w.r.t. segment's COM
		self.Inertia = mymath.RotateInertia(self.RotMat,self.relInertia)
		
		# inertia in frame f w.r.t. segment's COM
		self.Inertia2 = np.mat( np.zeros( (3,3) ) )
		for s in self.solids:
			dist = s.COM - self.COM
			self.Inertia2 += np.mat(inertia.parallel_axis(s.Inertia,s.Mass,[dist[0,0],dist[1,0],dist[2,0]]))

	def printProperties(self):
		'''Prints mass, center of mass (in local and fixed human frames), and inertia (in local and fixed human frames).
		'''
		print self.label,"properties:\n"
		print "Mass (kg):",self.Mass,"\n"
		print "COM in local segment frame (m):\n",self.relCOM,"\n"
		print "COM in fixed human frame (m):\n",self.COM,"\n"
		print "Inertia tensor in segment frame about local segment COM (kg-m^2):\n",self.relInertia,"\n"
		print "Inertia tensor in fixed human frame about local segment COM (kg-m^2):\n",self.Inertia,"\n"
		
	def printSolidProperties(self):
		'''Calls the printProperties() member method of each of this segment's solids. See the solid class's definition of printProperties(self) for more detail.
		'''
		for s in self.solids:
			s.printProperties()

	def draw(self,ax):
		'''Draws all the solids within a segment.'''
		for idx in np.arange(self.nSolids):
			print "Drawing solid",self.solids[idx].label,"."
			self.solids[idx].draw(ax, self.color)

		u = np.linspace( 0, 2*np.pi, 30)
		v = np.linspace( 0, np.pi, 30)

		R = 0.3
		x = R * np.outer(np.cos(u), np.sin(v)) + self.COM[0,0]
		y = R * np.outer(np.sin(u), np.sin(v)) + self.COM[1,0]
		z = R * np.outer(np.ones(np.size(u)), np.cos(v)) + self.COM[2,0]
		ax.plot_surface(x, y, z,  rstride=4, cstride=4, edgecolor ='', color='r')

