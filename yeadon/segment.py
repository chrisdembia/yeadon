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
		
		self.setOrientations()
		
		self.calcRelProperties()
		
		self.calcProperties()
		
	def setOrientations(self):
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
		print self.label
		self.relInertia = np.mat(np.zeros( (3,3) ))
		for i in np.arange(self.nSolids):
			dist = self.solidCOM[i] - self.relCOM
			self.relInertia += np.mat(inertia.parallel_axis(self.solids[i].relInertia,self.solids[i].Mass,[dist[0,0],dist[1,0],dist[2,0]]))

		print self.relInertia
			
	def calcProperties(self):
	
		# center of mass
		self.COM = self.pos + self.RotMat * self.relCOM

		# inertia in frame f w.r.t. segment's COM
		self.Inertia = mymath.RotateInertia(self.RotMat,self.relInertia)
		print self.Inertia
		
		# inertia in frame f w.r.t. segment's COM
		self.Inertia2 = np.mat( np.zeros( (3,3) ) )
		for s in self.solids:
			dist = s.COM - self.COM
			self.Inertia2 += np.mat(inertia.parallel_axis(s.Inertia,s.Mass,[dist[0,0],dist[1,0],dist[2,0]]))
		print self.Inertia2


	def draw(self,ax):
		'''Draws all the solids within a segment.'''
		for idx in np.arange(self.nSolids):
			self.solids[idx].draw(ax, self.color)

		u = np.linspace( 0, 2*np.pi, 30)
		v = np.linspace( 0, np.pi, 30)

		R = 0.5
		x = R * np.outer(np.cos(u), np.sin(v)) + self.COM[0,0]
		y = R * np.outer(np.sin(u), np.sin(v)) + self.COM[1,0]
		z = R * np.outer(np.ones(np.size(u)), np.cos(v)) + self.COM[2,0]
		ax.plot_surface(x, y, z,  rstride=4, cstride=4, edgecolor ='', color='r')

# orientation

#if 0:
#	class stadiumsegment(segment):
#		def __init__(stadiums):
#			self.stadiums = stadiums
#	class mixedsegment(segment):
#		def __init__(self):
		
#sublclasses for C, T, P, A1, A2, etc?

# include density
