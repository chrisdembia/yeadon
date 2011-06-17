import numpy as np
import stadium as stad
import segment as seg
import data
import densities as dens

import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
import mymath



class human:
	def __init__(self,externalangles):

		# define all solids.
		self.externalangles = externalangles # np.array([0,0,0])
		
		self.Ls = []
		self.s = []

		# Ls0: hip joint centre
		self.Ls.append( stad.stadium('perimwidth', data.Ls0p, data.Ls0w) ) 

		# Ls1: umbilicus
		self.Ls.append( stad.stadium('perimwidth', data.Ls1p, data.Ls1w) )
		
		# Ls2: lowest front rib
		self.Ls.append( stad.stadium('perimwidth', data.Ls2p, data.Ls2w) )
				
		# Ls3: nipple
		self.Ls.append( stad.stadium('perimwidth', data.Ls3p, data.Ls3w) )

		# Ls4: shoulder joint centre
		self.Ls.append( stad.stadium('perimwidth', data.Ls4d, data.Ls4w) )

		# Ls5: acromion
		self.Ls.append( stad.stadium('perimwidth', data.Ls5p, data.Ls5w) )
		
		# Ls6: beneath nose
		self.Ls.append( stad.stadium('perim', data.Ls6p, '=p') )
		
		# Ls7: above ear
		self.Ls.append( stad.stadium('perim', data.Ls7p, '=p') )
		
		# top of head # TEMP: MUST CHANGE TO SEMISPHERE
		self.Ls.append( stad.stadium('perim', data.Ls7p, '=p') )

		# define solids: this can definitely be done in a loop
		# s0
		posS0,orientS0 = self.calcPlaceS0()
		self.s.append( stad.stadiumsolid( 's0',
		                                  dens.Ds[0],
		                                  posS0,
		                                  orientS0,
		                                  self.Ls[0],
		                                  self.Ls[1],
		                                  data.s0h) )
		# s1
		posS1,orientS1 = self.calcPlaceS1()
		self.s.append( stad.stadiumsolid( 's1',
		                                  dens.Ds[1],
		                                  posS1,
		                                  orientS1,
		                                  self.Ls[1],
		                                  self.Ls[2],
		                                  data.s1h) )
		                                  
		# s2
		posS2,orientS2 = self.calcPlaceS2()
		self.s.append( stad.stadiumsolid( 's2',
		                                  dens.Ds[2],
		                                  posS2,
		                                  orientS2,
		                                  self.Ls[2],
		                                  self.Ls[3],
		                                  data.s2h) )

		# s3
		posS3,orientS3 = self.calcPlaceS3()
		self.s.append( stad.stadiumsolid( 's3',
		                                  dens.Ds[3],
		                                  posS3,
		                                  orientS3,
		                                  self.Ls[3],
		                                  self.Ls[4],
		                                  data.s3h) )
		                                  
		# s4
		posS4,orientS4 = self.calcPlaceS4()
		self.s.append( stad.stadiumsolid( 's4',
		                                  dens.Ds[4],
		                                  posS4,
		                                  orientS4,
		                                  self.Ls[4],
		                                  self.Ls[5],
		                                  data.s4h) )
		                                  
		# s5
		posS5,orientS5 = self.calcPlaceS5()
		self.s.append( stad.stadiumsolid( 's5',
		                                  dens.Ds[5],
		                                  posS5,
		                                  orientS5,
		                                  self.Ls[6],
		                                  self.Ls[6],
		                                  data.s5h) )
		                                  
		# s6
		posS6,orientS6 = self.calcPlaceS6()
		self.s.append( stad.stadiumsolid( 's6',
		                                  dens.Ds[6],
		                                  posS6,
		                                  orientS6,
		                                  self.Ls[6],
		                                  self.Ls[7],
		                                  data.s6h) )

		# s7
		posS7,orientS7 = self.calcPlaceS7()
		self.s.append( stad.semiellipsoid( 's7',
		                                   dens.Ds[7],
		                                   posS7,
		                                   orientS7,
		                                   data.Ls7p,
		                                   data.s7h) )
		print "HIII0",data.s7h     
		# define all segments
		self.P = seg.segment( [self.s[0],self.s[1]] , 'r' )
		self.T = seg.segment( [self.s[2]], 'g' )
		self.C = seg.segment( [self.s[3],self.s[4],self.s[5],self.s[6],self.s[7]], 'b' )

	def calcInertias(self):
		absInertiaTensor = 0
		bikerposInertiaTensor = 0
		return absInertiaTensor, bikerposInertiaTensor

	def draw(self):
		'''Draws a human.'''
		print "Drawing the human."
#		self.reCalc
		# temp draw
		fig = mpl.figure()
		ax = Axes3D(fig)

		self.P.draw(ax)
		self.T.draw(ax)
		self.C.draw(ax)
		
		ax.plot( np.array([-1,1]) , np.array([0,0]), np.array([0,0]) )
		ax.plot( np.array([0,0]) , np.array([-1,1]), np.array([0,0]) )
		ax.plot( np.array([0,0]) , np.array([0,0]), np.array([-1,1]) )

		ax.text(1,0,0,'x')
		ax.text(0,1,0,'y')
		ax.text(0,0,1,'z')

		limval = 10
		ax.set_xlim3d(-limval, limval)
		ax.set_ylim3d(-limval, limval)
		ax.set_zlim3d(-limval, limval)				

		mpl.show()
			
	def calcPlaceS0(self):
		pos = np.array([[0],[0],[0]])
		orient = self.externalangles
		return pos,orient
	def calcPlaceS1(self):
		pos = self.s[0].pos + self.s[0].height * mymath.RotateExternal(self.s[0].orient) * mymath.zunit
		orient = self.s[0].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		return pos,orient
	def calcPlaceS2(self,TPangles):
		pos = self.s[1].pos + self.s[1].height * mymath.RotateExternal(self.s[1].orient) * mymath.zunit
		orient = self.s[1].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		return pos,orient
	def calcPlaceS3(self):
		pos = self.s[2].pos + self.s[2].height * mymath.RotateExternal(self.s[2].orient) * mymath.zunit
		orient = self.s[2].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		return pos,orient
	def calcPlaceS4(self):
		pos = self.s[3].pos + self.s[3].height * mymath.RotateExternal(self.s[3].orient) * mymath.zunit
		orient = self.s[3].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		return pos,orient
	def calcPlaceS5(self):
		pos = self.s[4].pos + self.s[4].height * mymath.RotateExternal(self.s[4].orient) * mymath.zunit
		orient = self.s[4].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		return pos,orient
	def calcPlaceS6(self):
		pos = self.s[5].pos + self.s[5].height * mymath.RotateExternal(self.s[5].orient) * mymath.zunit
		orient = self.s[5].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		return pos,orient
	def calcPlaceS7(self):
		pos = self.s[6].pos + self.s[6].height * mymath.RotateExternal(self.s[6].orient) * mymath.zunit
		orient = self.s[6].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		return pos,orient
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
