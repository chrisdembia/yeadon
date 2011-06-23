import stadium
import numpy as np
import inertia

class segment:
	def __init__(self,label,solids,color):
		self.label = label
		self.solids = solids
		self.nSolids = len(self.solids) 
		self.color = color
		self.RotMat = 5
		
		self.calcProperties()
		
	def calcProperties(self):
		self.Mass = 0.0
		for s in self.solids:
			self.Mass += s.Mass
		#print "Mass for segment",self.label, "is", self.Mass
		
		relmoment = np.zeros( (3,1) )

		for i in np.arange(self.nSolids):
			relCOM = 0
			for j in np.arange(i):
				relCOM += self.solids[j].relCOM
			
			relmoment += self.solids[i].Mass * relCOM
		self.relCOM = relmoment / self.Mass

		moment = np.zeros( (3,1) )
		for s in self.solids:
			moment += s.Mass * s.COM
		self.COM = moment / self.Mass
		
		#dist = 
		#self.relInertia = np.matrix( (3,3) )
		#for  need all local positions

		self.Inertia = np.mat( np.zeros( (3,3) ) )
		for s in self.solids:
			dist = s.COM - self.COM
			self.Inertia += np.mat(inertia.parallel_axis(s.Inertia,s.Mass,[dist[0,0],dist[1,0],dist[2,0]]))
		
	def printInertias(self):
	    print "Inertias for segment", self.label, ":"
	    for s in self.solids:
	    	print s.localI

	def draw(self,ax):
		for idx in np.arange(self.nSolids):
			self.solids[idx].draw(ax, self.color)

		
# orientation

#if 0:
#	class stadiumsegment(segment):
#		def __init__(stadiums):
#			self.stadiums = stadiums
#	class mixedsegment(segment):
#		def __init__(self):
		
#sublclasses for C, T, P, A1, A2, etc?

# include density
