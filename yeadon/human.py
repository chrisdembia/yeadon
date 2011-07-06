'''The human module defines the human class, which is composed of segments.
   The human class has methods to define the constituent segments from inputs
   and to calculate their properties.
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import inertia # jason moore's

import solid as sol
import segment as seg
import densities as dens
import mymath

class human:
    def __init__(self,meas_in,CFG):
        '''Initializes a human object. Stores inputs as instance variables,
           defines the names of the configuration variables (CFG) in a class
           tuple, defines the bounds on the configuration variables in a class
           2D list, validates the input CFG against the CFG bounds, defines all
           the solids using the meas input parameter, defines all segments
           using the solid definitions, averages the segment inertia
           information (if the option is selected), calculates the inertia
           parameters (mass, center of mass, inertia tensor) of each solid 
           and then of the entire human.

        Parameters
        ----------
        meas : python module
            Holds roughly 95 measurements (supposedly in meters) that allow the generation of stadium solids, circles, and ellipsoids with which to define the model's goemetry.
        CFG : dictionary with 21 entries
            The configuration of the human (radians).

       
        '''
        self.isSymmetric = 1
        human.measnames = ('Ls1L','Ls2L','Ls3L','Ls4L','Ls5L','Ls6L','Ls7L',
                           'Ls8L','Ls0p','Ls1p','Ls2p','Ls3p','Ls5p','Ls6p',
                           'Ls7p','Ls0w','Ls1w','Ls2w','Ls3w','Ls4w','Ls4d',                               'La2L','La3L','La4L','La5L','La6L','La7L','La0p',
                           'La1p','La2p','La3p','La4p','La5p','La6p','La7p',
                           'La4w','La5w','La6w','La7w',
                           'Lb2L','Lb3L','Lb4L','Lb5L','Lb6L','Lb7L','Lb0p',
                           'Lb1p','Lb2p','Lb3p','Lb4p','Lb5p','Lb6p','Lb7p',
                           'Lb4w','Lb5w','Lb6w','Lb7w',
                           'Lj1L','Lj3L','Lj4L','Lj5L','Lj6L','Lj8L','Lj9L',
                           'Lj1p','Lj2p','Lj3p','Lj4p','Lj5p','Lj6p','Lj7p',
                           'Lj8p','Lj9p','Lj8w','Lj9w','Lj6d', 
                           'Lk1L','Lk3L','Lk4L','Lk5L','Lk6L','Lk8L','Lk9L',
                           'Lk1p','Lk2p','Lk3p','Lk4p','Lk5p','Lk6p','Lk7p',
                           'Lk8p','Lk9p','Lk8w','Lk9w','Lk6d')
        human.CFGnames = ('somersalt', 'tilt', 'twist',
                          'PTsagittalFlexion', 'PTfrontalFlexion',
                          'TCspinalTorsion', 'TClateralSpinalFlexion',
                          'CA1elevation', 'CA1abduction', 'CA1rotation',
                          'CB1elevation', 'CB1abduction', 'CB1rotation',
                          'A1A2flexion', 'B1B2flexion', 'PJ1flexion',
                          'PJ1abduction', 'PK1flexion', 'PK1abduction',
                          'J1J2flexion', 'K1K2flexion')
        human.CFGbounds = [ [-np.pi, np.pi],
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
                            [0, np.pi]]
        # if measurements input is a module, just assign. else, read in file
        if type(meas_in) == dict:
            self.meas = meas_in
        elif type(meas_in) == str:
            self.read_measurements(meas_in)
        # if configuration input is a dictionary, just assign. else, read in
        if type(CFG) == dict:
            self.CFG = CFG
        elif type(CFG) == str:
            self.read_CFG(CFG)
        # check CFG input against CFG bounds
        self.validate_CFG()
        # define all solids.
        self.define_torso_solids()
        self.define_arm_solids()
        self.define_leg_solids()
        # define segments. this deals with coordinate transformations. and locates the bases of the segments.
        self.define_segments()
        # arrange segment pointers into an indexable format
        self.Segments = [ self.P, self.T, self.C,
                          self.A1, self.A2, self.B1, self.B2,
                          self.J1, self.J2, self.K1, self.K2]
        # Yeadon wants to be able to create a symmetrical human.
        self.average_segment_properties()
        # calculate inertia properties of all segments.
        for s in self.Segments:
            s.calc_properties()
        # this next call must happen after the previous 
        # per-segment call because EDIT.
        self.calc_properties()
       
 
    def update_segments(self):
        '''Updates all segments. Expected to be called by a GUI or commandline interface when a user has updated joint angles after the human object has been created. Solids do not need to be recreated, but the segments need to be redefined, and so inertia parameters need to be averaged again, and the human's inertia parameters must also be redefined.
        
        '''
        print "Updating segment properties."
        self.validateCFG()
        self.define_segments()
        # must redefine this Segments list, 
        # the code does not work otherwise
        self.Segments = [ self.P, self.T, self.C,
                          self.A1, self.A2, self.B1, self.B2,
                          self.J1, self.J2, self.K1, self.K2]
        self.average_segment_properties()
        for s in self.Segments:
            s.calc_properties()
        self.calc_properties()

    def validate_CFG(self):
        '''Validates the joint angle degrees of freedom against the CFG bounds specified in the definition of the human object. Prints an error message if there is an issue. Hopefully this will implement sys.stderr eventually.
        
        Returns
        -------
        boolval : boolean
            0 if all configuration variables are okay, -1 if there is an issue
        
        '''
        boolval = 0
        for i in np.arange(len(self.CFG)):
            if (self.CFG[human.CFGnames[i]] < human.CFGbounds[i][0] or 
                self.CFG[human.CFGnames[i]] > human.CFGbounds[i][1]):
                print "Joint angle",human.CFGnames[i],"=",\
                      self.CFG[human.CFGnames[i]]/np.pi,\
                      "pi-rad is out of range. Must be between",\
                      human.CFGbounds[i][0]/np.pi,"and",\
                      human.CFGbounds[i][1]/np.pi,"pi-rad"
                boolval = -1
        return boolval

    def average_segment_properties(self):
        ''' Yeadon 1989-ii mentions that the model is to have symmetric inertia properties, especially for the sake of modelling the particular aerial movement that is the subject of the Yeadon-i-iv papers. This function sets the mass and relative/local inertia tensor of each limb (arms and legs) to be the average of the left and right limbs.
        
        '''
        if self.isSymmetric:
            upperarmMass = 0.5 * (self.A1.Mass + self.B1.Mass)
            self.A1.Mass = upperarmMass
            self.B1.Mass = upperarmMass
            forearmhandMass = 0.5 * (self.A2.Mass + self.B2.Mass)
            self.A2.Mass = forearmhandMass
            self.B2.Mass = forearmhandMass
            thighMass = 0.5 * (self.J1.Mass + self.K1.Mass)
            self.J1.Mass = thighMass
            self.K1.Mass = thighMass
            shankfootMass = 0.5 * (self.J2.Mass + self.K2.Mass)
            self.J2.Mass = shankfootMass
            self.K2.Mass = shankfootMass
            if 0:
                # it doesn't make sense to average these
                # unless the leg orientations are coupled.
                upperarmCOM = 0.5 * (self.A1.COM + self.B1.COM)
                self.A1.COM = upperarmCOM
                self.B1.COM = upperarmCOM
                forearmhandCOM = 0.5 * (self.A2.COM + self.B2.COM)
                self.A2.COM = forearmhandCOM
                self.B2.COM = forearmhandCOM
                thighCOM = 0.5 * (self.J1.COM + self.K1.COM)
                self.J1.COM = thighCOM
                self.K1.COM = thighCOM
                shankfootCOM = 0.5 * (self.J2.COM + self.K2.COM)
                self.J2.COM = shankfootCOM
                self.K2.COM = shankfootCOM
            
            # it only makes sense to change relative inertia.
            upperarmInertia = 0.5 * (self.A1.relInertia +
                                     self.B1.relInertia)
            self.A1.relInertia = upperarmInertia
            self.B1.relInertia = upperarmInertia
            forearmhandInertia = 0.5 * (self.A2.relInertia +
                                        self.B2.relInertia)
            self.A2.relInertia = forearmhandInertia
            self.B2.relInertia = forearmhandInertia
            thighInertia = 0.5 * (self.J1.relInertia +
                                  self.K1.relInertia)
            self.J1.relInertia = thighInertia
            self.K1.relInertia = thighInertia
            shankfootInertia = 0.5 * (self.J2.relInertia +
                                      self.K2.relInertia)
            self.J2.relInertia = shankfootInertia
            self.K2.relInertia = shankfootInertia
       
    def set_CFG(self,idx,value):
        '''Allows the user to set a single configuration variable in CFG without
           using the command line interface. CFG is a dictionary that holds all
           21 configuration variables. Then, this function validates and
           updates the human model with the proper configuration variables.

           Parameters
           ----------
           idx : int or str
               Index into configuration variable dictionary CFG. If int, must
               be between 0 and 21. If str, must be a valid name of a 
               configuration variable.
           value : float
               New value for the configuration variable identified by idx.
               This value will be validated for joint angle limits.

        '''
        if type(idx)==int:
            CFG[CFGnames[idx]] = value
        elif type(idx)==str:
            CFG[idx] = value
        else:
            print "set_CFG(idx,value): first argument must be an integer" \
                  " between 0 and 21, or a valid string index for the" \
                  " CFG dictionary."
        self.update_segments() 

    def calc_properties(self):
        '''Calculates the mass, center of mass, and inertia tensor of the human. The quantities are calculated from the segment quantities. This method also calculates quantities in terms of the standard bicycle coordinate frame (x forward, z down).

        '''
        # mass
        self.Mass = 0.0;
        for s in self.Segments:
            self.Mass += s.Mass
        # center of mass
        moment = np.zeros((3,1))
        for s in self.Segments:
            moment += s.Mass * s.COM
        self.COM = moment / self.Mass
        # inertia
        self.Inertia = np.mat(np.zeros((3,3)))
        for s in self.Segments:
            dist = s.COM - self.COM
            self.Inertia += np.mat(
                inertia.parallel_axis(s.Inertia,
                                      s.Mass,
                                      [dist[0,0],dist[1,0],dist[2,0]]))
        # center of mass in biker coordinate system
        self.bikerposCOM = mymath.Rotate3([0,np.pi,np.pi/2]) * self.COM
        dist = self.bikerposCOM - self.COM
        self.bikeposInertia = inertia.parallel_axis(
            mymath.Rotate3([0,np.pi,np.pi/2]) *
                self.Inertia * mymath.Rotate3([0,np.pi,np.pi/2]).T,
            self.Mass,
            [dist[0,0],dist[1,0],dist[2,0]])
        
    def print_properties(self):
        '''Prints human mass, center of mass,and inertia.

        '''
        print "Mass (kg):", self.Mass, "\n"
        print "COM  (m):\n", self.COM, "\n"
        print "Inertia tensor about COM (kg-m^2):\n", self.Inertia, "\n"
        
    def draw2D(self):
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(121, aspect='equal')
        ax4 = fig2.add_subplot(122, aspect='equal')
        for seg in self.Segments:
            seg.draw2D(ax2,ax4)
        plt.show()

    def draw(self):
        '''Draws a self by calling the draw methods of all of the segments. Drawing is done by the matplotlib library.

        '''
        print "Drawing the self."
        fig = plt.figure()
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
        ax.plot( np.array([0,.3]),
                 np.array([0,0]),
                 np.array([0,0]), 'r', linewidth=3)
        ax.plot( np.array([0,0]),
                 np.array([0,.3]),
                 np.array([0,0]), 'g', linewidth=3)
        ax.plot( np.array([0,0]),
                 np.array([0,0]),
                 np.array([0,.3]), 'b', linewidth=3)
        ax.text(.3,0,0,'x')
        ax.text(0,.3,0,'y')
        ax.text(0,0,.3,'z')
        # plot center of mass ball
        N = 30
        u = np.linspace(0, 0.5 * np.pi, 30)
        v = np.linspace(0, np.pi/2, 30)
        self.draw_octant(ax,u,v,'b')
        u = np.linspace(np.pi, 3/2 * np.pi, 30)
        v = np.linspace(0, np.pi / 2, 30)
        self.draw_octant(ax,u,v,'b')
        u = np.linspace(np.pi / 2, np.pi, 30)
        v = np.linspace(np.pi / 2, np.pi, 30)
        self.draw_octant(ax,u,v,'b')
        u = np.linspace( 3/2 * np.pi, 2 * np.pi, 30)
        v = np.linspace(np.pi / 2, np.pi, 30)
        self.draw_octant(ax,u,v,'b')
        u = np.linspace(0.5 * np.pi, np.pi, 30)
        v = np.linspace(0, np.pi / 2, 30)
        self.draw_octant(ax,u,v,'w')
        u = np.linspace(3/2 * np.pi, 2 * np.pi, 30)
        v = np.linspace(0, np.pi / 2, 30)
        self.draw_octant(ax,u,v,'w')
        u = np.linspace(0, np.pi / 2, 30)
        v = np.linspace(np.pi / 2, np.pi, 30)
        self.draw_octant(ax,u,v,'w')
        u = np.linspace( np.pi, 3/2 * np.pi, 30)
        v = np.linspace(np.pi / 2, np.pi, 30)
        self.draw_octant(ax,u,v,'w')
        # "axis equal"
        limval = 1
        ax.set_xlim3d(-limval, limval)
        ax.set_ylim3d(-limval, limval)
        ax.set_zlim3d(-limval, limval)
        # save the plot to an SVG file
        plt.savefig('humanplot', dpi=300)
        # show the plot window, this is a loop actually
        plt.show()
        
    def draw_octant(self,ax,u,v,c):
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
        R = 0.05
        x = R * np.outer(np.cos(u), np.sin(v)) + self.COM[0,0]
        y = R * np.outer(np.sin(u), np.sin(v)) + self.COM[1,0]
        z = R * np.outer(np.ones(np.size(u)), np.cos(v)) + self.COM[2,0]
        ax.plot_surface( x, y, z,  rstride=4, cstride=4,
                         edgecolor='', color=c)
                
    def define_torso_solids(self):
        '''Defines the solids (from solid.py) that create the torso of the human. This requires the definition of 2-D stadium levels using the input measurement parameters.

        '''
  
        meas = self.meas 
        # get solid heights from length measurements
        s0h = meas['Ls1L']
        s1h = meas['Ls2L'] - s0h
        s2h = meas['Ls3L'] - s1h
        s3h = meas['Ls4L'] - s2h
        s4h = meas['Ls5L'] - s3h
        s5h = meas['Ls6L']
        s6h = meas['Ls7L'] - s5h
        s7h = meas['Ls8L'] - s6h
        # torso    
        self.Ls = []
        self.s = []
        # Ls0: hip joint centre
        self.Ls.append( sol.stadium('perimwidth', meas['Ls0p'], meas['Ls0w'])) 
        # Ls1: umbilicus
        self.Ls.append( sol.stadium('perimwidth', meas['Ls1p'], meas['Ls1w']))
        # Ls2: lowest front rib
        self.Ls.append( sol.stadium('perimwidth', meas['Ls2p'], meas['Ls2w']))
        # Ls3: nipple
        self.Ls.append( sol.stadium('perimwidth', meas['Ls3p'], meas['Ls3w']))
        # Ls4: shoulder joint centre (note depthwidth this time)
        self.Ls.append( sol.stadium('depthwidth', meas['Ls4d'], meas['Ls4w']))
        # Ls5: acromion EDIT!!
        thick = self.Ls[4].width / 2.0 - 0.57 * self.Ls[4].radius
        radius = meas['Ls5p'] / 2.0 / np.pi
        self.Ls.append( sol.stadium('thickradius', thick, radius))
        # Ls5: acromion/bottom of neck
        self.Ls.append( sol.stadium('perim',meas['Ls5p'], '=p'))
        # Ls6: beneath nose
        self.Ls.append( sol.stadium('perim', meas['Ls6p'], '=p'))
        # Ls7: above ear
        self.Ls.append( sol.stadium('perim', meas['Ls7p'], '=p'))
        # define solids: this can definitely be done in a loop
        # s0
        self.s.append( sol.stadiumsolid( 's0: hip joint centre',
                                          dens.Ds[0],
                                          self.Ls[0],
                                          self.Ls[1],
                                          s0h))
        # s1
        self.s.append( sol.stadiumsolid( 's1: umbilicus',
                                          dens.Ds[1],
                                          self.Ls[1],
                                          self.Ls[2],
                                          s1h))
        # s2
        self.s.append( sol.stadiumsolid( 's2: lowest front rib',
                                          dens.Ds[2],
                                          self.Ls[2],
                                          self.Ls[3],
                                          s2h))
        # s3
        self.s.append( sol.stadiumsolid( 's3: nipple',
                                          dens.Ds[3],
                                          self.Ls[3],
                                          self.Ls[4],
                                          s3h))
        # s4
        self.s.append( sol.stadiumsolid( 's4: shoulder joint centre',
                                          dens.Ds[4],
                                          self.Ls[4],
                                          self.Ls[5],
                                          s4h))
        # s5
        self.s.append( sol.stadiumsolid( 's5: acromion',
                                          dens.Ds[5],
                                          self.Ls[6],
                                          self.Ls[7],
                                          s5h))
        # s6
        self.s.append( sol.stadiumsolid( 's6: beneath nose',
                                          dens.Ds[6],
                                          self.Ls[7],
                                          self.Ls[8],
                                          s6h))
        # s7
        self.s.append( sol.semiellipsoid( 's7: above ear',
                                           dens.Ds[7],
                                           meas['Ls7p'],
                                           s7h))
            
    def define_arm_solids(self):
        '''Defines the solids (from solid.py) that create the arms of the human. This requires the definition of 2-D stadium levels using the input measurement parameters .

        '''
        meas = self.meas 
        # get solid heights from length measurements
        a0h = meas['La2L'] * 0.5
        a1h = meas['La2L'] - a0h
        a2h = meas['La3L'] - a1h
        a3h = meas['La4L'] - a2h
        a4h = meas['La5L']
        a5h = meas['La6L'] - a4h
        a6h = meas['La7L'] - a5h
        # left arm
        self.La = []
        self.a = []
        # La0: shoulder joint centre
        self.La.append( sol.stadium('perim', meas['La0p'], '=p'))
        # La1: mid-arm
        self.La.append( sol.stadium('perim', meas['La1p'], '=p'))
        # La2: lowest front rib
        self.La.append( sol.stadium('perim', meas['La2p'], '=p'))
        # La3: nipple
        self.La.append( sol.stadium('perim', meas['La3p'], '=p'))
        # La4: wrist joint centre
        self.La.append( sol.stadium('perimwidth', meas['La4p'], meas['La4w']))
        # La5: acromion
        self.La.append( sol.stadium('perimwidth', meas['La5p'], meas['La5w']))
        # La6: knuckles
        self.La.append( sol.stadium('perimwidth', meas['La6p'], meas['La6w']))
        # La7: fingernails
        self.La.append( sol.stadium('perimwidth', meas['La7p'], meas['La7w']))
        # define left arm solids
        self.a.append( sol.stadiumsolid( 'a0: shoulder joint centre',
                                          dens.Da[0],
                                          self.La[0],
                                          self.La[1],
                                          a0h))
        self.a.append( sol.stadiumsolid( 'a1: mid-arm',
                                          dens.Da[1],
                                          self.La[1],
                                          self.La[2],
                                          a1h))
        self.a.append( sol.stadiumsolid( 'a2: elbow joint centre',
                                          dens.Da[2],
                                          self.La[2],
                                          self.La[3],
                                          a2h))
        self.a.append( sol.stadiumsolid( 'a3: maximum forearm perimeter',
                                          dens.Da[3],
                                          self.La[3],
                                          self.La[4],
                                          a3h))
        self.a.append( sol.stadiumsolid( 'a4: wrist joint centre',
                                          dens.Da[4],
                                          self.La[4],
                                          self.La[5],
                                          a4h))
        self.a.append( sol.stadiumsolid( 'a5: base of thumb',
                                          dens.Da[5],
                                          self.La[5],
                                          self.La[6],
                                          a5h))
        self.a.append( sol.stadiumsolid( 'a6: knuckles',
                                          dens.Da[6],
                                          self.La[6],
                                          self.La[7],
                                          a6h))
        # get solid heights from length measurements
        b0h = meas['Lb2L'] * 0.5
        b1h = meas['Lb2L'] - b0h
        b2h = meas['Lb3L'] - b1h
        b3h = meas['Lb4L'] - b2h
        b4h = meas['Lb5L']
        b5h = meas['Lb6L'] - b4h
        b6h = meas['Lb7L'] - b5h
        # right arm
        self.Lb = []
        self.b = []
        # Lb0: shoulder joint centre
        self.Lb.append( sol.stadium('perim', meas['Lb0p'], '=p'))
        # Lb1: mid-arm
        self.Lb.append( sol.stadium('perim', meas['Lb1p'], '=p'))
        # Lb2: lowest front rib
        self.Lb.append( sol.stadium('perim', meas['Lb2p'], '=p'))
        # Lb3: nipple
        self.Lb.append( sol.stadium('perim', meas['Lb3p'], '=p'))
        # Lb4: wrist joint centre
        self.Lb.append( sol.stadium('perimwidth', meas['Lb4p'], meas['Lb4w']))
        # Lb5: acromion
        self.Lb.append( sol.stadium('perimwidth', meas['Lb5p'], meas['Lb5w']))
        # Lb6: knuckles
        self.Lb.append( sol.stadium('perimwidth', meas['Lb6p'], meas['Lb6w']))
        # Lb7: fingernails
        self.Lb.append( sol.stadium('perimwidth', meas['Lb7p'], meas['Lb7w']))
        # define right arm solids
        self.b.append( sol.stadiumsolid( 'b0: shoulder joint centre',
                                          dens.Db[0],
                                          self.Lb[0],
                                          self.Lb[1],
                                          b0h))
        self.b.append( sol.stadiumsolid( 'b1: mid-arm',
                                          dens.Db[1],
                                          self.Lb[1],
                                          self.Lb[2],
                                          b1h))
        self.b.append( sol.stadiumsolid( 'b2: elbow joint centre',
                                          dens.Db[2],
                                          self.Lb[2],
                                          self.Lb[3],
                                          b2h))
        self.b.append( sol.stadiumsolid( 'b3: maximum forearm perimeter',
                                          dens.Db[3],
                                          self.Lb[3],
                                          self.Lb[4],
                                          b3h))
        self.b.append( sol.stadiumsolid( 'b4: wrist joint centre',
                                          dens.Db[4],
                                          self.Lb[4],
                                          self.Lb[5],
                                          b4h))
        self.b.append( sol.stadiumsolid( 'b5: base of thumb',
                                          dens.Db[5],
                                          self.Lb[5],
                                          self.Lb[6],
                                          b5h))
        self.b.append( sol.stadiumsolid( 'b6: knuckles',
                                          dens.Db[6],
                                          self.Lb[6],
                                          self.Lb[7],
                                          b6h))

    def define_leg_solids(self):
        '''Defines the solids (from solid.py) that create the legs of the human. This requires the definition of 2-D stadium levels using the input measurement parameters .

        '''
        meas = self.meas 
        # get solid heights from length measurements
        j0h = meas['Lj1L']
        j1h = (meas['Lj3L'] + meas['Lj1L']) * 0.5 - j0h
        j2h = meas['Lj3L'] - j1h
        j3h = meas['Lj4L'] - j2h
        j4h = meas['Lj5L'] - j3h
        j5h = meas['Lj6L']
        j6h = (meas['Lj8L'] + meas['Lj6L']) * 0.5 - j5h
        j7h = meas['Lj8L'] - j6h
        j8h = meas['Lj9L'] - j7h
        # left leg
        self.Lj = []
        self.j = []
        # Lj0: hip joint centre
        Lj0p = 2 * np.pi * 0.5 * np.sqrt(np.abs(self.Ls[0].radius *
                                                self.Ls[0].width))
        self.Lj.append( sol.stadium('perim', Lj0p, '=p'))
        # Lj1: crotch
        self.Lj.append( sol.stadium('perim', meas['Lj1p'], '=p'))
        # Lj2: mid-thigh
        self.Lj.append( sol.stadium('perim', meas['Lj2p'], '=p'))
        # Lj3: knee joint centre
        self.Lj.append( sol.stadium('perim', meas['Lj3p'], '=p'))
        # Lj4: maximum calf perimeter
        self.Lj.append( sol.stadium('perim', meas['Lj4p'], '=p'))
        # Lj5: ankle joint centre
        self.Lj.append( sol.stadium('perim', meas['Lj5p'], '=p'))
        # Lj6: heel, aligned anterior-posteriorly
        # rather than medio-laterally
        self.Lj.append( sol.stadium('perimwidth', meas['Lj6p'], meas['Lj6d'],
                                    'AP'))
        # Lj7: arch
        self.Lj.append( sol.stadium('perim', meas['Lj7p'], '=p'))
        # Lj8: ball
        self.Lj.append( sol.stadium('perimwidth', meas['Lj8p'], meas['Lj8w']))
        # Lj9: toe nails
        self.Lj.append( sol.stadium('perimwidth', meas['Lj9p'], meas['Lj9w']))

        # define left leg solids        
        self.j.append( sol.stadiumsolid( 'j0: hip joint centre',
                                          dens.Dj[0],
                                          self.Lj[0],
                                          self.Lj[1],
                                          j0h))
        self.j.append( sol.stadiumsolid( 'j1: crotch',
                                          dens.Dj[1],
                                          self.Lj[1],
                                          self.Lj[2],
                                          j1h))
        self.j.append( sol.stadiumsolid( 'j2: mid-thigh',
                                          dens.Dj[2],
                                          self.Lj[2],
                                          self.Lj[3],
                                          j2h))
        self.j.append( sol.stadiumsolid( 'j3: knee joint centre',
                                          dens.Dj[3],
                                          self.Lj[3],
                                          self.Lj[4],
                                          j3h))
        self.j.append( sol.stadiumsolid( 'j4: maximum calf parimeter',
                                          dens.Dj[4],
                                          self.Lj[4],
                                          self.Lj[5],
                                          j4h))
        self.j.append( sol.stadiumsolid( 'j5: ankle joint centre',
                                          dens.Dj[5],
                                          self.Lj[5],
                                          self.Lj[6],
                                          j5h))
        self.j.append( sol.stadiumsolid( 'j6: heel',
                                          dens.Dj[6],
                                          self.Lj[6],
                                          self.Lj[7],
                                          j6h))
        self.j.append( sol.stadiumsolid( 'j7: arch',
                                          dens.Dj[7],
                                          self.Lj[7],
                                          self.Lj[8],
                                          j7h))
        self.j.append( sol.stadiumsolid( 'k8: ball',
                                          dens.Dj[8],
                                          self.Lj[8],
                                          self.Lj[9],
                                          j8h))       
        # get solid heights from length measurements
        k0h = meas['Lk1L']
        k1h = (meas['Lk3L'] + meas['Lk1L']) * 0.5 - k0h
        k2h = meas['Lk3L'] - k1h
        k3h = meas['Lk4L'] - k2h
        k4h = meas['Lk5L'] - k3h
        k5h = meas['Lk6L']
        k6h = (meas['Lk8L'] + meas['Lk6L']) * 0.5 - k5h
        k7h = meas['Lk8L'] - k6h
        k8h = meas['Lk9L'] - k7h
        # right leg
        self.Lk = []
        self.k = []
        # Lk0: hip joint centre
        Lk0p = 2 * np.pi * 0.5 * np.sqrt(np.abs(self.Ls[0].radius *
                                                self.Ls[0].width))
        self.Lk.append( sol.stadium('perim', Lk0p, '=p'))
        # Lk1: crotch
        self.Lk.append( sol.stadium('perim', meas['Lk1p'], '=p'))
        # Lk2: mid-thigh
        self.Lk.append( sol.stadium('perim', meas['Lk2p'], '=p'))
        # Lk3: knee joint centre
        self.Lk.append( sol.stadium('perim', meas['Lk3p'], '=p'))
        # Lk4: maximum calf perimeter
        self.Lk.append( sol.stadium('perim', meas['Lk4p'], '=p'))
        # Lk5: ankle joint centre
        self.Lk.append( sol.stadium('perim', meas['Lk5p'], '=p'))
        # Lk6: heel, aligned anterior-posteriorly
        # rather than medio-laterally
        self.Lk.append( sol.stadium('perimwidth', meas['Lk6p'], meas['Lk6d'],
                                    'AP'))
        # Lk7: arch
        self.Lk.append( sol.stadium('perim', meas['Lk7p'], '=p'))
        # Lk8: ball
        self.Lk.append( sol.stadium('perimwidth', meas['Lk8p'], meas['Lk8w']))
        # Lk9: toe nails
        self.Lk.append( sol.stadium('perimwidth', meas['Lk9p'], meas['Lk9w']))
        
        self.k.append( sol.stadiumsolid( 'k0: hip joint centre',
                                          dens.Dk[0],
                                          self.Lk[0],
                                          self.Lk[1],
                                          k0h))
        self.k.append( sol.stadiumsolid( 'k1: crotch',
                                          dens.Dk[1],
                                          self.Lk[1],
                                          self.Lk[2],
                                          k1h))
        self.k.append( sol.stadiumsolid( 'k2: mid-thigh',
                                          dens.Dk[2],
                                          self.Lk[2],
                                          self.Lk[3],
                                          k2h))
        self.k.append( sol.stadiumsolid( 'k3: knee joint centre',
                                          dens.Dk[3],
                                          self.Lk[3],
                                          self.Lk[4],
                                          k3h))
        self.k.append( sol.stadiumsolid( 'k4: maximum calf perimeter',
                                          dens.Dk[4],
                                          self.Lk[4],
                                          self.Lk[5],
                                          k4h))
        self.k.append( sol.stadiumsolid( 'k5: ankle joint centre',
                                          dens.Dk[5],
                                          self.Lk[5],
                                          self.Lk[6],
                                          k5h))
        self.k.append( sol.stadiumsolid( 'k6: heel',
                                          dens.Dk[6],
                                          self.Lk[6],
                                          self.Lk[7],
                                          k6h))
        self.k.append( sol.stadiumsolid( 'k7: arch',
                                          dens.Dk[7],
                                          self.Lk[7],
                                          self.Lk[8],
                                          k7h))    
        self.k.append( sol.stadiumsolid( 'k8: ball',
                                          dens.Dk[8],
                                          self.Lk[8],
                                          self.Lk[9],
                                          k8h))       
                       
    def define_segments(self):
        '''Define segment objects using previously defined solids. This is where the definition of segment position and rotation really happens. There are 9 segments. Each segment has a base, located at a joint, and an orientation given by the input joint angle parameters.

        '''
        # define all segments
        # pelvis
        Ppos = np.array([[0],[0],[0]])
        PRotMat = mymath.RotateRel([self.CFG['somersalt'],
                                    self.CFG['tilt'],
                                    self.CFG['twist']])
        self.P = seg.segment( 'P: Pelvis', Ppos, PRotMat,
                              [self.s[0],self.s[1]] , 'red')
        # thorax
        Tpos = self.s[1].pos + (self.s[1].height *
                                self.s[1].RotMat * mymath.zunit)
        TRotMat = self.s[1].RotMat * mymath.Rotate3(
                                    [self.CFG['PTsagittalFlexion'],
                                     self.CFG['PTfrontalFlexion'],0])
        self.T = seg.segment( 'T: Thorax', Tpos, TRotMat,
                              [self.s[2]], 'orange')
        # chest-head
        Cpos = self.s[2].pos + (self.s[2].height *
                                self.s[2].RotMat * mymath.zunit)
        CRotMat = self.s[2].RotMat * mymath.Rotate3(
                                    [0,
                                     self.CFG['TClateralSpinalFlexion'],
                                     self.CFG['TCspinalTorsion']])
        self.C = seg.segment( 'C: Chest-head', Cpos, CRotMat,
                              [self.s[3],self.s[4],self.s[5],self.s[6],
                               self.s[7]], 'yellow')
        # left upper arm                                  
        dpos = np.array([[self.s[3].stads[1].width/2],[0.0],
                         [self.s[3].height]])
        A1pos = self.s[3].pos + self.s[3].RotMat * dpos
        A1RotMat = self.s[3].RotMat * (mymath.Rotate3(
                                       [0,-np.pi,0]) * 
                                          mymath.RotateRel(
                                          [self.CFG['CA1elevation'],
                                          -self.CFG['CA1abduction'],
                                          -self.CFG['CA1rotation']]))
        self.A1 = seg.segment( 'A1: Left upper arm', A1pos, A1RotMat,
                               [self.a[0],self.a[1]] , 'green' )
        # left forearm-hand
        A2pos = self.a[1].pos + (self.a[1].height *
                                 self.a[1].RotMat * mymath.zunit)
        A2RotMat = self.a[1].RotMat * mymath.Rotate3(
                                     [self.CFG['A1A2flexion'],0,0])
        self.A2 = seg.segment( 'A2: Left forearm-hand', A2pos, A2RotMat,
                               [self.a[2],self.a[3],self.a[4],self.a[5],
                                self.a[6]], 'red')
        # right upper arm
        dpos = np.array([[-self.s[3].stads[1].width/2],[0.0],
                         [self.s[3].height]])
        B1pos = self.s[3].pos + self.s[3].RotMat * dpos
        B1RotMat = self.s[3].RotMat * (mymath.Rotate3(
                                       [0,-np.pi,0]) *
                                           mymath.RotateRel(
                                           [self.CFG['CB1elevation'],
                                           self.CFG['CB1abduction'],
                                           self.CFG['CB1rotation']]))
        self.B1 = seg.segment( 'B1: Right upper arm', B1pos, B1RotMat,
                               [self.b[0],self.b[1]], 'green')
        # right forearm-hand
        B2pos = self.b[1].pos + (self.b[1].height *
                                 self.b[1].RotMat * mymath.zunit)
        B2RotMat = self.b[1].RotMat * mymath.Rotate3(
                                     [self.CFG['B1B2flexion'],0,0])
        self.B2 = seg.segment( 'B2: Right forearm-hand', B2pos, B2RotMat,
                               [self.b[2],self.b[3],self.b[4],self.b[5],
                                self.b[6]], 'red')
        # left thigh                            
        dpos = np.array([[self.s[0].stads[0].thick],[0.0],[0.0]])
        J1pos = self.s[0].pos + self.s[0].RotMat * dpos
        J1RotMat = self.s[0].RotMat * (mymath.Rotate3(
                                       np.array([0,np.pi,0])) *
                                          mymath.Rotate3(
                                          [self.CFG['PJ1flexion'], 0,
                                          -self.CFG['PJ1abduction']]))
        self.J1 = seg.segment( 'J1: Left thigh', J1pos, J1RotMat,
                               [self.j[0],self.j[1],self.j[2]], 'green')
        # left shank-foot
        J2pos = self.j[2].pos + (self.j[2].height *
                                 self.j[2].RotMat * mymath.zunit)
        J2RotMat = self.j[2].RotMat * mymath.Rotate3(
                                     [-self.CFG['J1J2flexion'],0,0])
        self.J2 = seg.segment( 'J2: Left shank-foot', J2pos, J2RotMat,
                               [self.j[3],self.j[4],self.j[5],self.j[6],
                                self.j[7],self.j[8]], 'red')
        # right thigh                            
        dpos = np.array([[-self.s[0].stads[0].thick],[0.0],[0.0]])
        K1pos = self.s[0].pos + self.s[0].RotMat * dpos
        K1RotMat = self.s[0].RotMat * (mymath.Rotate3(
                                       np.array([0,np.pi,0])) *
                                       mymath.Rotate3(
                                          [self.CFG['PK1flexion'], 0,
                                          self.CFG['PK1abduction']]))
        self.K1 = seg.segment( 'K1: Right thigh', K1pos, K1RotMat,
                               [self.k[0],self.k[1],self.k[2]], 'green')
        # right shank-foot
        K2pos = self.k[2].pos + (self.k[2].height *
                                 self.k[2].RotMat * mymath.zunit)
        K2RotMat = self.k[2].RotMat * mymath.Rotate3(
                                      [-self.CFG['K1K2flexion'],0,0])
        self.K2 = seg.segment( 'K2: Right shank-foot', K2pos, K2RotMat,
                               [self.k[3],self.k[4],self.k[5],self.k[6],
                                self.k[7],self.k[8]], 'red')

    def read_measurements(self,fname):
        '''
        '''
        # initialize measurement conversion factor
        self.measurementconversionfactor = 0 
        # initialize measurement dictionary
        self.meas = {}
        # open measurement file
        fid = open(fname,'r')
        # loop until all 95 parameters are read in
        for line in fid:
            tempstr0 = line
            # skip the line if it is empty
            if (tempstr0.isspace() == False):
                tempstr1 = tempstr0.partition('#')
                # skip lines that start with a pound, after only spaces
                if ((tempstr1[0].isspace() == False) and 
                    (tempstr1[0].find('=') != -1)):
                    tempstr2 = tempstr1[0].partition('=')
                    varname = tempstr2[0].strip()
                    varval = float(tempstr2[2])
                    # identify varname-varval pairs and assign appropriately
                    if varname == 'measurementconversionfactor':
                        self.measurementconversionfactor = varval
                    else:
                    	if varname in self.meas:
                            # key was already defined
                            print "Error in human.read_measurements(fname):" \
                                  " variable",varname,"has been defined " \
                                  "multiple times in input measurement file",\
                                  fname
                        else:
                            if [x for x in self.measnames if x==varname] == []:
                                print "Error in human.read_measurements"\
                                      "(fname): variable name",varname,"in " \
                                      "file",fname,"is not a valid " \
                                      "name for a measurement."
                                raise Exception()
                            else:
                                # okay, go ahead and assign the measurement!
                                self.meas[varname] = float(varval)
        if len(self.meas) != len(self.measnames):
            print "Error in human.read_measurements(fname): there should be", \
                  len(self.measnames),"measurements, but",len(self.meas), \
                  "were found."
        if self.measurementconversionfactor == 0:
            print "Error in human.read_measurements(fname): no variable " \
                  "measurementconversionfactor has been provided. Set as 1 " \
                  "if measurements are given in meters."
        # multiply all values by conversion factor
        for key,val in self.meas.items():
            self.meas[key] = val * self.measurementconversionfactor

    def write_measurements(self,fname):
        '''

        '''
        fid = open(fname,'w')
        for key,val in self.meas.items():
            fid.write(key + "=" + val)
        fid.close()

    def write_meas_for_ISEG(self,fname):
        '''Converts measurement input from the current format to the format used by Yeadon's Fortran code ISEG01B.F

        '''
        SI = 1./1000.
        m = self.meas
        fid = open(fname,'w')
        # refer to Yeadon's iseg01b.f source code to understand
        #  what this stuff is.
        # torso
        L0 = m.s0h
        L1 = L0 + m.s1h
        L2 = L1 + m.s2h
        L3 = L2 + m.s3h
        L4 = L3 + m.s4h
        L5 = m.s5h
        L6 = L5 + m.s6h
        L7 = L6 + m.s7h
        fid.write(str(L0/SI)+','+str(L1/SI)+','+str(L2/SI)+','+str(L3/SI)+','+str(L4/SI)+','+str(L5/SI)+','+str(L6/SI)+','+str(L7/SI)+'\n')
        fid.write(str(m.Ls0p/SI)+','+str(m.Ls1p/SI)+','+str(m.Ls2p/SI)+','+str(m.Ls3p/SI)+','+str(m.Ls5p/SI)+','+str(m.Ls6p/SI)+','+str(m.Ls7p/SI)+'\n')
        fid.write(str(m.Ls0w/SI)+','+str(m.Ls1w/SI)+','+str(m.Ls2w/SI)+','+str(m.Ls3w/SI)+','+str(m.Ls4w/SI)+','+str(m.Ls4d/SI)+'\n')
        # arms
        L0 = m.a0h
        L1 = L0 + m.a1h
        L2 = L1 + m.a2h
        L3 = L2 + m.a3h
        L4 = m.a4h
        L5 = L4 + m.a5h
        L6 = L5 + m.a6h
        fid.write(str(L1/SI)+','+str(L2/SI)+','+str(L3/SI)+','+str(L4/SI)+','+str(L5/SI)+','+str(L6/SI)+','+str(L7/SI)+'\n')
        fid.write(str(m.La0p/SI)+','+str(m.La1p/SI)+','+str(m.La2p/SI)+','+str(m.La3p/SI)+','+str(m.La4p/SI)+','+str(m.La5p/SI)+','+str(m.La6p/SI)+','+str(m.La7p/SI)+'\n')
        fid.write(str(m.La4w/SI)+','+str(m.La5w/SI)+','+str(m.La6w/SI)+','+str(m.La7w/SI)+'\n')
        L0 = m.b0h
        L1 = L0 + m.b1h
        L2 = L1 + m.b2h
        L3 = L2 + m.b3h
        L4 = m.b4h
        L5 = L4 + m.b5h
        L6 = L5 + m.b6h
        fid.write(str(L1/SI)+','+str(L2/SI)+','+str(L3/SI)+','+str(L4/SI)+','+str(L5/SI)+','+str(L6/SI)+','+str(L7/SI)+'\n')
        fid.write(str(m.Lb0p/SI)+','+str(m.Lb1p/SI)+','+str(m.Lb2p/SI)+','+str(m.Lb3p/SI)+','+str(m.Lb4p/SI)+','+str(m.Lb5p/SI)+','+str(m.Lb6p/SI)+','+str(m.Lb7p/SI)+'\n')
        fid.write(str(m.Lb4w/SI)+','+str(m.Lb5w/SI)+','+str(m.Lb6w/SI)+','+str(m.Lb7w/SI)+'\n')
        # legs
        L0 = m.j0h
        L1 = L0 + m.j1h
        L2 = L1 + m.j2h
        L3 = L2 + m.j3h
        L4 = L3 + m.j4h
        L5 = m.j5h
        L6 = L5 + m.j6h
        L7 = L6 + m.j7h
        L8 = L7 + m.j8h
        fid.write(str(L0/SI)+','+str(L2/SI)+','+str(L3/SI)+','+str(L4/SI)+','+str(L5/SI)+','+str(L7/SI)+','+str(L8/SI)+'\n')
        fid.write(str(m.Lj1p/SI)+','+str(m.Lj2p/SI)+','+str(m.Lj3p/SI)+','+str(m.Lj4p/SI)+','+str(m.Lj5p/SI)+','+str(m.Lj6p/SI)+','+str(m.Lj7p/SI)+','+str(m.Lj8p/SI)+','+str(m.Lj9p/SI)+'\n')
        fid.write(str(m.Lj6w/SI)+','+str(m.Lj8w/SI)+','+str(m.Lj9w/SI)+'\n')
        L0 = m.k0h
        L1 = L0 + m.k1h
        L2 = L1 + m.k2h
        L3 = L2 + m.k3h
        L4 = L3 + m.k4h
        L5 = m.k5h
        L6 = L5 + m.k6h
        L7 = L6 + m.k7h
        L8 = L7 + m.k8h
        fid.write(str(L0/SI)+','+str(L2/SI)+','+str(L3/SI)+','+str(L4/SI)+','+str(L5/SI)+','+str(L7/SI)+','+str(L8/SI)+'\n')
        fid.write(str(m.Lk1p/SI)+','+str(m.Lk2p/SI)+','+str(m.Lk3p/SI)+','+str(m.Lk4p/SI)+','+str(m.Lk5p/SI)+','+str(m.Lk6p/SI)+','+str(m.Lk7p/SI)+','+str(m.Lk8p/SI)+','+str(m.Lk9p/SI)+'\n')
        fid.write(str(m.Lk6w/SI)+','+str(m.Lk8w/SI)+','+str(m.Lk9w/SI)+'\n')
        fid.write(str(500)+','+str(200)+'\n')
        fid.close()
        return 0;

    def read_CFG(self,CFGfname):
        '''Reads in a text file that contains the joint angles of the human.
           There is no error-checking for this yet. EDIT, make more durable.

        '''
        self.CFG = {}
        fid = open(CFGfname,'r')
        i = 0
        for line in fid:
            tempstr = line.partition('=')
            self.CFG[human.CFGnames[i]] = float(tempstr[2])
            i += 1

    def write_CFG(self,CFGfname):
        '''

        '''
        fid = open(CFGfname,'w')
        for key,val in self.CFG.items():
            fid.write(key + "=" + val)
        fid.close()

    def draw_vector(self,vec):
        print "not written"
