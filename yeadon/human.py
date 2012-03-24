'''The human module defines the human class, which is composed of segments.
The human class has methods to define the constituent segments from inputs,
calculates their properties, and manages file input/output.

Typical usage (not using yeadon.ui.start_ui())

::

    # create human object, providing paths to measurement and configuration
    # filenames (.txt files). Configuration input is optional.
    H = y.(<measfname>,<CFGfname>)
    # transform the absolute fixed coordiantes from yeadon's to your system's
    H.transform_coord_sys(pos,rotmat)
    # obtain inertia information
    var1 = H.Mass
    var2 = H.COM
    var3 = H.Inertia
    var4 = H.J1.Mass
    var5a = H.J1.relCOM
    var5b = H.J1.COM
    var6 = H.J1.Inertia
    var7 = H.J1.solids[0].Mass
    var8 = H.J1.solids[0].COM
    var9 = H.J1.solids[1].Inertia``

See documentation for a complete description of functionality.
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
try:
    import visual as vis
except ImportError:
    print "Yeadon failed to import python-visual. It is possible that you do" \
          " not have this package. This is fine, it just means that you " \
          "cannot use the draw_visual() member functions."
import inertia

import solid as sol
import segment as seg
import densities as dens

class human:
    measnames = ('Ls1L','Ls2L','Ls3L','Ls4L','Ls5L','Ls6L','Ls7L',
                 'Ls8L','Ls0p','Ls1p','Ls2p','Ls3p','Ls5p','Ls6p',
                 'Ls7p','Ls0w','Ls1w','Ls2w','Ls3w','Ls4w','Ls4d',
                 'La2L','La3L','La4L','La5L','La6L','La7L','La0p',
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

    CFGnames = ('somersalt',
                'tilt',
                'twist',
                'PTsagittalFlexion',
                'PTfrontalFlexion',
                'TCspinalTorsion',
                'TClateralSpinalFlexion',
                'CA1elevation',
                'CA1abduction',
                'CA1rotation',
                'CB1elevation',
                'CB1abduction',
                'CB1rotation',
                'A1A2flexion',
                'B1B2flexion',
                'PJ1flexion',
                'PJ1abduction',
                'PK1flexion',
                'PK1abduction',
                'J1J2flexion',
                'K1K2flexion')

    CFGbounds = [[-np.pi, np.pi],
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

    def __init__(self, meas_in, CFG=None, symmetric=True):
        '''Initializes a human object. Stores inputs as instance variables,
        defines the names of the configuration variables (CFG) in a class
        tuple, defines the bounds on the configuration variables in a class 2D
        list, validates the input CFG against the CFG bounds, defines all the
        solids using the meas input parameter, defines all segments using the
        solid definitions, averages the segment inertia information (if the
        option is selected), calculates the inertia parameters (mass, center of
        mass, inertia tensor) of each solid and then of the entire human.

        Parameters
        ----------
        meas_in : str or dict
            Holds 95 measurements (in meters) that allow the generation of
            stadium solids and an ellipsoid with which to define the model's
            goemetry. See sphinx documentation on how to take the measurements.
            If its type is str, it is the path to a measurements input file.
            See the template .txt file. If its type is a dict, it is a
            dictionary with keys that are the names of the variables in
            the text file. In this latter case, units must be in meters and
            a measured mass canoot be provided.
        CFG : dict
            The configuration of the human (radians). This option is optional.
            If not provided, the human is in a default configuration in which
            all joint angles are set to zero.
        symmetric : bool
            Optional argument, set to True. Decides whether or not to average
            the measurements of the left and right limbs of the human.


        '''
        self.isSymmetric = symmetric
        self.measMass = -1
        # initialize measurement dictionary
        self.meas = {}
        # if measurements input is a module, just assign. else, read in file
        if type(meas_in) == dict:
            self.measurementconversionfactor = 1
            self.meas = meas_in
        elif type(meas_in) == str:
            self.read_measurements(meas_in)
        # average left and right limbs for symmetry (maybe)
        if self.isSymmetric==True:
            self.average_limbs()

        # if configuration input is a dictionary, just assign. else, read in
        # the file.
        if CFG is None: # set all joint angles to zero
            self.CFG = {}
            for key in human.CFGnames:
                self.CFG[key] = 0.0
        elif type(CFG) == dict:
            self.CFG = CFG
        elif type(CFG) == str:
            self.read_CFG(CFG)

        # check CFG input against CFG bounds
        self.validate_CFG()
        # define all solids.
        self.define_torso_solids()
        self.define_arm_solids()
        self.define_leg_solids()
        # define segments. this deals with coordinate transformations.
        # and locates the bases of the segments.
        self.coord_sys_pos = np.array([[0],[0],[0]])
        self.coord_sys_orient = inertia.rotate3((0,0,0))
        self.define_segments()
        # arrange segment pointers into an indexable format
        self.Segments = [ self.P, self.T, self.C,
                          self.A1, self.A2, self.B1, self.B2,
                          self.J1, self.J2, self.K1, self.K2]
        # Yeadon wants to be able to create a symmetrical human.
        # calculate inertia properties of all segments.
        for s in self.Segments:
            s.calc_properties()
        # this next call must happen after the previous
        # per-segment call because human properties depend on segment
        # properties.
        self.calc_properties()
        if self.measMass > 0:
            self.scale_human_by_mass(self.measMass)

    def update_solids(self):
        '''Redefines all solids and then calls yeadon.human.update_segments.
        Called by the method yeadon.human.scale_human_by_mass. The method is
        to be used in instances in which measurements change.

        '''
        self.define_torso_solids()
        self.define_arm_solids()
        self.define_leg_solids()
        self.update_segments()

    def update_segments(self):
        '''Updates all segments. Called after joint angles are updated, in
        which case solids do not need to be recreated, but the segments need
        to be redefined, and the human's inertia parameters (in the global
        frame) must also be redefined.

        '''
        self.validate_CFG()
        self.define_segments()
        # must redefine this Segments list,
        # the code does not work otherwise
        self.Segments = [ self.P, self.T, self.C,
                          self.A1, self.A2, self.B1, self.B2,
                          self.J1, self.J2, self.K1, self.K2]
        for s in self.Segments:
            s.calc_properties()
        self.calc_properties()

    def validate_CFG(self):
        '''Validates the joint angle degrees of freedom against the CFG bounds
        specified in the definition of the human object. Prints an error
        message if there is an issue.

        Returns
        -------
        boolval : bool
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

    def average_limbs(self):
        '''Called only if symmetric=True (which is the default). The left and
        right arms and legs are averaged (the measurements are averaged before
        the code creates yeadon.solid or yeadon.segment objects. To be
        perfectly clear, all left and right arms' and legs' lengths,
        perimeters, widths and depths are averaged between corresponding
        left and right measurements.

        '''
        # make a list of indices to the correct measurements (torso is not
        # averaged)
        leftidxs = np.concatenate( (np.arange(21,39),np.arange(57,76) ),1)
        rightidx = np.concatenate( (np.arange(39,57),np.arange(76,95) ),1)
        for i in np.arange(len(leftidxs)):
            avg = 0.5 * (self.meas[human.measnames[leftidxs[i]]] +
                         self.meas[human.measnames[rightidx[i]]])
            self.meas[human.measnames[leftidxs[i]]] = avg
            self.meas[human.measnames[rightidx[i]]] = avg

    def set_CFG(self, idx, value):
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
            self.CFG[self.CFGnames[idx]] = value
        elif type(idx)==str:
            self.CFG[idx] = value
        else:
            print "set_CFG(idx,value): first argument must be an integer" \
                  " between 0 and 21, or a valid string index for the" \
                  " CFG dictionary."
        self.update_segments()

    def set_CFG_dict(self, CFG):
        '''Allows the user to pass an entirely new CFG dictionary with which
        to update the human object. Ensure that the dictionary is of the
        right format (ideally obtain it from a Human object with human.CFG
        and modify it). After configuration is update, the segments are
        updated.

        CFG : dict
            Stores the 21 joint angles.

        '''
        self.CFG = CFG
        self.update_segments()

    def calc_properties(self):
        '''Calculates the mass, center of mass, and inertia tensor of the
        human. The quantities are calculated from the segment quantities.

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

    def print_properties(self):
        '''Prints human mass, center of mass,and inertia.

        '''
        print "Mass (kg):", self.Mass, "\n"
        print "COM  (m):\n", self.COM, "\n"
        print "Inertia tensor about COM (kg-m^2):\n", self.Inertia, "\n"

    def translate_coord_sys(self,vec):
        '''Moves the cooridinate system from the center of the bottom of the
        human's pelvis to a location defined by the input to this method.
        Note that if this method is used along with
        yeadon.human.rotate_coord_sys, the vector components for the inputs
        to this function are in the new coordinate frame defined by the input
        to yeadon.human.rotate_coord_sys (rather than in the original frame
        of the yeadon module).

        Parameters
        ----------
        vec : list or tuple (3,)
            position of the center of the bottom of the human's torso, with
            respect to the new coordinate system.

        '''
        newpos = np.zeros( (3,1) )
        newpos[0] = vec[0]
        newpos[1] = vec[1]
        newpos[2] = vec[2]
        self.coord_sys_pos = newpos
        self.update_segments()

    def rotate_coord_sys(self,varin):
        '''Rotates the coordinate system, given a list of three rotations
        about the x, y and z axes. For list or tuple input, the order of the
        rotations is x, then, y, then z. All rotations are about the
        original (unrotated) axes (rotations are not relative).

        Parameters
        ----------
        varin : list or tuple (3,) or np.matrix (3,3)
            If list or tuple, the rotations in radians about the x, y,
            and z axes (in that order). If np.matrix, it is a 3x3 rotation
            matrix. For more information, see the DynamicistToolKit
            documentation.

        '''
        if type(varin) == tuple or type(varin) == list:
            rotmat = inertia.rotate3(varin)
        else:
            rotmat = varin
        self.coord_sys_orient = rotmat
        self.update_segments()

    def transform_coord_sys(self,vec,rotmat):
        '''Calls both yeadon.human.translate_coord_sys and
        yeadon.human.rotate_coord_sys.

        Parameters
        ----------
        vec : list or tuple (3,)
            See yeadon.human.translate_coord_sys
        rotmat

        '''
        self.translate_coord_sys(vec)
        self.rotate_coord_sys(rotmat)

    def combine_inertia(self,objlist):
        '''Returns the inertia properties of a combination of solids
        and/or segments of the human, using the fixed human frame (or the
        modified fixed frame as given by the user). Be careful with inputs:
        do not specify a solid that is part of a segment that you have also
        specified. There is some errorchecking for invalid inputs. This method
        does not assign anything to any object attributes, it simply returns
        the desired quantities.

        Parameters
        ----------
        objlist : tuple
            Tuple of strings that identifies solids and/or segments. Options
            for inputs are:
                s0 - s7, a0 - a6, b0 - b6, j0 - j8, k0 - k8
                P, T, C, A1, A2, B1, B2, J1, J2, K1, K2

        Returns
        -------
        resultantMass : float
            Sum of the mass of the input solids and/or segments.
        resultantCOM : np.array (3,1)
            Position of the center of mass of the input solids and/or segments.
            Uses the absolute fixed coordinate system.
        resultantInertia : np.matrix (3,3)
            Inertia tensor at the resultantCOM, with axes aligned with the axes
            of the absolute fixed coordinate system.


        '''

        # preparing to arrange input
        solidkeys = ['s0','s1','s2','s3','s4','s5','s6','s7',
                      'a0','a1','a2','a3','a4','a5','a6',
                      'b0','b1','b2','b3','b4','b5','b6',
                      'j0','j1','j2','j3','j4','j5','j6','j7','j8',
                      'k0','k1','k2','k3','k4','k5','k6','k7','k8',]
        segmentkeys = ['P','T','C','A1','A2','B1','B2','J1','J2','K1','K2']
        solidvals = self.s + self.a + self.b + self.j + self.k
        ObjDict = dict(zip(solidkeys + segmentkeys,solidvals + self.Segments))
        # error-checking
        for key in (solidkeys + segmentkeys):
            if objlist.count(key) > 1:
                print "In yeadon.human.human.combine_inertia(), an object is" \
                      " listed more than once. A solid/segment can only be" \
                      " listed once."
                raise Exception()
        for segkey in segmentkeys:
            if objlist.count(segkey) == 1:
                # this segment is listed as input
                for solobj in objlist:
                    for segsol in ObjDict[segkey].solids:
                        if solobj == segsol.label[0:2]:
                            print "In yeadon.human.human.combine_inertia()," \
                                  " a solid",solobj,"and its parent segment", \
                                  segkey,"have both been given as inputs." \
                                  " This duplicates that solid."
                            raise Exception()
        print "Combining/lumping segments/solids",objlist,"."
        resultantMass = 0.0
        resultantMoment = np.zeros( (3,1) )
        for objstr in objlist:
            if ObjDict.has_key(objstr) == False:
                print "In yeadon.human.human.combine_inertia(),", \
                      "the string",objstr,"does not identify a segment", \
                      "or solid of the human."
                raise Exception()
            obj = ObjDict[objstr]
            resultantMass += obj.Mass
            resultantMoment += obj.Mass * obj.COM
        resultantCOM = resultantMoment / resultantMass
        resultantInertia = np.mat(np.zeros( (3,3) ))
        for objstr in objlist:
            obj = ObjDict[objstr]
            dist = obj.COM - resultantCOM
            resultantInertia += np.mat(inertia.parallel_axis(
                                       obj.Inertia,
                                       obj.Mass,
                                       [dist[0,0],dist[1,0],dist[2,0]]))
        return resultantMass,resultantCOM,resultantInertia

    def draw_visual(self, forward=(-1,1,-1), up=(0,0,1), bg=(0,0,0)):
        '''Draws the human in 3D in a new window using VPython (python-visual).
        The mouse can be used to control or explore the 3D view.
        Scroll to zoom in and out, right click to rotate. This method
        can be followed by other python visual commands (from visual import *)
        and those objects should be drawn in the same window as the human. For
        example, multiple humans can be drawn in one window.

        Parameters
        ----------
        forward : tuple (3,)
            Optional. A vector from the position of the 3D view's camera to
            the origin of the fixed coordinate system. Default is (-1,1,-1)
        up : tuple (3,)
            Optional. A vector denoting the "up" direction. Rotations can only
            be about this vector. Default is (0,0,1).
        bg : tuple (3,)
            Optional. Sets the background color of the view.
            Default is (0,0,0).


        '''
        for s in self.Segments:
            s.draw_visual()
        self.draw_vector(np.array([[0],[0],[0]]),np.array([[.5],[0],[0]]),
                        (1,0,0))
        self.draw_vector(np.array([[0],[0],[0]]),np.array([[0],[.5],[0]]),
                        (0,1,0))
        self.draw_vector(np.array([[0],[0],[0]]),np.array([[0],[0],[.5]]),
                        (0,0,1))
        vis.scene.forward = forward
        vis.scene.up = up
        vis.scene.background = bg
        vis.scene.autocenter = True
        #vis.scene.exit = False

    def draw_vector(self,vec0,vec1, c=(1,1,1), rad=.01):
        '''Draws a vector in a python-visual window. It is expected that this
        method is called in conjuction with yeadon.human.draw_visual,
        so that the vectors are drawn in the same window as the human.

        Parameters
        ----------
        vec0 : str or np.array (3,1)
            Starting position of the vector in the fixed global coordinates.
            If str, it must have the value 'origin'. In this case, the vector
            is drawn from the origin.
        vec1 : np.array (3,1)
            End point of the vector
        c : tuple (3,)
            Optional. Specifies the the color of the vector as a tuple, using
            rgb values (r,g,b) with r,g,b being floats between 0 and 1.
            Default is (1,1,1)
        rad : float
            Optional. Specifies the radius of the shaft of the drawn vector.
            Default is 0.01, which works well when drawn alongside
            typical humans.

        '''
        if vec0 == 'origin':
            vec0 = np.array([[0],[0],[0]])
        conelengthfactor = .05
        ax = (1-conelengthfactor) * (vec1 - vec0)
        vis.cylinder( pos=(vec0[0,0],vec0[1,0],vec0[2,0]),
                  axis=(ax[0,0],ax[1,0],ax[2,0]), radius=rad, color=c)
        coneax = conelengthfactor*ax
        conepos = vec1 - coneax
        vis.cone( pos=(conepos[0,0],conepos[1,0],conepos[2,0]),
              axis=(coneax[0,0],coneax[1,0],coneax[2,0]), radius=3*rad, color=c)

    def draw2D(self):
        '''Uses the matplotlib library to draw a 2D human, from two
        projections. Not implemented well.

        '''
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(121, aspect='equal')
        ax4 = fig2.add_subplot(122, aspect='equal')
        for s in self.Segments:
            s.draw2D(ax2,ax4)
        plt.show()

    def draw(self):
        '''Draws a 3D human by calling the draw methods of all of the segments.
        Drawing is done by the matplotlib library. Currently produces many
        matplotlib warnings, which can be ignored. It is preferred to use the
        yeadon.human.draw_visual mehod instead of this one.

        '''
        fig = plt.figure()
        ax = Axes3D(fig)
        self.P.draw(ax)
        for s in self.Segments:
            s.draw(ax)
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
        ax.set_xlim3d(-limval + self.coord_sys_pos[0,0],
            limval + self.coord_sys_pos[0,0])
        ax.set_ylim3d(-limval + self.coord_sys_pos[1,0],
            limval + self.coord_sys_pos[1,0])
        ax.set_zlim3d(-limval + self.coord_sys_pos[2,0],
            limval + self.coord_sys_pos[2,0])
        # save the plot to an SVG file
        plt.savefig('humanplot', dpi=300)
        # show the plot window, this is a loop actually
        plt.show()

    def draw_octant(self,ax,u,v,c):
        '''Draws an octant of sphere in a matplotlib window (Axes3D library).
        Assists with drawing the center of mass sphere.

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
        '''Defines the solids (from solid.py) that create the torso of
        the human. This requires the definition of 2D stadium levels using
        the input measurement parameters.

        '''

        meas = self.meas
        # get solid heights from length measurements
        s0h = meas['Ls1L']
        s1h = meas['Ls2L'] - meas['Ls1L']
        s2h = meas['Ls3L'] - meas['Ls2L']
        s3h = meas['Ls4L'] - meas['Ls3L']
        s4h = meas['Ls5L'] - meas['Ls4L']
        s5h = meas['Ls6L']
        s6h = meas['Ls7L'] - meas['Ls6L']
        s7h = meas['Ls8L'] - meas['Ls7L']
        # torso
        self.Ls = []
        self.s = []
        self.Ls.append( sol.stadium('Ls0: hip joint centre',
                                    'perimwidth', meas['Ls0p'], meas['Ls0w']))
        self.Ls.append( sol.stadium('Ls1: umbilicus',
                                    'perimwidth', meas['Ls1p'], meas['Ls1w']))
        self.Ls.append( sol.stadium('Ls2: lowest front rib',
                                    'perimwidth', meas['Ls2p'], meas['Ls2w']))
        self.Ls.append( sol.stadium('Ls3: nipple',
                                    'perimwidth', meas['Ls3p'], meas['Ls3w']))
        self.Ls.append( sol.stadium('Ls4: shoulder joint centre',
                                    'depthwidth', meas['Ls4d'], meas['Ls4w']))
        radius = 0.6 * self.Ls[4].radius # see Yeadon's ISEG code
        thick = 0.6 * self.Ls[4].width / 2.0 - radius
        self.Ls.append( sol.stadium('Ls5: acromion',
                                    'thickradius', thick, radius))
        self.Ls.append( sol.stadium('Ls5: acromion/bottom of neck',
                                    'perim',meas['Ls5p'], '=p'))
        self.Ls.append( sol.stadium('Ls6: beneath nose',
                                    'perim', meas['Ls6p'], '=p'))
        self.Ls.append( sol.stadium('Ls7: above ear',
                                    'perim', meas['Ls7p'], '=p'))
        # define solids: this can definitely be done in a loop
        self.s.append( sol.stadiumsolid( 's0: hip joint centre',
                                          dens.Ds[0],
                                          self.Ls[0],
                                          self.Ls[1],
                                          s0h))
        self.s.append( sol.stadiumsolid( 's1: umbilicus',
                                          dens.Ds[1],
                                          self.Ls[1],
                                          self.Ls[2],
                                          s1h))
        self.s.append( sol.stadiumsolid( 's2: lowest front rib',
                                          dens.Ds[2],
                                          self.Ls[2],
                                          self.Ls[3],
                                          s2h))
        self.s.append( sol.stadiumsolid( 's3: nipple',
                                          dens.Ds[3],
                                          self.Ls[3],
                                          self.Ls[4],
                                          s3h))
        self.s.append( sol.stadiumsolid( 's4: shoulder joint centre',
                                          dens.Ds[4],
                                          self.Ls[4],
                                          self.Ls[5],
                                          s4h))
        self.s.append( sol.stadiumsolid( 's5: acromion',
                                          dens.Ds[5],
                                          self.Ls[6],
                                          self.Ls[7],
                                          s5h))
        self.s.append( sol.stadiumsolid( 's6: beneath nose',
                                          dens.Ds[6],
                                          self.Ls[7],
                                          self.Ls[8],
                                          s6h))
        self.s.append( sol.semiellipsoid( 's7: above ear',
                                           dens.Ds[7],
                                           meas['Ls7p'],
                                           s7h))

    def define_arm_solids(self):
        '''Defines the solids (from solid.py) that create the arms of the
        human. This requires the definition of 2D stadium levels using the
        input measurement parameters .

        '''
        meas = self.meas
        # get solid heights from length measurements
        a0h = meas['La2L'] * 0.5
        a1h = meas['La2L'] - meas['La2L'] * 0.5
        a2h = meas['La3L'] - meas['La2L']
        a3h = meas['La4L'] - meas['La3L']
        a4h = meas['La5L']
        a5h = meas['La6L'] - meas['La5L']
        a6h = meas['La7L'] - meas['La6L']
        # left arm
        self.La = []
        self.a = []
        self.La.append( sol.stadium('La0: shoulder joint centre',
                                    'perim', meas['La0p'], '=p'))
        self.La.append( sol.stadium('La1: mid-arm',
                                    'perim', meas['La1p'], '=p'))
        self.La.append( sol.stadium('La2: lowest front rib',
                                    'perim', meas['La2p'], '=p'))
        self.La.append( sol.stadium('La3: nipple',
                                    'perim', meas['La3p'], '=p'))
        self.La.append( sol.stadium('La4: wrist joint centre',
                                    'perimwidth', meas['La4p'], meas['La4w']))
        self.La.append( sol.stadium('La5: acromion',
                                    'perimwidth', meas['La5p'], meas['La5w']))
        self.La.append( sol.stadium('La6: knuckles',
                                    'perimwidth', meas['La6p'], meas['La6w']))
        self.La.append( sol.stadium('La7: fingernails',
                                    'perimwidth', meas['La7p'], meas['La7w']))
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
        b1h = meas['Lb2L'] - meas['Lb2L'] * 0.5
        b2h = meas['Lb3L'] - meas['Lb2L']
        b3h = meas['Lb4L'] - meas['Lb3L']
        b4h = meas['Lb5L']
        b5h = meas['Lb6L'] - meas['Lb5L']
        b6h = meas['Lb7L'] - meas['Lb6L']
        # right arm
        self.Lb = []
        self.b = []
        self.Lb.append( sol.stadium('Lb0: shoulder joint centre',
                                    'perim', meas['Lb0p'], '=p'))
        self.Lb.append( sol.stadium('Lb1: mid-arm',
                                    'perim', meas['Lb1p'], '=p'))
        self.Lb.append( sol.stadium('Lb2: lowest front rib',
                                    'perim', meas['Lb2p'], '=p'))
        self.Lb.append( sol.stadium('Lb3: nipple',
                                    'perim', meas['Lb3p'], '=p'))
        self.Lb.append( sol.stadium('Lb4: wrist joint centre',
                                    'perimwidth', meas['Lb4p'], meas['Lb4w']))
        self.Lb.append( sol.stadium('Lb5: acromion',
                                    'perimwidth', meas['Lb5p'], meas['Lb5w']))
        self.Lb.append( sol.stadium('Lb6: knuckles',
                                    'perimwidth', meas['Lb6p'], meas['Lb6w']))
        self.Lb.append( sol.stadium('Lb7: fingernails',
                                    'perimwidth', meas['Lb7p'], meas['Lb7w']))
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
        '''Defines the solids (from solid.py) that create the legs of the
        human. This requires the definition of 2D stadium levels using
        the input measurement parameters .

        '''
        meas = self.meas
        # get solid heights from length measurements
        j0h = meas['Lj1L']
        j1h = (meas['Lj3L'] + meas['Lj1L']) * 0.5 - meas['Lj1L']
        j2h = meas['Lj3L'] - (meas['Lj3L'] + meas['Lj1L']) * 0.5
        j3h = meas['Lj4L'] - meas['Lj3L']
        j4h = meas['Lj5L'] - meas['Lj4L']
        j5h = meas['Lj6L']
        j6h = (meas['Lj8L'] + meas['Lj6L']) * 0.5 - meas['Lj6L']
        j7h = meas['Lj8L'] - (meas['Lj8L'] + meas['Lj6L']) * 0.5
        j8h = meas['Lj9L'] - meas['Lj8L']
        # left leg
        self.Lj = []
        self.j = []
        Lj0p = 2 * np.pi * 0.5 * np.sqrt(np.abs(self.Ls[0].radius *
                                                self.Ls[0].width))
        self.Lj.append( sol.stadium('Lj0: hip joint centre',
                                    'perim', Lj0p, '=p'))
        self.Lj.append( sol.stadium('Lj1: crotch',
                                    'perim', meas['Lj1p'], '=p'))
        self.Lj.append( sol.stadium('Lj2: mid-thigh',
                                    'perim', meas['Lj2p'], '=p'))
        self.Lj.append( sol.stadium('Lj3: knee joint centre',
                                    'perim', meas['Lj3p'], '=p'))
        self.Lj.append( sol.stadium('Lj4: maximum calf perimeter',
                                    'perim', meas['Lj4p'], '=p'))
        self.Lj.append( sol.stadium('Lj5: ankle joint centre',
                                    'perim', meas['Lj5p'], '=p'))
        self.Lj.append( sol.stadium('Lj6: heel',
                                    'perimwidth', meas['Lj6p'], meas['Lj6d'],
                                    'AP'))
        self.Lj.append( sol.stadium('Lj7: arch',
                                    'perim', meas['Lj7p'], '=p'))
        self.Lj.append( sol.stadium('Lj8: ball',
                                    'perimwidth', meas['Lj8p'], meas['Lj8w']))
        self.Lj.append( sol.stadium('Lj9: toe nails',
                                    'perimwidth', meas['Lj9p'], meas['Lj9w']))
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
        k1h = (meas['Lk3L'] + meas['Lk1L']) * 0.5 - meas['Lk1L']
        k2h = meas['Lk3L'] - (meas['Lk3L'] + meas['Lk1L']) * 0.5
        k3h = meas['Lk4L'] - meas['Lk3L']
        k4h = meas['Lk5L'] - meas['Lk4L']
        k5h = meas['Lk6L']
        k6h = (meas['Lk8L'] + meas['Lk6L']) * 0.5 - meas['Lk6L']
        k7h = meas['Lk8L'] - (meas['Lk8L'] + meas['Lk6L']) * 0.5
        k8h = meas['Lk9L'] - meas['Lk8L']
        # right leg
        self.Lk = []
        self.k = []
        Lk0p = 2 * np.pi * 0.5 * np.sqrt(np.abs(self.Ls[0].radius *
                                                self.Ls[0].width))
        self.Lk.append( sol.stadium('Lk0: hip joint centre',
                                    'perim', Lk0p, '=p'))
        self.Lk.append( sol.stadium('Lk1: crotch',
                                    'perim', meas['Lk1p'], '=p'))
        self.Lk.append( sol.stadium('Lk2: mid-thigh',
                                    'perim', meas['Lk2p'], '=p'))
        self.Lk.append( sol.stadium('Lk3: knee joint centre',
                                    'perim', meas['Lk3p'], '=p'))
        self.Lk.append( sol.stadium('Lk4: maximum calf perimeter',
                                    'perim', meas['Lk4p'], '=p'))
        self.Lk.append( sol.stadium('Lk5: ankle joint centre',
                                    'perim', meas['Lk5p'], '=p'))
        self.Lk.append( sol.stadium('Lk6: heel',
                                    'perimwidth', meas['Lk6p'], meas['Lk6d'],
                                    'AP'))
        self.Lk.append( sol.stadium('Lk7: arch',
                                    'perim', meas['Lk7p'], '=p'))
        self.Lk.append( sol.stadium('Lk8: ball',
                                    'perimwidth', meas['Lk8p'], meas['Lk8w']))
        self.Lk.append( sol.stadium('Lk9: toe nails',
                                    'perimwidth', meas['Lk9p'], meas['Lk9w']))
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
        '''Define segment objects using previously defined solids.
        This is where the definition of segment position and rotation really
        happens. There are 9 segments. Each segment has a base, located
        at a joint, and an orientation given by the input joint angle
        parameters.

        '''
        # define all segments
        # pelvis
        Ppos = self.coord_sys_pos
        PRotMat = (self.coord_sys_orient *
                   inertia.euler_123([self.CFG['somersalt'],
                                    self.CFG['tilt'],
                                    self.CFG['twist']]))
        self.P = seg.segment( 'P: Pelvis', Ppos, PRotMat,
                              [self.s[0],self.s[1]] , (1,0,0))
        # thorax
        Tpos = self.s[1].endpos
        TRotMat = self.s[1].RotMat * inertia.rotate3(
                                    [self.CFG['PTsagittalFlexion'],
                                     self.CFG['PTfrontalFlexion'],0])
        self.T = seg.segment( 'T: Thorax', Tpos, TRotMat,
                              [self.s[2]], (1,.5,0))
        # chest-head
        Cpos = self.s[2].endpos
        CRotMat = self.s[2].RotMat * inertia.rotate3(
                                    [0,
                                     self.CFG['TClateralSpinalFlexion'],
                                     self.CFG['TCspinalTorsion']])
        self.C = seg.segment( 'C: Chest-head', Cpos, CRotMat,
                              [self.s[3],self.s[4],self.s[5],self.s[6],
                               self.s[7]], (1,1,0))
        # left upper arm
        dpos = np.array([[self.s[3].stads[1].width/2],[0.0],
                         [self.s[3].height]])
        A1pos = self.s[3].pos + self.s[3].RotMat * dpos
        A1RotMat = self.s[3].RotMat * (inertia.rotate3(
                                       [0,-np.pi,0]) *
                                          inertia.euler_123(
                                          [self.CFG['CA1elevation'],
                                          -self.CFG['CA1abduction'],
                                          -self.CFG['CA1rotation']]))
        self.A1 = seg.segment( 'A1: Left upper arm', A1pos, A1RotMat,
                               [self.a[0],self.a[1]] , (0,1,0))
        # left forearm-hand
        A2pos = self.a[1].endpos
        A2RotMat = self.a[1].RotMat * inertia.rotate3(
                                     [self.CFG['A1A2flexion'],0,0])
        self.A2 = seg.segment( 'A2: Left forearm-hand', A2pos, A2RotMat,
                               [self.a[2],self.a[3],self.a[4],self.a[5],
                                self.a[6]], (1,0,0))
        # right upper arm
        dpos = np.array([[-self.s[3].stads[1].width/2],[0.0],
                         [self.s[3].height]])
        B1pos = self.s[3].pos + self.s[3].RotMat * dpos
        B1RotMat = self.s[3].RotMat * (inertia.rotate3(
                                       [0,-np.pi,0]) *
                                           inertia.euler_123(
                                           [self.CFG['CB1elevation'],
                                           self.CFG['CB1abduction'],
                                           self.CFG['CB1rotation']]))
        self.B1 = seg.segment( 'B1: Right upper arm', B1pos, B1RotMat,
                               [self.b[0],self.b[1]], (0,1,0))
        # right forearm-hand
        B2pos = self.b[1].endpos
        B2RotMat = self.b[1].RotMat * inertia.rotate3(
                                     [self.CFG['B1B2flexion'],0,0])
        self.B2 = seg.segment( 'B2: Right forearm-hand', B2pos, B2RotMat,
                               [self.b[2],self.b[3],self.b[4],self.b[5],
                                self.b[6]], (1,0,0))
        # left thigh
        dpos = np.array([[.5*self.s[0].stads[0].thick+
                          .5*self.s[0].stads[0].radius],[0.0],[0.0]])
        J1pos = self.s[0].pos + self.s[0].RotMat * dpos
        J1RotMat = self.s[0].RotMat * (inertia.rotate3(
                                       np.array([0,np.pi,0])) *
                                          inertia.rotate3(
                                          [self.CFG['PJ1flexion'],
                                           -self.CFG['PJ1abduction'],0]))
        self.J1 = seg.segment( 'J1: Left thigh', J1pos, J1RotMat,
                               [self.j[0],self.j[1],self.j[2]], (0,1,0))
        # left shank-foot
        J2pos = self.j[2].endpos
        J2RotMat = self.j[2].RotMat * inertia.rotate3(
                                     [-self.CFG['J1J2flexion'],0,0])
        self.J2 = seg.segment( 'J2: Left shank-foot', J2pos, J2RotMat,
                               [self.j[3],self.j[4],self.j[5],self.j[6],
                                self.j[7],self.j[8]], (1,0,0))
        # right thigh
        dpos = np.array([[-.5*self.s[0].stads[0].thick-
                           .5*self.s[0].stads[0].radius],[0.0],[0.0]])
        K1pos = self.s[0].pos + self.s[0].RotMat * dpos
        K1RotMat = self.s[0].RotMat * (inertia.rotate3(
                                       np.array([0,np.pi,0])) *
                                       inertia.rotate3(
                                          [self.CFG['PK1flexion'],
                                           self.CFG['PK1abduction'],0]))
        self.K1 = seg.segment( 'K1: Right thigh', K1pos, K1RotMat,
                               [self.k[0],self.k[1],self.k[2]], (0,1,0))
        # right shank-foot
        K2pos = self.k[2].endpos
        K2RotMat = self.k[2].RotMat * inertia.rotate3(
                                      [-self.CFG['K1K2flexion'],0,0])
        self.K2 = seg.segment( 'K2: Right shank-foot', K2pos, K2RotMat,
                               [self.k[3],self.k[4],self.k[5],self.k[6],
                                self.k[7],self.k[8]], (1,0,0))

    def scale_human_by_mass(self,measmass):
        '''Takes a measured mass and scales all densities by that mass so that
        the mass of the human is the same as the mesaured mass. Mass must be
        in units of kilograms to be consistent with the densities used.

        Parameters
        ----------
        measmass : float
            Measured mass of the human in kilograms.

        '''
        massratio = measmass / self.Mass
        for i in range(len(dens.Ds)):
            dens.Ds[i] = dens.Ds[i] * massratio
        for i in range(len(dens.Da)):
            dens.Da[i] = dens.Da[i] * massratio
        for i in range(len(dens.Db)):
            dens.Db[i] = dens.Db[i] * massratio
        for i in range(len(dens.Dj)):
            dens.Dj[i] = dens.Dj[i] * massratio
        for i in range(len(dens.Dk)):
            dens.Dk[i] = dens.Dk[i] * massratio
        self.update_solids()
        if round(measmass, 2) != round(self.Mass, 2):
            print "Error: attempted to scale mass by a " \
                  "measured mass, but did not succeed. " \
                  "Measured mass:", round(measmass,
                          2),"self.Mass:",round(self.Mass, 2)
            raise Exception()

    def read_measurements(self,fname):
        '''Reads a measurement input .txt file and assigns the measurements
        to fields in the self.meas dict. This method is called by the
        constructor.

        Parameters
        ----------
        fname : str
            Filename or path to measurement file.
        '''
        # initialize measurement conversion factor
        self.measurementconversionfactor = 0
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
                    if len(tempstr2[2]) == 0:
                       print "Error in human.read_measurements(fname):" \
                             " variable",varname,"does not have a value."
                       raise Exception()
                    else:
                       varval = float(tempstr2[2])
                    # identify varname-varval pairs and assign appropriately
                    if varname == 'measurementconversionfactor':
                        self.measurementconversionfactor = varval
                    elif varname == 'totalmass':
                        if varval > 0:
                            # scale densities
                            self.measMass = varval
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
        '''Writes the keys and values of the self.meas dict to a text file.

        Parameters
        ----------
        fname : str
            Filename or path to measurement output .txt file.

        '''
        fid = open(fname,'w')
        for key,val in self.meas.items():
            fid.write(key + "=" + val)
        fid.close()

    def write_meas_for_ISEG(self,fname):
        '''Writes the values of the self.meas dict to a .txt file that is
        formidable as input to Yeadon's ISEG fortran code that performs
        similar calculations to this package.

        Parameters
        ----------
        fname : str
            Filename or path to ISEG .txt input file.
        '''
        fid = open(fname,'w')
        m = self.meas
        SI = 1./1000.
        fid.write(str(m['Ls1L']/SI)+','+str(m['Ls2L']/SI)+','+str(m['Ls3L']/SI)+','+str(m['Ls4L']/SI)+','+str(m['Ls5L']/SI)+','+str(m['Ls6L']/SI)+','+str(m['Ls7L']/SI)+','+str(m['Ls8L']/SI)+'\n')
        fid.write(str(m['Ls0p']/SI)+','+str(m['Ls1p']/SI)+','+str(m['Ls2p']/SI)+','+str(m['Ls3p']/SI)+','+str(m['Ls5p']/SI)+','+str(m['Ls6p']/SI)+','+str(m['Ls7p']/SI)+'\n')
        fid.write(str(m['Ls0w']/SI)+','+str(m['Ls1w']/SI)+','+str(m['Ls2w']/SI)+','+str(m['Ls3w']/SI)+','+str(m['Ls4w']/SI)+','+str(m['Ls4d']/SI)+'\n')
        # arms
        fid.write(str(m['La2L']/SI)+','+str(m['La3L']/SI)+','+str(m['La4L']/SI)+','+str(m['La5L']/SI)+','+str(m['La6L']/SI)+','+str(m['La7L']/SI)+'\n')
        fid.write(str(m['La0p']/SI)+','+str(m['La1p']/SI)+','+str(m['La2p']/SI)+','+str(m['La3p']/SI)+','+str(m['La4p']/SI)+','+str(m['La5p']/SI)+','+str(m['La6p']/SI)+','+str(m['La7p']/SI)+'\n')
        fid.write(str(m['La4w']/SI)+','+str(m['La5w']/SI)+','+str(m['La6w']/SI)+','+str(m['La7w']/SI)+'\n')
        fid.write(str(m['Lb2L']/SI)+','+str(m['Lb3L']/SI)+','+str(m['Lb4L']/SI)+','+str(m['Lb5L']/SI)+','+str(m['Lb6L']/SI)+','+str(m['Lb7L']/SI)+'\n')
        fid.write(str(m['Lb0p']/SI)+','+str(m['Lb1p']/SI)+','+str(m['Lb2p']/SI)+','+str(m['Lb3p']/SI)+','+str(m['Lb4p']/SI)+','+str(m['Lb5p']/SI)+','+str(m['Lb6p']/SI)+','+str(m['Lb7p']/SI)+'\n')
        fid.write(str(m['Lb4w']/SI)+','+str(m['Lb5w']/SI)+','+str(m['Lb6w']/SI)+','+str(m['Lb7w']/SI)+'\n')
        # legs
        fid.write(str(m['Lj1L']/SI)+','+str(m['Lj3L']/SI)+','+str(m['Lj4L']/SI)+','+str(m['Lj5L']/SI)+','+str(m['Lj6L']/SI)+','+str(m['Lj8L']/SI)+','+str(m['Lj9L']/SI)+'\n')
        fid.write(str(m['Lj1p']/SI)+','+str(m['Lj2p']/SI)+','+str(m['Lj3p']/SI)+','+str(m['Lj4p']/SI)+','+str(m['Lj5p']/SI)+','+str(m['Lj6p']/SI)+','+str(m['Lj7p']/SI)+','+str(m['Lj8p']/SI)+','+str(m['Lj9p']/SI)+'\n')
        fid.write(str(m['Lj6d']/SI)+','+str(m['Lj8w']/SI)+','+str(m['Lj9w']/SI)+'\n')
        fid.write(str(m['Lk1L']/SI)+','+str(m['Lk3L']/SI)+','+str(m['Lk4L']/SI)+','+str(m['Lk5L']/SI)+','+str(m['Lk6L']/SI)+','+str(m['Lk8L']/SI)+','+str(m['Lk9L']/SI)+'\n')
        fid.write(str(m['Lk1p']/SI)+','+str(m['Lk2p']/SI)+','+str(m['Lk3p']/SI)+','+str(m['Lk4p']/SI)+','+str(m['Lk5p']/SI)+','+str(m['Lk6p']/SI)+','+str(m['Lk7p']/SI)+','+str(m['Lk8p']/SI)+','+str(m['Lk9p']/SI)+'\n')
        fid.write(str(m['Lk6d']/SI)+','+str(m['Lk8w']/SI)+','+str(m['Lk9w']/SI)+'\n')
        fid.write(str(500)+','+str(200)+'\n')
        fid.close()
        return 0

    def read_CFG(self, CFGfname):
        '''Reads in a text file that contains the joint angles of the human.
        There is little error-checking for this. Make sure that the input
        is consistent with template input .txt files, or with the output
        from the yeadon.human.write_CFG method.

        Parameters
        ----------
        CFGfname : str
            Filename or path to configuration input .txt file.

        '''
        self.CFG = {}
        with open(CFGfname, 'r') as fid:
            for line in fid:
                # skip lines that are comment lines
                if not line.strip().startswith('#'):
                    # remove any whitespace characters and comments at the end
                    # of the line, then split the right and left side of the
                    # equality
                    tempstr = line.strip().split('#')[0].split('=')
                    if tempstr[0]:
                        if tempstr[0] not in human.CFGnames:
                            mes = ('{}'.format(tempstr[0]) +
                                ' is not a correct variable name.')
                            raise StandardError(mes)
                        else:
                            self.CFG[tempstr[0]] = float(tempstr[1])

        if len(self.CFG.keys()) < len(self.CFGnames):
            raise StandardError('You have not supplied all of the joint angles in the CFG file.')

    def write_CFG(self,CFGfname):
        '''Writes the keys and values of the self.CFG dict to a .txt file.

        Parameters
        ----------
        CFGfname : str
            Filename or path to configuration output .txt file

        '''
        fid = open(CFGfname,'w')
        for key,val in self.CFG.items():
            fid.write(key + "=" + val)
        fid.close()

