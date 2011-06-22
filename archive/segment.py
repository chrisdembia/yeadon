import stadium
import numpy as np

class segment:
	def __init__(self,solids,color):
		self.solids = solids
		print self.solids
		self.nSolids = len(self.solids) 
		self.color = color
		print self.nSolids# ? python syntax

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
