import numpy as np

# matplotlib
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D

# fresh code!
import solid as sol
import segment as seg
import measurements as meas
import densities as dens
import inertia # jason moore's
import mymath

class human:
	def __init__(self,meas,DOF):
		'''Initializes a human object. Stores inputs as instance variables, defines the names of the degrees of freedom (DOF) in a class tuple, defines the bounds on the DOFs in a class 2D list, validates the input DOFs against the DOF bounds, defines all the solids using the meas input parameter, defines all segments using the solid definitions, averages the segment inertia information (if the option is selected), calculates the inertia parameters (mass, center of mass, inertia tensor) of each solid and then of the entire human.

		Parameters
		----------
		meas : python module
		    Holds roughly 95 measurements (supposedly in meters) that allow the generation of stadium solids, circles, and ellipsoids with which to define the model's goemetry.
		DOF : dictionary with 21 entries
			The degrees of freedom of the human (radians).
		'''
		
		self.meas = meas
		self.isSymmetric = 1
		
		self.DOF = DOF
		
		human.DOFnames = ('somersalt', 'tilt', 'twist', 'PTsagittalFlexion', 'PTfrontalFlexion', 'TCspinalTorsion', 'TClateralSpinalFlexion', 'CA1elevation', 'CA1abduction', 'CA1rotation', 'CB1elevation', 'CB1abduction', 'CB1rotation', 'A1A2flexion', 'B1B2flexion', 'PJ1flexion', 'PJ1abduction', 'PK1flexion', 'PK1abduction', 'J1J2flexion', 'K1K2flexion')

		human.DOFbounds = [ [-np.pi, np.pi],
				           [-np.pi, np.pi],
				           [-np.pi, np.pi],
				           [-np.pi/2, np.pi],
				           [-np.pi/2, np.pi/2],
				           [-np.pi/2, np.pi/2],
				           [-np.pi/2, np.pi/2],
				           [-np.pi/2, np.pi*3/2],
				           [-np.pi*3/2, np.pi],
				           [-np.pi, np.pi],
				           [-np.pi/2, np.pi*3/2],
				           [-np.pi*3/2, np.pi],
				           [-np.pi, np.pi],
				           [0, np.pi],
				           [0, np.pi],
				           [-np.pi/2, np.pi],
				           [-np.pi/2, np.pi/2],
				           [-np.pi/2, np.pi],
				           [-np.pi/2, np.pi/2],
				           [0, np.pi],
				           [0, np.pi] ]
				       
		# check DOF input against DOF bounds
		self.validateDOFs()
		
		# define all solids.
		self.defineTorsoSolids()
		self.defineArmSolids()
		self.defineLegSolids()

		# define segments. this deals with coordinate transformations. and locates the bases of the segments.
		self.defineSegments()
		
		# arrange segment pointers into an indexable format
		self.Segments = [ self.P, self.T, self.C, self.A1, self.A2, self.B1, self.B2, self.J1, self.J2, self.K1, self.K2 ]
		
		# Yeadon wants to be able to create a symmetrical human.
		self.averageSegmentProperties()
		
		# calculate inertia properties of all segments.
		for s in self.Segments:
			s.calcProperties()

		# this next call must happen after the previous per-segment call because EDIT.
		self.calcProperties()
		
	def updateSegments(self):
		'''Updates all segments. Expected to be called by a GUI or commandline interface when a user has updated joint angles after the human object has been created. Solids do not need to be recreated, but the segments need to be redefined, and so inertia parameters need to be averaged again, and the human's inertia parameters must also be redefined.
		'''
		print "Updating segment properties."
		self.defineSegments()
		
		# must redefine this Segments list, the code does not work otherwise
		self.Segments = [ self.P, self.T, self.C, self.A1, self.A2, self.B1, self.B2, self.J1, self.J2, self.K1, self.K2 ]
		self.averageSegmentProperties()
		for s in self.Segments:
			s.calcProperties()
		self.calcProperties()

	def validateDOFs(self):
		'''Validates the joint angle degrees of freedom against the DOF bounds specified in the definition of the human object. Prints an error message if there is an issue. Hopefully this will implement sys.stderr eventually.
		
		Returns
		-------
		boolval : boolean
			0 if all DOFs are okay, -1 if there is an issue
		'''
		boolval = 0
		for i in np.arange(len(self.DOF)):
			if self.DOF[ human.DOFnames[i] ] < human.DOFbounds[i][0] or self.DOF[ human.DOFnames[i] ] > human.DOFbounds[i][1]:
				print "Joint angle",human.DOFnames[i],"=",self.DOF[human.DOFnames[i]]/np.pi,"pi-rad is out of range. Must be between",human.DOFbounds[i][0]/np.pi,"and",human.DOFbounds[i][1]/np.pi,"pi-rad"
				boolval = -1
		return boolval

	def averageSegmentProperties(self):
		''' Yeadon 1989-ii mentions that the model is to have symmetric inertia properties, especially for the sake of modelling the particular aerial movement that is the subject of the Yeadon-i-iv papers. This function sets the mass and relative/local inertia tensor of each limb (arms and legs) to be the average of the left and right limbs.
		'''
		if self.isSymmetric:
			upperarmMass = 0.5 * ( self.A1.Mass + self.B1.Mass )
			self.A1.Mass = upperarmMass
			self.B1.Mass = upperarmMass
			
			forearmhandMass = 0.5 * ( self.A2.Mass + self.B2.Mass )
			self.A2.Mass = forearmhandMass
			self.B2.Mass = forearmhandMass
			
			thighMass = 0.5 * ( self.J1.Mass + self.K1.Mass )
			self.J1.Mass = thighMass
			self.K1.Mass = thighMass
			
			shankfootMass = 0.5 * ( self.J2.Mass + self.K2.Mass )
			self.J2.Mass = shankfootMass
			self.K2.Mass = shankfootMass
			
			if 0:
				# it doesn't make sense to average these unless the leg orientations are coupled
				upperarmCOM = 0.5 * ( self.A1.COM + self.B1.COM )
				self.A1.COM = upperarmCOM
				self.B1.COM = upperarmCOM
			
				forearmhandCOM = 0.5 * ( self.A2.COM + self.B2.COM )
				self.A2.COM = forearmhandCOM
				self.B2.COM = forearmhandCOM
			
				thighCOM = 0.5 * ( self.J1.COM + self.K1.COM )
				self.J1.COM = thighCOM
				self.K1.COM = thighCOM
			
				shankfootCOM = 0.5 * ( self.J2.COM + self.K2.COM )
				self.J2.COM = shankfootCOM
				self.K2.COM = shankfootCOM
			
			# should we also mess with relative inertia?
			upperarmInertia = 0.5 * ( self.A1.relInertia + self.B1.relInertia )
			self.A1.relInertia = upperarmInertia
			self.B1.relInertia = upperarmInertia
			
			forearmhandInertia = 0.5 * ( self.A2.relInertia + self.B2.relInertia )
			self.A2.relInertia = forearmhandInertia
			self.B2.relInertia = forearmhandInertia
			
			thighInertia = 0.5 * ( self.J1.relInertia + self.K1.relInertia )
			self.J1.relInertia = thighInertia
			self.K1.relInertia = thighInertia
			
			shankfootInertia = 0.5 * ( self.J2.relInertia + self.K2.relInertia )
			self.J2.relInertia = shankfootInertia
			self.K2.relInertia = shankfootInertia
		
	def calcProperties(self):
		'''Calculates the mass, center of mass, and inertia tensor of the human. The quantities are calculated from the segment quantities. This method also calculates quantities in terms of the standard bicycle coordinate frame (x forward, z down).
		'''
		# mass
		self.Mass = 0.0;
		for s in self.Segments:
			self.Mass += s.Mass

		# center of mass
		moment = np.zeros( (3,1) )
		for s in self.Segments:
			moment += s.Mass * s.COM
		self.COM = moment / self.Mass

		self.Inertia = np.mat( np.zeros((3,3)) )
		for s in self.Segments:
			dist = s.COM - self.COM
			self.Inertia += np.mat( inertia.parallel_axis(s.Inertia, s.Mass, [dist[0,0],dist[1,0],dist[2,0]]) )

		self.bikerposCOM = mymath.Rotate3([0,np.pi,np.pi/2]) * self.COM
		dist = self.bikerposCOM - self.COM
		self.bikeposInertia = inertia.parallel_axis(mymath.Rotate3([0,np.pi,np.pi/2])* self.Inertia *mymath.Rotate3([0,np.pi,np.pi/2]).T,self.Mass,[dist[0,0],dist[1,0],dist[2,0]])
		
	def printProperties(self):
		'''Prints human mass, center of mass,and inertia.
		'''
		print "Mass (kg):", self.Mass, "\n"
		print "COM  (m):\n", self.COM, "\n"
		print "Inertia tensor about COM (kg-m^2):\n", self.Inertia, "\n"
		
	def draw(self):
		'''Draws a self by calling the draw methods of all of the segments. Drawing is done by the matplotlib library.'''
		print "Drawing the self."
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
		
		# fixed coordinate frame axes
		ax.plot( np.array([0,3]) , np.array([0,0]), np.array([0,0]), 'r', linewidth = 3)
		ax.plot( np.array([0,0]) , np.array([0,3]), np.array([0,0]), 'g', linewidth = 3)
		ax.plot( np.array([0,0]) , np.array([0,0]), np.array([0,3]), 'b', linewidth = 3)

		ax.text(3,0,0,'x')
		ax.text(0,3,0,'y')
		ax.text(0,0,3,'z')

		# plot center of mass ball
		N = 30
		u = np.linspace(0, 0.5*np.pi, 30)
		v = np.linspace(0, np.pi/2, 30)
		self.drawOctant(ax,u,v,'b')
		
		u = np.linspace(np.pi, 3/2*np.pi, 30)
		v = np.linspace(0, np.pi/2, 30)
		self.drawOctant(ax,u,v,'b')
		
		u = np.linspace(np.pi/2, np.pi, 30)
		v = np.linspace(np.pi/2, np.pi, 30)
		self.drawOctant(ax,u,v,'b')
		
		u = np.linspace( 3/2*np.pi, 2*np.pi, 30)
		v = np.linspace(np.pi/2, np.pi, 30)
		self.drawOctant(ax,u,v,'b')
		
		u = np.linspace(0.5*np.pi, np.pi, 30)
		v = np.linspace(0, np.pi/2, 30)
		self.drawOctant(ax,u,v,'w')
		
		u = np.linspace(3/2*np.pi, 2*np.pi, 30)
		v = np.linspace(0, np.pi/2, 30)
		self.drawOctant(ax,u,v,'w')
		
		u = np.linspace(0, np.pi/2, 30)
		v = np.linspace(np.pi/2, np.pi, 30)
		self.drawOctant(ax,u,v,'w')
		
		u = np.linspace( np.pi, 3/2*np.pi, 30)
		v = np.linspace(np.pi/2, np.pi, 30)
		self.drawOctant(ax,u,v,'w')
		
		# "axis equal"
		limval = 10
		ax.set_xlim3d(-limval, limval)
		ax.set_ylim3d(-limval, limval)
		ax.set_zlim3d(-limval, limval)
		
		# save the plot to an SVG file
		mpl.savefig('humanplot', dpi = 300)
		
		# show the plot window, this is a loop actually
		mpl.show()
		
	def drawOctant(self,ax,u,v,c):
		'''Draws an octant of sphere. Assists with drawing the center of mass sphere.
		
		Parameters
		----------
		ax : Axes3D object
			Axes on which to plot, defined by human.plot(self).
		u : numpy.array
		v : numpy.array
		c : string
			Color
		'''
		R = 0.5
		x = R * np.outer(np.cos(u), np.sin(v)) + self.COM[0,0]
		y = R * np.outer(np.sin(u), np.sin(v)) + self.COM[1,0]
		z = R * np.outer(np.ones(np.size(u)), np.cos(v)) + self.COM[2,0]
		ax.plot_surface(x, y, z,  rstride=4, cstride=4, edgecolor ='', color=c)
				
	def defineTorsoSolids(self):
		'''Defines the solids (from solid.py) that create the torso of the human. This requires the definition of 2-D stadium levels using the input measurement parameters (meas.).
		'''
	
		# torso	
		self.Ls = []
		self.s = []

		# Ls0: hip joint centre
		self.Ls.append( sol.stadium('perimwidth', meas.Ls0p, meas.Ls0w) ) 
		# Ls1: umbilicus
		self.Ls.append( sol.stadium('perimwidth', meas.Ls1p, meas.Ls1w) )
		# Ls2: lowest front rib
		self.Ls.append( sol.stadium('perimwidth', meas.Ls2p, meas.Ls2w) )
		# Ls3: nipple
		self.Ls.append( sol.stadium('perimwidth', meas.Ls3p, meas.Ls3w) )
		# Ls4: shoulder joint centre
		self.Ls.append( sol.stadium('perimwidth', meas.Ls4d, meas.Ls4w) )
		# Ls5: acromion
		self.Ls.append( sol.stadium('perimwidth', meas.Ls5p, meas.Ls5w) )
		# Ls6: beneath nose
		self.Ls.append( sol.stadium('perim', meas.Ls6p, '=p') )
		# Ls7: above ear
		self.Ls.append( sol.stadium('perim', meas.Ls7p, '=p') )
		# top of head # TEMP: MUST CHANGE TO SEMISPHERE
		self.Ls.append( sol.stadium('perim', meas.Ls7p, '=p') )
		
		# define solids: this can definitely be done in a loop
		# s0
		self.s.append( sol.stadiumsolid( 's0: hip joint centre',
		                                  dens.Ds[0],
		                                  self.Ls[0],
		                                  self.Ls[1],
		                                  meas.s0h) )
		# s1
		self.s.append( sol.stadiumsolid( 's1: umbilicus',
		                                  dens.Ds[1],
		                                  self.Ls[1],
		                                  self.Ls[2],
		                                  meas.s1h) )
		# s2
		self.s.append( sol.stadiumsolid( 's2: lowest front rib',
		                                  dens.Ds[2],
		                                  self.Ls[2],
		                                  self.Ls[3],
		                                  meas.s2h) )
		# s3
		self.s.append( sol.stadiumsolid( 's3: nipple',
		                                  dens.Ds[3],
		                                  self.Ls[3],
		                                  self.Ls[4],
		                                  meas.s3h) )
		# s4
		self.s.append( sol.stadiumsolid( 's4: shoulder joint centre',
		                                  dens.Ds[4],
		                                  self.Ls[4],
		                                  self.Ls[5],
		                                  meas.s4h) )
		# s5
		self.s.append( sol.stadiumsolid( 's5: acromion',
		                                  dens.Ds[5],
		                                  self.Ls[6],
		                                  self.Ls[6],
		                                  meas.s5h) )
		# s6
		self.s.append( sol.stadiumsolid( 's6: beneath nose',
		                                  dens.Ds[6],
		                                  self.Ls[6],
		                                  self.Ls[7],
		                                  meas.s6h) )
		# s7
		self.s.append( sol.semiellipsoid( 's7: above ear',
		                                   dens.Ds[7],
		                                   meas.Ls7p,
		                                   meas.s7h) )
			
	def defineArmSolids(self):
		'''Defines the solids (from solid.py) that create the arms of the human. This requires the definition of 2-D stadium levels using the input measurement parameters (meas.).
		'''
		
		# left arm
		self.La = []
		self.a = []
		# La0: shoulder joint centre
		self.La.append( sol.stadium('perim', meas.La0p, '=p') )
		# La1: mid-arm
		self.La.append( sol.stadium('perim', meas.La1p, '=p') )
		# La2: lowest front rib
		self.La.append( sol.stadium('perim', meas.La2p, '=p') )
		# La3: nipple
		self.La.append( sol.stadium('perim', meas.La3p, '=p') )
		# La4: wrist joint centre
		self.La.append( sol.stadium('perim', meas.La4p, '=p') )
		# La5: acromion
		self.La.append( sol.stadium('perimwidth', meas.La5p, meas.La5w) )
		# La6: knuckles
		self.La.append( sol.stadium('perimwidth', meas.La6p, meas.La6w) )
		# La7: fingernails
		self.La.append( sol.stadium('perimwidth', meas.La7p, meas.La7w) )
		
		# define left arm solids
		self.a.append( sol.stadiumsolid( 'a0: shoulder joint centre',
		                                  dens.Da[0],
		                                  self.La[0],
		                                  self.La[1],
		                                  meas.a0h) )
		self.a.append( sol.stadiumsolid( 'a1: mid-arm',
		                                  dens.Da[1],
		                                  self.La[1],
		                                  self.La[2],
		                                  meas.a1h) )
		self.a.append( sol.stadiumsolid( 'a2: elbow joint centre',
		                                  dens.Da[2],
		                                  self.La[2],
		                                  self.La[3],
		                                  meas.a2h) )
		self.a.append( sol.stadiumsolid( 'a3: maximum forearm perimeter',
		                                  dens.Da[3],
		                                  self.La[3],
		                                  self.La[4],
		                                  meas.a3h) )
		self.a.append( sol.stadiumsolid( 'a4: wrist joint centre',
		                                  dens.Da[4],
		                                  self.La[4],
		                                  self.La[5],
		                                  meas.a4h) )
		self.a.append( sol.stadiumsolid( 'a5: base of thumb',
		                                  dens.Da[5],
		                                  self.La[5],
		                                  self.La[6],
		                                  meas.a5h) )
		self.a.append( sol.stadiumsolid( 'a6: knuckles',
		                                  dens.Da[6],
		                                  self.La[6],
		                                  self.La[7],
		                                  meas.a6h) )
		                                  		
		# right arm
		self.Lb = []
		self.b = []
		
		# Lb0: shoulder joint centre
		self.Lb.append( sol.stadium('perim', meas.Lb0p, '=p') )
		# Lb1: mid-arm
		self.Lb.append( sol.stadium('perim', meas.Lb1p, '=p') )
		# Lb2: lowest front rib
		self.Lb.append( sol.stadium('perim', meas.Lb2p, '=p') )
		# Lb3: nipple
		self.Lb.append( sol.stadium('perim', meas.Lb3p, '=p') )
		# Lb4: wrist joint centre
		self.Lb.append( sol.stadium('perim', meas.Lb4p, '=p') )
		# Lb5: acromion
		self.Lb.append( sol.stadium('perimwidth', meas.Lb5p, meas.Lb5w) )
		# Lb6: knuckles
		self.Lb.append( sol.stadium('perimwidth', meas.Lb6p, meas.Lb6w) )
		# Lb7: fingernails
		self.Lb.append( sol.stadium('perimwidth', meas.Lb7p, meas.Lb7w) )
		
		# define right arm solids
		self.b.append( sol.stadiumsolid( 'b0: shoulder joint centre',
		                                  dens.Db[0],
		                                  self.Lb[0],
		                                  self.Lb[1],
		                                  meas.b0h) )
		self.b.append( sol.stadiumsolid( 'b1: mid-arm',
		                                  dens.Db[1],
		                                  self.Lb[1],
		                                  self.Lb[2],
		                                  meas.b1h) )
		self.b.append( sol.stadiumsolid( 'b2: elbow joint centre',
		                                  dens.Db[2],
		                                  self.Lb[2],
		                                  self.Lb[3],
		                                  meas.b2h) )
		self.b.append( sol.stadiumsolid( 'b3: maximum forearm perimeter',
		                                  dens.Db[3],
		                                  self.Lb[3],
		                                  self.Lb[4],
		                                  meas.b3h) )
		self.b.append( sol.stadiumsolid( 'b4: wrist joint centre',
		                                  dens.Db[4],
		                                  self.Lb[4],
		                                  self.Lb[5],
		                                  meas.b4h) )
		self.b.append( sol.stadiumsolid( 'b5: base of thumb',
		                                  dens.Db[5],
		                                  self.Lb[5],
		                                  self.Lb[6],
		                                  meas.b5h) )
		self.b.append( sol.stadiumsolid( 'b6: knuckles',
		                                  dens.Db[6],
		                                  self.Lb[6],
		                                  self.Lb[7],
		                                  meas.b6h) )

	def defineLegSolids(self):
		'''Defines the solids (from solid.py) that create the legs of the human. This requires the definition of 2-D stadium levels using the input measurement parameters (meas.).
		'''
		# left leg
		self.Lj = []
		self.j = []
		
		# Lj0: hip joint centre
		self.Lj.append( sol.stadium('perim', meas.Lj0p, '=p') )
		# Lj1: crotch
		self.Lj.append( sol.stadium('perim', meas.Lj1p, '=p') )
		# Lj2: mid-thigh
		self.Lj.append( sol.stadium('perim', meas.Lj2p, '=p') )
		# Lj3: knee joint centre
		self.Lj.append( sol.stadium('perim', meas.Lj3p, '=p') )
		# Lj4: maximum calf perimeter
		self.Lj.append( sol.stadium('perim', meas.Lj4p, '=p') )
		# Lj5: ankle joint centre
		self.Lj.append( sol.stadium('perim', meas.Lj5p, '=p') )
		# Lj6: heel, aligned anterior-posteriorly rather than medio-laterally
		self.Lj.append( sol.stadium('perimwidth', meas.Lj6p, meas.Lj6w, 'AP') )
		# Lj7: arch
		self.Lj.append( sol.stadium('perim', meas.Lj7p, '=p') )
		# Lj8: ball
		self.Lj.append( sol.stadium('perimwidth', meas.Lj8p, meas.Lj8w) )
		# Lj9: toe nails
		self.Lj.append( sol.stadium('perimwidth', meas.Lj9p, meas.Lj9w) )

		# define left leg solids		
		self.j.append( sol.stadiumsolid( 'j0: hip joint centre',
		                                  dens.Dj[0],
		                                  self.Lj[0],
		                                  self.Lj[1],
		                                  meas.j0h) )
		self.j.append( sol.stadiumsolid( 'j1: crotch',
		                                  dens.Dj[1],
		                                  self.Lj[1],
		                                  self.Lj[2],
		                                  meas.j1h) )
		self.j.append( sol.stadiumsolid( 'j2: mid-thigh',
		                                  dens.Dj[2],
		                                  self.Lj[2],
		                                  self.Lj[3],
		                                  meas.j2h) )
		self.j.append( sol.stadiumsolid( 'j3: knee joint centre',
		                                  dens.Dj[3],
		                                  self.Lj[3],
		                                  self.Lj[4],
		                                  meas.j3h) )
		self.j.append( sol.stadiumsolid( 'j4: maximum calf parimeter',
		                                  dens.Dj[4],
		                                  self.Lj[4],
		                                  self.Lj[5],
		                                  meas.j4h) )
		self.j.append( sol.stadiumsolid( 'j5: ankle joint centre',
		                                  dens.Dj[5],
		                                  self.Lj[5],
		                                  self.Lj[6],
		                                  meas.j5h) )
		self.j.append( sol.stadiumsolid( 'j6: heel',
		                                  dens.Dj[6],
		                                  self.Lj[6],
		                                  self.Lj[7],
		                                  meas.j6h) )
		self.j.append( sol.stadiumsolid( 'j7: arch',
		                                  dens.Dj[7],
		                                  self.Lj[7],
		                                  self.Lj[8],
		                                  meas.j7h) )
		self.j.append( sol.stadiumsolid( 'k8: ball',
		                                  dens.Dj[8],
		                                  self.Lj[8],
		                                  self.Lj[9],
		                                  meas.j8h) )       
		                                  
		# right leg
		self.Lk = []
		self.k = []
		
		# Lk0: hip joint centre
		self.Lk.append( sol.stadium('perim', meas.Lk0p, '=p') )
		# Lk1: crotch
		self.Lk.append( sol.stadium('perim', meas.Lk1p, '=p') )
		# Lk2: mid-thigh
		self.Lk.append( sol.stadium('perim', meas.Lk2p, '=p') )
		# Lk3: knee joint centre
		self.Lk.append( sol.stadium('perim', meas.Lk3p, '=p') )
		# Lk4: maximum calf perimeter
		self.Lk.append( sol.stadium('perim', meas.Lk4p, '=p') )
		# Lk5: ankle joint centre
		self.Lk.append( sol.stadium('perim', meas.Lk5p, '=p') )
		# Lk6: heel, aligned anterior-posteriorly rather than medio-laterally
		self.Lk.append( sol.stadium('perimwidth', meas.Lk6p, meas.Lk6w, 'AP') )
		# Lk7: arch
		self.Lk.append( sol.stadium('perim', meas.Lk7p, '=p') )
		# Lk8: ball
		self.Lk.append( sol.stadium('perimwidth', meas.Lk8p, meas.Lk8w) )
		# Lk9: toe nails
		self.Lk.append( sol.stadium('perimwidth', meas.Lk9p, meas.Lk9w) )
		
		self.k.append( sol.stadiumsolid( 'k0: hip joint centre',
		                                  dens.Dk[0],
		                                  self.Lk[0],
		                                  self.Lk[1],
		                                  meas.k0h) )
		self.k.append( sol.stadiumsolid( 'k1: crotch',
		                                  dens.Dk[1],
		                                  self.Lk[1],
		                                  self.Lk[2],
		                                  meas.k1h) )
		self.k.append( sol.stadiumsolid( 'k2: mid-thigh',
		                                  dens.Dk[2],
		                                  self.Lk[2],
		                                  self.Lk[3],
		                                  meas.k2h) )
		self.k.append( sol.stadiumsolid( 'k3: knee joint centre',
		                                  dens.Dk[3],
		                                  self.Lk[3],
		                                  self.Lk[4],
		                                  meas.k3h) )
		self.k.append( sol.stadiumsolid( 'k4: maximum calf perimeter',
		                                  dens.Dk[4],
		                                  self.Lk[4],
		                                  self.Lk[5],
		                                  meas.k4h) )
		self.k.append( sol.stadiumsolid( 'k5: ankle joint centre',
		                                  dens.Dk[5],
		                                  self.Lk[5],
		                                  self.Lk[6],
		                                  meas.k5h) )
		self.k.append( sol.stadiumsolid( 'k6: heel',
		                                  dens.Dk[6],
		                                  self.Lk[6],
		                                  self.Lk[7],
		                                  meas.k6h) )
		self.k.append( sol.stadiumsolid( 'k7: arch',
		                                  dens.Dk[7],
		                                  self.Lk[7],
		                                  self.Lk[8],
		                                  meas.k7h) )    
		self.k.append( sol.stadiumsolid( 'k8: ball',
		                                  dens.Dk[8],
		                                  self.Lk[8],
		                                  self.Lk[9],
		                                  meas.k8h) )       
		               
	def defineSegments(self):
		'''Define segment objects using previously defined solids. This is where the definition of segment position and rotation really happens. There are 9 segments. Each segment has a base, located at a joint, and an orientation given by the input joint angle parameters.
		'''
		# define all segments
		# pelvis
		Ppos = np.array([[0],[0],[0]])
		PRotMat = mymath.RotateRel([self.DOF['somersalt'],
		                            self.DOF['tilt'],
		                            self.DOF['twist']])
		self.P = seg.segment( 'P: Pelvis', Ppos, PRotMat,
		                      [self.s[0],self.s[1]] , 'red')

		# thorax
		Tpos = self.s[1].pos + self.s[1].height * self.s[1].RotMat * mymath.zunit
		TRotMat = self.s[1].RotMat * mymath.Rotate3([self.DOF['PTsagittalFlexion'],
		                                             self.DOF['PTfrontalFlexion'],0])
		self.T = seg.segment( 'T: Thorax', Tpos, TRotMat,
		                      [self.s[2]], 'orange')

		# chest-head
		Cpos = self.s[2].pos + self.s[2].height * self.s[2].RotMat * mymath.zunit
		CRotMat = self.s[2].RotMat * mymath.Rotate3([0, self.DOF['TClateralSpinalFlexion'], self.DOF['TCspinalTorsion']])
		self.C = seg.segment( 'C: Chest-head', Cpos, CRotMat,
		                      [self.s[3],self.s[4],self.s[5],self.s[6],self.s[7]], 'yellow')

		# left upper arm                                  
		dpos = np.array([[self.s[3].stads[1].width/2],[0.0],[self.s[3].height]])
		A1pos = self.s[3].pos + self.s[3].RotMat * dpos
		A1RotMat = self.s[3].RotMat * mymath.Rotate3([0,-np.pi,0]) * mymath.RotateRel([self.DOF['CA1elevation'],
                                  -self.DOF['CA1abduction'],
                                  -self.DOF['CA1rotation']])
		self.A1 = seg.segment( 'A1: Left upper arm', A1pos, A1RotMat,
		                       [self.a[0],self.a[1]] , 'green' )

		# left forearm-hand
		A2pos = self.a[1].pos + self.a[1].height * self.a[1].RotMat * mymath.zunit
		A2RotMat = self.a[1].RotMat * mymath.Rotate3([self.DOF['A1A2flexion'],0,0])
		self.A2 = seg.segment( 'A2: Left forearm-hand', A2pos, A2RotMat,
		                       [self.a[2],self.a[3],self.a[4],self.a[5],self.a[6]], 'red')
		# right upper arm
		dpos = np.array([[-self.s[3].stads[1].width/2],[0.0],[self.s[3].height]])
		B1pos = self.s[3].pos + self.s[3].RotMat * dpos
		B1RotMat = self.s[3].RotMat * mymath.Rotate3([0,-np.pi,0]) * mymath.RotateRel([self.DOF['CB1elevation'],
		                             self.DOF['CB1abduction'],
		                             self.DOF['CB1rotation']])
		self.B1 = seg.segment( 'B1: Right upper arm', B1pos, B1RotMat,
		                       [self.b[0],self.b[1]], 'green')

		# right forearm-hand
		B2pos = self.b[1].pos + self.b[1].height * self.b[1].RotMat * mymath.zunit
		B2RotMat = self.b[1].RotMat * mymath.Rotate3([self.DOF['B1B2flexion'],0,0])
		self.B2 = seg.segment( 'B2: Right forearm-hand', B2pos, B2RotMat,
		                       [self.b[2],self.b[3],self.b[4],self.b[5],self.b[6]], 'red')

		# left thigh                            
		dpos = np.array([[self.s[0].stads[0].thick],[0.0],[0.0]])
		J1pos = self.s[0].pos + self.s[0].RotMat * dpos
		J1RotMat = self.s[0].RotMat * mymath.Rotate3(np.array([0,np.pi,0])) * mymath.Rotate3([self.DOF['PJ1flexion'], 0,
		                          -self.DOF['PJ1abduction']])
		self.J1 = seg.segment( 'J1: Left thigh', J1pos, J1RotMat,
		                       [self.j[0],self.j[1],self.j[2]], 'green')

		# left shank-foot
		J2pos = self.j[2].pos + self.j[2].height * self.j[2].RotMat * mymath.zunit
		J2RotMat = self.j[2].RotMat * mymath.Rotate3([-self.DOF['J1J2flexion'],0,0])
		self.J2 = seg.segment( 'J2: Left shank-foot', J2pos, J2RotMat,
		                       [self.j[3],self.j[4],self.j[5],self.j[6],self.j[7],self.j[8]], 'red')

		# right thigh                            
		dpos = np.array([[-self.s[0].stads[0].thick],[0.0],[0.0]])
		K1pos = self.s[0].pos + self.s[0].RotMat * dpos
		K1RotMat = self.s[0].RotMat * mymath.Rotate3(np.array([0,np.pi,0])) * mymath.Rotate3([self.DOF['PK1flexion'], 0,
		                         self.DOF['PK1abduction']])
		self.K1 = seg.segment( 'K1: Right thigh', K1pos, K1RotMat,
		                       [self.k[0],self.k[1],self.k[2]], 'green')
		
		# right shank-foot
		K2pos = self.k[2].pos + self.k[2].height * self.k[2].RotMat * mymath.zunit
		K2RotMat = self.k[2].RotMat * mymath.Rotate3([-self.DOF['K1K2flexion'],0,0])
		self.K2 = seg.segment( 'K2: Right shank-foot', K2pos, K2RotMat,
		                       [self.k[3],self.k[4],self.k[5],self.k[6],self.k[7],self.k[8]], 'red')
