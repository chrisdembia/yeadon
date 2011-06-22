import numpy as np
import stadium as stad
import segment as seg
import data
import densities as dens

import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
import mymath



class human:
	def __init__(self,externalangles,PTangles,TCangles,CA1angles,CB1angles,A1A2angle,B1B2angle,PJ1angles,PK1angles,J1J2angle,K1K2angle):

		self.externalangles = externalangles # np.array([0,0,0])
		self.PTangles = PTangles
		self.TCangles = TCangles
		self.CA1angles = CA1angles
		self.CB1angles = CB1angles
		self.A1A2angle = A1A2angle
		self.B1B2angle = B1B2angle
		self.PJ1angles = PJ1angles
		self.PK1angles = PK1angles
		self.J1J2angle = J1J2angle
		self.K1K2angle = K1K2angle
				
		# define all solids.	
		
		self.defineTorso()
		self.defineArms()
		self.defineLegs()

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
		self.A1.draw(ax)
		self.A2.draw(ax)
		self.B1.draw(ax)
		self.B2.draw(ax)
		self.J1.draw(ax)
		self.J2.draw(ax)
		self.K1.draw(ax)
		self.K2.draw(ax)
		
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
		orient = self.externalangles
		pos = np.array([[0],[0],[0]])
		RotMat = mymath.RotateExternal(self.externalangles)
		return pos,orient,RotMat
	def calcPlaceS1(self):
		pos = self.s[0].pos + self.s[0].height * self.s[0].RotMat * mymath.zunit
		orient = self.s[0].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		RotMat = self.s[0].RotMat # mymath.RotateExternal(self.s[0].orient)
		return pos,orient,RotMat
	def calcPlaceS2(self):
		pos = self.s[1].pos + self.s[1].height * self.s[1].RotMat * mymath.zunit
		orient = self.s[1].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		RotMat = mymath.Rotate3([self.PTangles[0],self.PTangles[1],0]) * self.s[1].RotMat
		return pos,orient,RotMat
	def calcPlaceS3(self):
		pos = self.s[2].pos + self.s[2].height * self.s[2].RotMat * mymath.zunit
		orient = self.s[2].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		RotMat = mymath.Rotate3([0,self.TCangles[1],self.TCangles[0]]) * self.s[2].RotMat
		return pos,orient,RotMat
	def calcPlaceS4(self):
		pos = self.s[3].pos + self.s[3].height * self.s[3].RotMat * mymath.zunit
		orient = self.s[3].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		RotMat = self.s[3].RotMat
		return pos,orient,RotMat
	def calcPlaceS5(self):
		pos = self.s[4].pos + self.s[4].height * self.s[4].RotMat * mymath.zunit
		orient = self.s[4].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		RotMat = self.s[4].RotMat
		return pos,orient,RotMat
	def calcPlaceS6(self):
		pos = self.s[5].pos + self.s[5].height * self.s[5].RotMat * mymath.zunit
		orient = self.s[5].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		RotMat = self.s[5].RotMat
		return pos,orient,RotMat
	def calcPlaceS7(self):
		pos = self.s[6].pos + self.s[6].height * self.s[6].RotMat * mymath.zunit
		orient = self.s[6].orient # THIS ACTUALLY IS MORE COMPLICATED: JOINT ANGLES!
		RotMat = self.s[6].RotMat
		return pos,orient,RotMat
	
	def calcPlaceA0(self): 
		dpos = np.array([[self.s[3].stads[1].width/2],[0.0],[self.s[3].height]])
		pos = self.s[3].pos + self.s[3].RotMat * dpos
		orient = self.s[3].RotMat * mymath.zunit
		RotMat = mymath.RotateExternal(self.CA1angles) * mymath.Rotate3(np.array([0,-np.pi,0])) * self.s[3].RotMat # EDIT EDIT EDIT
		return pos,orient,RotMat
	def calcPlaceA1(self):
		pos = self.a[0].pos + self.a[0].height * self.a[0].RotMat * mymath.zunit
		orient = self.a[0].orient
		RotMat = self.a[0].RotMat
		return pos,orient,RotMat
	def calcPlaceA2(self):
		pos = self.a[1].pos + self.a[1].height * self.a[1].RotMat * mymath.zunit
		orient = self.a[1].orient
		RotMat = mymath.Rotate3([0,-self.A1A2angle,0]) * self.a[1].RotMat # EDIT EDIT EDIT
		return pos,orient,RotMat
	def calcPlaceA3(self):
		pos = self.a[2].pos + self.a[2].height * self.a[2].RotMat * mymath.zunit
		orient = self.a[2].orient
		RotMat = self.a[2].RotMat
		return pos,orient,RotMat
	def calcPlaceA4(self):
		pos = self.a[3].pos + self.a[3].height * self.a[3].RotMat * mymath.zunit
		orient = self.a[3].orient
		RotMat = self.a[3].RotMat
		return pos,orient,RotMat
	def calcPlaceA5(self):
		pos = self.a[4].pos + self.a[4].height * self.a[4].RotMat * mymath.zunit
		orient = self.a[4].orient
		RotMat = self.a[4].RotMat
		return pos,orient,RotMat
	def calcPlaceA6(self):
		pos = self.a[5].pos + self.a[5].height * self.a[5].RotMat * mymath.zunit
		orient = self.a[5].orient
		RotMat = self.a[5].RotMat
		return pos,orient,RotMat
	def calcPlaceA7(self):
		pos = self.a[6].pos + self.a[6].height * self.a[6].RotMat * mymath.zunit
		orient = self.a[6].orient
		RotMat = self.a[6].RotMat
		return pos,orient,RotMat
	def calcPlaceA8(self):
		pos = self.a[7].pos + self.a[7].height * self.a[7].RotMat * mymath.zunit
		orient = self.a[7].orient
		RotMat = self.a[7].RotMat
		return pos,orient,RotMat

	def calcPlaceB0(self):
		dpos = np.array([[-self.s[3].stads[1].width/2],[0.0],[self.s[3].height]])
		pos = self.s[3].pos + self.s[3].RotMat * dpos
		orient = self.s[3].RotMat * mymath.zunit
		RotMat = mymath.RotateExternal(self.CB1angles) * mymath.Rotate3(np.array([0,-np.pi,0])) * self.s[3].RotMat
		return pos,orient,RotMat
	def calcPlaceB1(self):
		pos = self.b[0].pos + self.b[0].height * self.b[0].RotMat * mymath.zunit
		orient = self.b[0].orient
		RotMat = self.b[0].RotMat
		return pos,orient,RotMat
	def calcPlaceB2(self):
		pos = self.b[1].pos + self.b[1].height * self.b[1].RotMat * mymath.zunit
		orient = self.b[1].orient
		RotMat = mymath.Rotate3([0,-self.B1B2angle,0]) * self.b[1].RotMat
		return pos,orient,RotMat
	def calcPlaceB3(self):
		pos = self.b[2].pos + self.b[2].height * self.b[2].RotMat * mymath.zunit
		orient = self.b[2].orient
		RotMat = self.b[2].RotMat
		return pos,orient,RotMat
	def calcPlaceB4(self):
		pos = self.b[3].pos + self.b[3].height * self.b[3].RotMat * mymath.zunit
		orient = self.b[3].orient
		RotMat = self.b[3].RotMat
		return pos,orient,RotMat
	def calcPlaceB5(self):
		pos = self.b[4].pos + self.b[4].height * self.b[4].RotMat * mymath.zunit
		orient = self.b[4].orient
		RotMat = self.b[4].RotMat
		return pos,orient,RotMat
	def calcPlaceB6(self):
		pos = self.b[5].pos + self.b[5].height * self.b[5].RotMat * mymath.zunit
		orient = self.b[5].orient
		RotMat = self.b[5].RotMat
		return pos,orient,RotMat
	def calcPlaceB7(self):
		pos = self.b[6].pos + self.b[6].height * self.b[6].RotMat * mymath.zunit
		orient = self.b[6].orient
		RotMat = self.b[6].RotMat
		return pos,orient,RotMat
	def calcPlaceB8(self):
		pos = self.b[7].pos + self.b[7].height * self.b[7].RotMat * mymath.zunit
		orient = self.b[7].orient
		RotMat = self.b[7].RotMat
		return pos,orient,RotMat

	def calcPlaceJ0(self):
		pos = self.s[0].pos + np.array([[self.s[0].stads[0].thick],[0.0],[0.0]])
		orient = self.s[0].orient
		RotMat = mymath.Rotate3([self.PJ1angles[0],self.PJ1angles[1],0]) * mymath.Rotate3(np.array([np.pi,0,0])) * self.s[0].RotMat   # EDIT EDIT EDIT
		return pos,orient,RotMat
	def calcPlaceJ1(self):
		pos = self.j[0].pos + self.j[0].height * self.j[0].RotMat * mymath.zunit
		orient = self.j[0].orient
		RotMat = self.j[0].RotMat
		return pos,orient,RotMat
	def calcPlaceJ2(self):
		pos = self.j[1].pos + self.j[1].height * self.j[1].RotMat * mymath.zunit
		orient = self.j[1].orient
		RotMat = self.j[1].RotMat
		return pos,orient,RotMat
	def calcPlaceJ3(self):
		pos = self.j[2].pos + self.j[2].height * self.j[2].RotMat * mymath.zunit
		orient = self.j[2].orient
		RotMat = mymath.Rotate3([-self.J1J2angle,0,0]) * self.j[2].RotMat # EDIT EDIT EDIT
		return pos,orient,RotMat
	def calcPlaceJ4(self):
		pos = self.j[3].pos + self.j[3].height * self.j[3].RotMat * mymath.zunit
		orient = self.j[3].orient
		RotMat = self.j[3].RotMat
		return pos,orient,RotMat
	def calcPlaceJ5(self):
		pos = self.j[4].pos + self.j[4].height * self.j[4].RotMat * mymath.zunit
		orient = self.j[4].orient
		RotMat = self.j[4].RotMat
		return pos,orient,RotMat
	def calcPlaceJ6(self):
		pos = self.j[5].pos + self.j[5].height * self.j[5].RotMat * mymath.zunit
		orient = self.j[5].orient
		RotMat = self.j[5].RotMat
		return pos,orient,RotMat
	def calcPlaceJ7(self):
		pos = self.j[6].pos + self.j[6].height * self.j[6].RotMat * mymath.zunit
		orient = self.j[6].orient
		RotMat = self.j[6].RotMat
		return pos,orient,RotMat
	def calcPlaceJ8(self):
		pos = self.j[7].pos + self.j[7].height * self.j[7].RotMat * mymath.zunit
		orient = self.j[7].orient
		RotMat = self.j[7].RotMat
		return pos,orient,RotMat
		
	def calcPlaceK0(self):
		pos = self.s[0].pos + np.array([[-self.s[0].stads[0].thick],[0.0],[0.0]])
		orient = self.s[0].orient
		RotMat = mymath.Rotate3([self.PK1angles[0],self.PK1angles[1],0]) * mymath.Rotate3(np.array([np.pi,0,0])) * self.s[0].RotMat
		return pos,orient,RotMat
	def calcPlaceK1(self):
		pos = self.k[0].pos + self.k[0].height * self.k[0].RotMat * mymath.zunit
		orient = self.k[0].orient
		RotMat = self.k[0].RotMat
		return pos,orient,RotMat
	def calcPlaceK2(self):
		pos = self.k[1].pos + self.k[1].height * self.k[1].RotMat * mymath.zunit
		orient = self.k[1].orient
		RotMat = self.k[1].RotMat
		return pos,orient,RotMat
	def calcPlaceK3(self):
		pos = self.k[2].pos + self.k[2].height * self.k[2].RotMat * mymath.zunit
		orient = self.k[2].orient
		RotMat = mymath.Rotate3([-self.K1K2angle,0,0]) * self.k[2].RotMat # EDIT EDIT EDIT # EDIT EDIT EDIT
		return pos,orient,RotMat
	def calcPlaceK4(self):
		pos = self.k[3].pos + self.k[3].height * self.k[3].RotMat * mymath.zunit
		orient = self.k[3].orient
		RotMat = self.k[3].RotMat
		return pos,orient,RotMat
	def calcPlaceK5(self):
		pos = self.k[4].pos + self.k[4].height * self.k[4].RotMat * mymath.zunit
		orient = self.k[4].orient
		RotMat = self.k[4].RotMat
		return pos,orient,RotMat
	def calcPlaceK6(self):
		pos = self.k[5].pos + self.k[5].height * self.k[5].RotMat * mymath.zunit
		orient = self.k[5].orient
		RotMat = self.k[5].RotMat
		return pos,orient,RotMat
	def calcPlaceK7(self):
		pos = self.k[6].pos + self.k[6].height * self.k[6].RotMat * mymath.zunit
		orient = self.k[6].orient
		RotMat = self.k[6].RotMat
		return pos,orient,RotMat
	def calcPlaceK8(self):
		pos = self.k[7].pos + self.k[7].height * self.k[7].RotMat * mymath.zunit
		orient = self.k[7].orient
		RotMat = self.k[7].RotMat
		return pos,orient,RotMat
		
	def defineTorso(self):
	
		# torso	
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
		posS0,orientS0,RotMatS0 = self.calcPlaceS0()
		self.s.append( stad.stadiumsolid( 's0',
		                                  dens.Ds[0],
		                                  posS0,
		                                  orientS0,
		                                  RotMatS0,
		                                  self.Ls[0],
		                                  self.Ls[1],
		                                  data.s0h) )
		# s1
		posS1,orientS1,RotMatS1 = self.calcPlaceS1()
		self.s.append( stad.stadiumsolid( 's1',
		                                  dens.Ds[1],
		                                  posS1,
		                                  orientS1,
		                                  RotMatS1,
		                                  self.Ls[1],
		                                  self.Ls[2],
		                                  data.s1h) )
		                                  
		# s2
		posS2,orientS2,RotMatS2 = self.calcPlaceS2()
		self.s.append( stad.stadiumsolid( 's2',
		                                  dens.Ds[2],
		                                  posS2,
		                                  orientS2,
		                                  RotMatS2,
		                                  self.Ls[2],
		                                  self.Ls[3],
		                                  data.s2h) )

		# s3
		posS3,orientS3,RotMatS3 = self.calcPlaceS3()
		self.s.append( stad.stadiumsolid( 's3',
		                                  dens.Ds[3],
		                                  posS3,
		                                  orientS3,
		                                  RotMatS3,
		                                  self.Ls[3],
		                                  self.Ls[4],
		                                  data.s3h) )
		                                  
		# s4
		posS4,orientS4,RotMatS4 = self.calcPlaceS4()
		self.s.append( stad.stadiumsolid( 's4',
		                                  dens.Ds[4],
		                                  posS4,
		                                  orientS4,
		                                  RotMatS4,
		                                  self.Ls[4],
		                                  self.Ls[5],
		                                  data.s4h) )
		                                  
		# s5
		posS5,orientS5,RotMatS5 = self.calcPlaceS5()
		self.s.append( stad.stadiumsolid( 's5',
		                                  dens.Ds[5],
		                                  posS5,
		                                  orientS5,
		                                  RotMatS5,
		                                  self.Ls[6],
		                                  self.Ls[6],
		                                  data.s5h) )
		                                  
		# s6
		posS6,orientS6,RotMatS6 = self.calcPlaceS6()
		self.s.append( stad.stadiumsolid( 's6',
		                                  dens.Ds[6],
		                                  posS6,
		                                  orientS6,
		                                  RotMatS6,
		                                  self.Ls[6],
		                                  self.Ls[7],
		                                  data.s6h) )

		# s7
		posS7,orientS7,RotMatS7 = self.calcPlaceS7()
		self.s.append( stad.semiellipsoid( 's7',
		                                   dens.Ds[7],
		                                   posS7,
		                                   orientS7,
		                                   RotMatS7,
		                                   data.Ls7p,
		                                   data.s7h) )

		# define all segments
		# pelvis
		self.P = seg.segment( [self.s[0],self.s[1]] , 'r' )
		# thorax
		self.T = seg.segment( [self.s[2]], 'g' )
		# chest-head
		self.C = seg.segment( [self.s[3],self.s[4],self.s[5],self.s[6],self.s[7]], 'b' )

	def defineArms(self):

		# left arm
		self.La = []
		self.a = []
		# La0: shoulder joint centre
		self.La.append( stad.stadium('perim', data.La0p, '=p') )
		
		# La1: mid-arm
		self.La.append( stad.stadium('perim', data.La1p, '=p') )
		
		# La2: lowest front rib
		self.La.append( stad.stadium('perim', data.La2p, '=p') )
		
		# La3: nipple
		self.La.append( stad.stadium('perim', data.La3p, '=p') )
		
		# La4: wrist joint centre
		self.La.append( stad.stadium('perim', data.La4p, '=p') )
		
		# La5: acromion
		self.La.append( stad.stadium('perimwidth', data.La5p, data.La5w) )
		
		# La6: knuckles
		self.La.append( stad.stadium('perimwidth', data.La6p, data.La6w) )
		
		# La7: fingernails
		self.La.append( stad.stadium('perimwidth', data.La7p, data.La7w) )
		
		# define left arm solids
		posA0,orientA0,RotMatA0 = self.calcPlaceA0()
		self.a.append( stad.stadiumsolid( 'a0',
		                                  dens.Da[0],
		                                  posA0,
		                                  orientA0,
		                                  RotMatA0,
		                                  self.La[0],
		                                  self.La[1],
		                                  data.a0h) )
		                                  
		posA1,orientA1,RotMatA1 = self.calcPlaceA1()
		self.a.append( stad.stadiumsolid( 'a1',
		                                  dens.Da[1],
		                                  posA1,
		                                  orientA1,
		                                  RotMatA1,
		                                  self.La[1],
		                                  self.La[2],
		                                  data.a1h) )
		                                  
		posA2,orientA2,RotMatA2 = self.calcPlaceA2()
		self.a.append( stad.stadiumsolid( 'a2',
		                                  dens.Da[2],
		                                  posA2,
		                                  orientA2,
		                                  RotMatA2,
		                                  self.La[2],
		                                  self.La[3],
		                                  data.a2h) )
		                                  
		posA3,orientA3,RotMatA3 = self.calcPlaceA3()
		self.a.append( stad.stadiumsolid( 'a3',
		                                  dens.Da[3],
		                                  posA3,
		                                  orientA3,
		                                  RotMatA3,
		                                  self.La[3],
		                                  self.La[4],
		                                  data.a3h) )

		posA4,orientA4,RotMatA4 = self.calcPlaceA4()
		self.a.append( stad.stadiumsolid( 'a4',
		                                  dens.Da[4],
		                                  posA4,
		                                  orientA4,
		                                  RotMatA4,
		                                  self.La[4],
		                                  self.La[5],
		                                  data.a4h) )
		                                  
		posA5,orientA5,RotMatA5 = self.calcPlaceA5()
		self.a.append( stad.stadiumsolid( 'a5',
		                                  dens.Da[5],
		                                  posA5,
		                                  orientA5,
		                                  RotMatA5,
		                                  self.La[5],
		                                  self.La[6],
		                                  data.a5h) )
		                                  
		posA6,orientA6,RotMatA6 = self.calcPlaceA6()
		self.a.append( stad.stadiumsolid( 'a6',
		                                  dens.Da[6],
		                                  posA6,
		                                  orientA6,
		                                  RotMatA6,
		                                  self.La[6],
		                                  self.La[7],
		                                  data.a6h) )
		                                  
		# right arm
		self.Lb = []
		self.b = []
		
		# Lb0: shoulder joint centre
		self.Lb.append( stad.stadium('perim', data.Lb0p, '=p') )
		
		# Lb1: mid-arm
		self.Lb.append( stad.stadium('perim', data.Lb1p, '=p') )
		
		# Lb2: lowest front rib
		self.Lb.append( stad.stadium('perim', data.Lb2p, '=p') )
		
		# Lb3: nipple
		self.Lb.append( stad.stadium('perim', data.Lb3p, '=p') )
		
		# Lb4: wrist joint centre
		self.Lb.append( stad.stadium('perim', data.Lb4p, '=p') )
		
		# Lb5: acromion
		self.Lb.append( stad.stadium('perimwidth', data.Lb5p, data.Lb5w) )
		
		# Lb6: knuckles
		self.Lb.append( stad.stadium('perimwidth', data.Lb6p, data.Lb6w) )
		
		# Lb7: fingernails
		self.Lb.append( stad.stadium('perimwidth', data.Lb7p, data.Lb7w) )
		
		# define right arm solids
		posB0,orientB0,RotMatB0 = self.calcPlaceB0()
		self.b.append( stad.stadiumsolid( 'b0',
		                                  dens.Db[0],
		                                  posB0,
		                                  orientB0,
		                                  RotMatB0,
		                                  self.Lb[0],
		                                  self.Lb[1],
		                                  data.b0h) )
		                                  
		posB1,orientB1,RotMatB1 = self.calcPlaceB1()
		self.b.append( stad.stadiumsolid( 'b1',
		                                  dens.Db[1],
		                                  posB1,
		                                  orientB1,
		                                  RotMatB1,
		                                  self.Lb[1],
		                                  self.Lb[2],
		                                  data.b1h) )
		                                  
		posB2,orientB2,RotMatB2 = self.calcPlaceB2()
		self.b.append( stad.stadiumsolid( 'b2',
		                                  dens.Db[2],
		                                  posB2,
		                                  orientB2,
		                                  RotMatB2,
		                                  self.Lb[2],
		                                  self.Lb[3],
		                                  data.b2h) )
		                                  
		posB3,orientB3,RotMatB3 = self.calcPlaceB3()
		self.b.append( stad.stadiumsolid( 'b3',
		                                  dens.Db[3],
		                                  posB3,
		                                  orientB3,
		                                  RotMatB3,
		                                  self.Lb[3],
		                                  self.Lb[4],
		                                  data.b3h) )

		posB4,orientB4,RotMatB4 = self.calcPlaceB4()
		self.b.append( stad.stadiumsolid( 'b4',
		                                  dens.Db[4],
		                                  posB4,
		                                  orientB4,
		                                  RotMatB4,
		                                  self.Lb[4],
		                                  self.Lb[5],
		                                  data.b4h) )
		                                  
		posB5,orientB5,RotMatB5 = self.calcPlaceB5()
		self.b.append( stad.stadiumsolid( 'b5',
		                                  dens.Db[5],
		                                  posB5,
		                                  orientB5,
		                                  RotMatB5,
		                                  self.Lb[5],
		                                  self.Lb[6],
		                                  data.b5h) )
		                                  
		posB6,orientB6,RotMatB6 = self.calcPlaceB6()
		self.b.append( stad.stadiumsolid( 'b6',
		                                  dens.Db[6],
		                                  posB6,
		                                  orientB6,
		                                  RotMatB6,
		                                  self.Lb[6],
		                                  self.Lb[7],
		                                  data.b6h) )
		# left upper arm                                  
		self.A1 = seg.segment( [self.a[0],self.a[1]] , 'r' )
		# left forearm-hand
		self.A2 = seg.segment( [self.a[2],self.a[3],self.a[4],self.a[5],self.a[6]] , 'b' )
		# right upper arm
		self.B1 = seg.segment( [self.b[0],self.b[1]] , 'r' )
		# right forearm-hand
		self.B2 = seg.segment( [self.b[2],self.b[3],self.b[4],self.b[5],self.b[6]] , 'b' )
		
	def defineLegs(self):
		
		# left leg
		self.Lj = []
		self.j = []
		
		# Lj0: hip joint centre
		self.Lj.append( stad.stadium('perim', data.Lj0p, '=p') )
		
		# Lj1: crotch
		self.Lj.append( stad.stadium('perim', data.Lj1p, '=p') )
		
		# Lj2: mid-thigh
		self.Lj.append( stad.stadium('perim', data.Lj2p, '=p') )
		
		# Lj3: knee joint centre
		self.Lj.append( stad.stadium('perim', data.Lj3p, '=p') )
		
		# Lj4: maximum calf perimeter
		self.Lj.append( stad.stadium('perim', data.Lj4p, '=p') )
		
		# Lj5: ankle joint centre
		self.Lj.append( stad.stadium('perim', data.Lj5p, '=p') )
		
		# Lj6: heel # MUST FLAG: ROTATED THE OTHER WAYYIIIII
		self.Lj.append( stad.stadium('perimwidth', data.Lj6p, data.Lj6w) )
		
		# Lj7: arch
		self.Lj.append( stad.stadium('perim', data.Lj7p, '=p') )
		
		# Lj8: ball
		self.Lj.append( stad.stadium('perimwidth', data.Lj8p, data.Lj8w) )
		
		# Lj9: toe nails
		self.Lj.append( stad.stadium('perimwidth', data.Lj9p, data.Lj9w) )

		# define left leg solids		
		posJ0,orientJ0,RotMatJ0 = self.calcPlaceJ0()
		self.j.append( stad.stadiumsolid( 'j0',
		                                  dens.Dj[0],
		                                  posJ0,
		                                  orientJ0,
		                                  RotMatJ0,
		                                  self.Lj[0],
		                                  self.Lj[1],
		                                  data.j0h) )
		                                  
		posJ1,orientJ1,RotMatJ1 = self.calcPlaceJ1()
		self.j.append( stad.stadiumsolid( 'j1',
		                                  dens.Dj[1],
		                                  posJ1,
		                                  orientJ1,
		                                  RotMatJ1,
		                                  self.Lj[1],
		                                  self.Lj[2],
		                                  data.j1h) )
		
		posJ2,orientJ2,RotMatJ2 = self.calcPlaceJ2()
		self.j.append( stad.stadiumsolid( 'j2',
		                                  dens.Dj[2],
		                                  posJ2,
		                                  orientJ2,
		                                  RotMatJ2,
		                                  self.Lj[2],
		                                  self.Lj[3],
		                                  data.j2h) )
		                                  
		posJ3,orientJ3,RotMatJ3 = self.calcPlaceJ3()
		self.j.append( stad.stadiumsolid( 'j3',
		                                  dens.Dj[3],
		                                  posJ3,
		                                  orientJ3,
		                                  RotMatJ3,
		                                  self.Lj[3],
		                                  self.Lj[4],
		                                  data.j3h) )
		                                  
		posJ4,orientJ4,RotMatJ4 = self.calcPlaceJ4()
		self.j.append( stad.stadiumsolid( 'j4',
		                                  dens.Dj[4],
		                                  posJ4,
		                                  orientJ4,
		                                  RotMatJ4,
		                                  self.Lj[4],
		                                  self.Lj[5],
		                                  data.j4h) )
		                                  
		posJ5,orientJ5,RotMatJ5 = self.calcPlaceJ5()
		self.j.append( stad.stadiumsolid( 'j5',
		                                  dens.Dj[5],
		                                  posJ5,
		                                  orientJ5,
		                                  RotMatJ5,
		                                  self.Lj[5],
		                                  self.Lj[6],
		                                  data.j5h) )
		                                  
		posJ6,orientJ6,RotMatJ6 = self.calcPlaceJ6()
		self.j.append( stad.stadiumsolid( 'j6',
		                                  dens.Dj[6],
		                                  posJ6,
		                                  orientJ6,
		                                  RotMatJ6,
		                                  self.Lj[6],
		                                  self.Lj[7],
		                                  data.j6h) )
		                                  
		posJ7,orientJ7,RotMatJ7 = self.calcPlaceJ7()
		self.j.append( stad.stadiumsolid( 'j7',
		                                  dens.Dj[7],
		                                  posJ7,
		                                  orientJ7,
		                                  RotMatJ7,
		                                  self.Lj[7],
		                                  self.Lj[8],
		                                  data.j7h) )
		                                  
		posJ8,orientJ8,RotMatJ8 = self.calcPlaceJ8()
		self.j.append( stad.stadiumsolid( 'k8',
		                                  dens.Dj[8],
		                                  posJ8,
		                                  orientJ8,
		                                  RotMatJ8,
		                                  self.Lj[8],
		                                  self.Lj[9],
		                                  data.j8h) )       
		                                  
		# right leg
		self.Lk = []
		self.k = []
		
		# Lk0: hip joint centre
		self.Lk.append( stad.stadium('perim', data.Lk0p, '=p') )
		
		# Lk1: crotch
		self.Lk.append( stad.stadium('perim', data.Lk1p, '=p') )
		
		# Lk2: mid-thigh
		self.Lk.append( stad.stadium('perim', data.Lk2p, '=p') )
		
		# Lk3: knee joint centre
		self.Lk.append( stad.stadium('perim', data.Lk3p, '=p') )
		
		# Lk4: maximum calf perimeter
		self.Lk.append( stad.stadium('perim', data.Lk4p, '=p') )
		
		# Lk5: ankle joint centre
		self.Lk.append( stad.stadium('perim', data.Lk5p, '=p') )
		
		# Lk6: heel # MUST FLAG: ROTATED THE OTHER WAYYIIIII
		self.Lk.append( stad.stadium('perimwidth', data.Lk6p, data.Lk6w) )
		
		# Lk7: arch
		self.Lk.append( stad.stadium('perim', data.Lk7p, '=p') )
		
		# Lk8: ball
		self.Lk.append( stad.stadium('perimwidth', data.Lk8p, data.Lk8w) )
		
		# Lk9: toe nails
		self.Lk.append( stad.stadium('perimwidth', data.Lk9p, data.Lk9w) )
		
		posK0,orientK0,RotMatK0 = self.calcPlaceK0()
		self.k.append( stad.stadiumsolid( 'k0',
		                                  dens.Dk[0],
		                                  posK0,
		                                  orientK0,
		                                  RotMatK0,
		                                  self.Lk[0],
		                                  self.Lk[1],
		                                  data.k0h) )
		                                  
		posK1,orientK1,RotMatK1 = self.calcPlaceK1()
		self.k.append( stad.stadiumsolid( 'k1',
		                                  dens.Dk[1],
		                                  posK1,
		                                  orientK1,
		                                  RotMatK1,
		                                  self.Lk[1],
		                                  self.Lk[2],
		                                  data.k1h) )
		
		posK2,orientK2,RotMatK2 = self.calcPlaceK2()
		self.k.append( stad.stadiumsolid( 'k2',
		                                  dens.Dk[2],
		                                  posK2,
		                                  orientK2,
		                                  RotMatK2,
		                                  self.Lk[2],
		                                  self.Lk[3],
		                                  data.k2h) )
		                                  
		posK3,orientK3,RotMatK3 = self.calcPlaceK3()
		self.k.append( stad.stadiumsolid( 'k3',
		                                  dens.Dk[3],
		                                  posK3,
		                                  orientK3,
		                                  RotMatK3,
		                                  self.Lk[3],
		                                  self.Lk[4],
		                                  data.k3h) )
		                                  
		posK4,orientK4,RotMatK4 = self.calcPlaceK4()
		self.k.append( stad.stadiumsolid( 'k4',
		                                  dens.Dk[4],
		                                  posK4,
		                                  orientK4,
		                                  RotMatK4,
		                                  self.Lk[4],
		                                  self.Lk[5],
		                                  data.k4h) )
		                                  
		posK5,orientK5,RotMatK5 = self.calcPlaceK5()
		self.k.append( stad.stadiumsolid( 'k5',
		                                  dens.Dk[5],
		                                  posK5,
		                                  orientK5,
		                                  RotMatK5,
		                                  self.Lk[5],
		                                  self.Lk[6],
		                                  data.k5h) )
		                                  
		posK6,orientK6,RotMatK6 = self.calcPlaceK6()
		self.k.append( stad.stadiumsolid( 'k6',
		                                  dens.Dk[6],
		                                  posK6,
		                                  orientK6,
		                                  RotMatK6,
		                                  self.Lk[6],
		                                  self.Lk[7],
		                                  data.k6h) )
		                                  
		posK7,orientK7,RotMatK7 = self.calcPlaceK7()
		self.k.append( stad.stadiumsolid( 'k7',
		                                  dens.Dk[7],
		                                  posK7,
		                                  orientK7,
		                                  RotMatK7,
		                                  self.Lk[7],
		                                  self.Lk[8],
		                                  data.k7h) )    
		                                  
		posK8,orientK8,RotMatK8 = self.calcPlaceK8()
		self.k.append( stad.stadiumsolid( 'k8',
		                                  dens.Dk[8],
		                                  posK8,
		                                  orientK8,
		                                  RotMatK8,
		                                  self.Lk[8],
		                                  self.Lk[9],
		                                  data.k8h) )       

		# left thigh                            
		self.J1 = seg.segment( [self.j[0],self.j[1],self.j[2]] , 'r' )
		# left shank-foot
		self.J2 = seg.segment( [self.j[3],self.j[4],self.j[5],self.j[6],self.j[7],self.j[8]] , 'b' )

		# right thigh                            
		self.K1 = seg.segment( [self.k[0],self.k[1],self.k[2]] , 'r' )
		# right shank-foot
		self.K2 = seg.segment( [self.k[3],self.k[4],self.k[5],self.k[6],self.k[7],self.k[8]] , 'b' )                 
		                                  
		                                  
		                                  
		                                  
		                                  
		                                  
		                                  
		                                  
		                                  
		                                  
		                                  
		                                  
		                                  
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
