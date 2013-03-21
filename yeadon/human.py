"""The human module defines the human class, which is composed of segments.
The human class has methods to define the constituent segments from inputs,
calculates their properties, and manages file input/output.

Typical usage (not using yeadon.ui.start_ui())

::

    # create human object, providing paths to measurement and configuration
    # filenames (.txt files). Configuration input is optional.
    H = y.Human(<measfname>, <CFGfname>)
    # transform the absolute fixed coordiantes from yeadon's to your system's
    H.transform_coord_sys(pos, rotmat)
    # obtain inertia information
    var1 = H.mass
    var2 = H.center_of_mass
    # Human's inertia tensor about H.center_of_mass.
    var3 = H.inertia
    var4 = H.J1.mass
    var5a = H.J1.rel_center_of_mass
    var5b = H.J1.center_of_mass
    var6 = H.J1.inertia
    var7 = H.J1.solids[0].mass
    var8 = H.J1.solids[0].center_of_mass
    var9 = H.J1.solids[1].inertia``

See documentation for a complete description of functionality.
"""

# Use Python3 integer division rules.
from __future__ import division
import copy

import numpy as np
try:
    from mayavi import mlab
except ImportError:
    print "Yeadon failed to import mayavi. It is possible that you do" \
          " not have this package. This is fine, it just means that you " \
          "cannot use the draw_mayavi() member functions."
import yaml

import inertia

import solid as sol
import segment as seg

class Human(object):
    measnames = ('Ls1L', 'Ls2L', 'Ls3L', 'Ls4L', 'Ls5L', 'Ls6L', 'Ls7L',
                 'Ls8L', 'Ls0p', 'Ls1p', 'Ls2p', 'Ls3p', 'Ls5p', 'Ls6p',
                 'Ls7p', 'Ls0w', 'Ls1w', 'Ls2w', 'Ls3w', 'Ls4w', 'Ls4d', 
                 'La2L', 'La3L', 'La4L', 'La5L', 'La6L', 'La7L', 'La0p', 
                 'La1p', 'La2p', 'La3p', 'La4p', 'La5p', 'La6p', 'La7p', 
                 'La4w', 'La5w', 'La6w', 'La7w', 
                 'Lb2L', 'Lb3L', 'Lb4L', 'Lb5L', 'Lb6L', 'Lb7L', 'Lb0p', 
                 'Lb1p', 'Lb2p', 'Lb3p', 'Lb4p', 'Lb5p', 'Lb6p', 'Lb7p', 
                 'Lb4w', 'Lb5w', 'Lb6w', 'Lb7w', 
                 'Lj1L', 'Lj3L', 'Lj4L', 'Lj5L', 'Lj6L', 'Lj8L', 'Lj9L', 
                 'Lj1p', 'Lj2p', 'Lj3p', 'Lj4p', 'Lj5p', 'Lj6p', 'Lj7p', 
                 'Lj8p', 'Lj9p', 'Lj8w', 'Lj9w', 'Lj6d', 
                 'Lk1L', 'Lk3L', 'Lk4L', 'Lk5L', 'Lk6L', 'Lk8L', 'Lk9L', 
                 'Lk1p', 'Lk2p', 'Lk3p', 'Lk4p', 'Lk5p', 'Lk6p', 'Lk7p', 
                 'Lk8p', 'Lk9p', 'Lk8w', 'Lk9w', 'Lk6d')

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

    @property
    def mass(self):
        """Mass of the human, in units of kg."""
        return self._mass

    @property
    def center_of_mass(self):
        """Center of mass of the human, a np.ndarray, in units of m, in the
        global frame centered at the bottom center of the pelvis."""
        return self._center_of_mass

    @property
    def inertia(self):
        """Inertia matrix/dyadic of the human, a np.matrix, in units of
        kg-m^2, about the center of mass of the human, in the global frame.
        """
        return self._inertia

    # Densities come from Yeadon 1990-ii.
    # Units from the paper are kg/L, units below are kg/m^3.
    # Headings for the segmental densities below:
    segment_names = ['head-neck', 'shoulders', 'thorax', 'abdomen-pelvis',
            'upper-arm', 'forearm', 'hand', 'thigh', 'lower-leg', 'foot']
    #   head-neck     thorax        upper arm     hand          lower leg
    #            shoulders   abdomenpelvis forearm       thigh         foot
    segmental_densities = {
        'Chandler': dict(zip(segment_names,
        [1056,  853,  853,  853, 1005, 1052, 1080, 1020, 1078, 1091])),
        'Dempster': dict(zip(segment_names,
        [1110, 1040,  920, 1010, 1070, 1130, 1160, 1050, 1090, 1100])),
        'Clauser': dict(zip(segment_names,
        [1070, 1019, 1019, 1019, 1056, 1089, 1109, 1044, 1085, 1084])),
        }

    def __init__(self, meas_in, CFG=None, symmetric=True,
            density_set='Dempster'):
        """Initializes a human object. Stores inputs as instance variables,
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
        CFG : str or dict, optional
            The configuration of the human (radians).
            If its type is str, it is the path to a CFG input file in YAML
            syntax (see template CFGtemplate.txt). If its type is dict, it must
            have an entry for each of the 21 names in Human.CFGnames or in the
            template. If not provided, the human is in a default configuration
            in which all joint angles are set to zero.
        symmetric : bool, optional
            True by default. Decides whether or not to average the measurements
            of the left and right limbs of the human. This has nothing to with
            the configuration being symmetric.
        density_set : str, optional
            Selects a set of densities to use for the body segments.
            Either 'Chandler', 'Clauser', or 'Dempster'. 'Dempster' by default.
            See class variable `segmental_densities` to inspect their values.

        """
        # Initialize position and orientation of entire body.
        self.coord_sys_pos = np.array([[0],[0],[0]])
        self.coord_sys_orient = inertia.rotate_space_123((0,0,0))

        # Assign densities for the solids.
        if density_set not in ['Chandler', 'Clauser', 'Dempster']:
            raise Exception("Density set {0!r} is not one of 'Chandler', "
                    "'Clauser', or 'Dempster'.".format(density_set))
        self._density_set = density_set

        self.is_symmetric = symmetric
        self.meas_mass = -1
        # initialize measurement dictionary
        self.meas = dict()
        # if measurements input is a module, just assign. else, read in file
        if type(meas_in) == dict:
            self.measurementconversionfactor = 1
            self.meas = meas_in
        elif type(meas_in) == str:
            self._read_measurements(meas_in)
        # average left and right limbs for symmetry (maybe)
        if self.is_symmetric == True:
            self._average_limbs()

        # Start off a zero configuration.
        self.CFG = dict()
        for key in Human.CFGnames:
            self.CFG[key] = 0.0

        # update will define all solids, validate CFG, define segments,
        # and calculate segment and human mass properties.
        self.update()

        if self.meas_mass > 0:
            self.scale_human_by_mass(self.meas_mass)

        # If configuration input is a dictionary, assign via public method.
        # Else, read in the file.
        if type(CFG) == dict:
            self.set_CFG_dict(CFG)
        elif type(CFG) == str:
            self._read_CFG(CFG)

    def _assign_densities(self, density_set):
        """Assigns densities from `segmental_densities` to instance variables
        holding the density of each solid.
        """


    def update(self):
        """Redefines all solids and then calls yeadon.Human._update_segments.
        Called by the method yeadon.Human.scale_human_by_mass. The method is
        to be used in instances in which measurements change.

        """
        self._define_torso_solids()
        self._define_arm_solids()
        self._define_leg_segments()
        self._update_segments()

    def _update_segments(self):
        """Updates all segments. Called after joint angles are updated, in
        which case solids do not need to be recreated, but the segments need
        to be redefined, and the human's inertia parameters (in the global
        frame) must also be redefined.

        """
        self._validate_CFG()
        self._define_segments()
        # must redefine this Segments list,
        # the code does not work otherwise
        self.segments = [ self.P, self.T, self.C,
                          self.A1, self.A2, self.B1, self.B2,
                          self.J1, self.J2, self.K1, self.K2]
        for s in self.segments:
            s.calc_properties()
        # Must update segment properties before updating the human properties.
        self.calc_properties()

    def _validate_CFG(self):
        """Validates the joint angle degrees of freedom against the CFG bounds
        specified in the definition of the human object. Prints an error
        message if there is an issue.

        Returns
        -------
        boolval : bool
            True if all configuration variables are okay, False if there is an
            issue

        """
        boolval = True
        for i in np.arange(len(self.CFG)):
            if (self.CFG[Human.CFGnames[i]] < Human.CFGbounds[i][0] or
                self.CFG[Human.CFGnames[i]] > Human.CFGbounds[i][1]):
                print "Joint angle",Human.CFGnames[i],"=",\
                      self.CFG[Human.CFGnames[i]]/np.pi,\
                      "pi-rad is out of range. Must be between",\
                      Human.CFGbounds[i][0]/np.pi,"and",\
                      Human.CFGbounds[i][1]/np.pi,"pi-rad."
                boolval = False
        return boolval

    def _average_limbs(self):
        """Called only if symmetric=True (which is the default). The left and
        right arms and legs are averaged (the measurements are averaged before
        the code creates yeadon.Solid or yeadon.Segment objects. To be
        perfectly clear, all left and right arms' and legs' lengths,
        perimeters, widths and depths are averaged between corresponding
        left and right measurements.

        """
        # make a list of indices to the correct measurements (torso is not
        # averaged)
        # [21, 38] U [57, 75] are the left limbs.
        # [39, 57] U [76, 95] are the right limbs.
        leftidxs = np.concatenate( (np.arange(21,39),np.arange(57,76) ),1)
        rightidx = np.concatenate( (np.arange(39,57),np.arange(76,95) ),1)
        for i in np.arange(len(leftidxs)):
            avg = 0.5 * (self.meas[Human.measnames[leftidxs[i]]] +
                         self.meas[Human.measnames[rightidx[i]]])
            self.meas[Human.measnames[leftidxs[i]]] = avg
            self.meas[Human.measnames[rightidx[i]]] = avg

    def set_CFG(self, varname, value):
        """Allows the user to set a single configuration variable in CFG. CFG
        is a dictionary that holds all 21 configuration variables. Then, this
        function validates and updates the human model with the new
        configuration variable.

           Parameters
           ----------
           varname : str
               Must be a valid name of a configuration variable.
           value : float
               New value for the configuration variable identified by varname.
               Units are radians.  This value will be validated for joint angle
               limits.

        """
        if varname not in self.CFGnames:
            raise Exception("'{0}' is not a valid name of a configuration "
                    "variable.".format(varname))
        self.CFG[varname] = value
        self._update_segments()

    def set_CFG_dict(self, CFG):
        """Allows the user to pass an entirely new CFG dictionary with which
        to update the human object. Ensure that the dictionary is of the
        right format (ideally obtain it from a Human object with Human.CFG
        and modify it). After configuration is update, the segments are
        updated.

        CFG : dict
            Stores the 21 joint angles.

        """
        # Some error checking.
        if len(CFG) != len(self.CFGnames):
            raise Exception("Number of CFG variables, {0}, is "
                    "incorrect.".format(len(CFG)))
        for key, val in CFG.items():
            if key not in self.CFGnames:
                raise Exception("'{0}' is not a correct variable "
                        "name.".format(key))
        self.CFG = CFG
        self._update_segments()

    def calc_properties(self):
        """Calculates the mass, center of mass, and inertia tensor of the
        human. The quantities are calculated from the segment quantities.

        """
        # mass
        self._mass = 0.0;
        for s in self.segments:
            self._mass += s.mass
        # center of mass
        moment = np.zeros((3,1))
        for s in self.segments:
            moment += s.mass * s.center_of_mass
        self._center_of_mass = moment / self.mass
        # inertia
        self._inertia = np.mat(np.zeros((3,3)))
        for s in self.segments:
            dist = s.center_of_mass - self.center_of_mass
            self._inertia += np.mat(
                inertia.parallel_axis(s.inertia,
                                      s.mass,
                                      [dist[0,0],dist[1,0],dist[2,0]]))

    def print_properties(self):
        """Prints human mass, center of mass, and inertia.

        """
        print "Mass (kg):", self.mass, "\n"
        print "COM  (m):\n", self.center_of_mass, "\n"
        print "Inertia tensor about COM (kg-m^2):\n", self.inertia, "\n"

    def translate_coord_sys(self, vec):
        """Moves the cooridinate system from the center of the bottom of the
        human's pelvis to a location defined by the input to this method.
        Note that if this method is used along with
        yeadon.Human.rotate_coord_sys, the vector components for the inputs
        to this function are in the new coordinate frame defined by the input
        to yeadon.Human.rotate_coord_sys (rather than in the original frame
        of the yeadon module).

        Parameters
        ----------
        vec : list or tuple (3,)
            position of the center of the bottom of the human's torso, with
            respect to the new coordinate system.

        """
        newpos = np.zeros( (3,1) )
        newpos[0] = vec[0]
        newpos[1] = vec[1]
        newpos[2] = vec[2]
        self.coord_sys_pos = newpos
        self._update_segments()

    def rotate_coord_sys(self, varin):
        """Rotates the coordinate system. For list or tuple input, the order of
        the rotations is x, then, y, then z.

        Parameters
        ----------
        varin : list or tuple (3,) or np.matrix (3,3)
            If list or tuple, the rotations are in radians about the x, y, and
            z axes (in that order).  In this case, rotations are space-fixed.
            In other words, they are space-fixed rotations as opposed to
            body-fixed rotations.  If np.matrix, it is a 3x3 rotation matrix.
            For more information, see the inertia.rotate_space_123
            documentation.

        """
        if type(varin) == tuple or type(varin) == list:
            rotmat = inertia.rotate_space_123(varin)
        else:
            rotmat = varin
        self.coord_sys_orient = rotmat
        self._update_segments()

    def transform_coord_sys(self, vec, rotmat):
        """Calls both yeadon.Human.translate_coord_sys and
        yeadon.Human.rotate_coord_sys.

        Parameters
        ----------
        vec : list or tuple (3,)
            See yeadon.Human.translate_coord_sys
        rotmat

        """
        self.translate_coord_sys(vec)
        self.rotate_coord_sys(rotmat)

    def inertia_transformed(self, pos=None, rotmat=None):
        """Returns an inertia tensor about `pos` and in the frame given by
        `rotmat` relative to the global frame. If N is the global frame, B is
        the name given by rotmat = ^{B}R^{N}, and pos = r^{P/N0}, this method
        returns ^{B}I^{H/P}.

        pos : list or tuple (3,)
            Position in the global coordinate system to the point about which
            the user desires the inertia tensor.
        rotmat : np.matrix (3,3)

        """
        pass

    def combine_inertia(self, objlist):
        """Returns the inertia properties of a combination of solids
        and/or segments of the human, using the fixed human frame (or the
        modified fixed frame as given by the user). Be careful with inputs:
        do not specify a solid that is part of a segment that you have also
        specified. This method does not assign anything to any object
        attributes (it is 'const'), it simply returns the desired quantities.

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

        """
        # preparing to arrange input
        solidkeys = ['s0','s1','s2','s3','s4','s5','s6','s7',
                      'a0','a1','a2','a3','a4','a5','a6',
                      'b0','b1','b2','b3','b4','b5','b6',
                      'j0','j1','j2','j3','j4','j5','j6','j7','j8',
                      'k0','k1','k2','k3','k4','k5','k6','k7','k8',]
        segmentkeys = ['P','T','C','A1','A2','B1','B2','J1','J2','K1','K2']
        solidvals = self._s + self._a + self._b + self._j + self._k
        ObjDict = dict(zip(solidkeys + segmentkeys, solidvals + self.segments))
        # error-checking
        for key in (solidkeys + segmentkeys):
            if objlist.count(key) > 1:
                print "In yeadon.human.Human.combine_inertia(), an object is" \
                      " listed more than once. A solid/segment can only be" \
                      " listed once."
                raise Exception()
        for segkey in segmentkeys:
            if objlist.count(segkey) == 1:
                # this segment is listed as input
                for solobj in objlist:
                    for segsol in ObjDict[segkey].solids:
                        if solobj == segsol.label[0:2]:
                            print "In yeadon.human.Human.combine_inertia()," \
                                  " a solid",solobj,"and its parent segment", \
                                  segkey,"have both been given as inputs." \
                                  " This duplicates that solid."
                            raise Exception()
        print "Combining/lumping segments/solids",objlist,"."
        resultantMass = 0.0
        resultantMoment = np.zeros( (3,1) )
        for objstr in objlist:
            if ObjDict.has_key(objstr) == False:
                print "In yeadon.human.Human.combine_inertia(),", \
                      "the string",objstr,"does not identify a segment", \
                      "or solid of the human."
                raise Exception()
            obj = ObjDict[objstr]
            resultantMass += obj.mass
            resultantMoment += obj.mass * obj.center_of_mass
        resultantCOM = resultantMoment / resultantMass
        resultantInertia = np.mat(np.zeros( (3,3) ))
        for objstr in objlist:
            obj = ObjDict[objstr]
            dist = obj.center_of_mass - resultantCOM
            resultantInertia += np.mat(inertia.parallel_axis(
                                       obj.inertia,
                                       obj.mass,
                                       [dist[0,0],dist[1,0],dist[2,0]]))
        return resultantMass, resultantCOM, resultantInertia

    def get_segment_by_name(self, name):
        """Returns a segment given its name."""
        labels = [s.label[0:len(name)] for s in self.segments]
        return self.segments[labels.index(name)]

    def draw_mayavi(self, mlabobj=mlab):
        """Draws the human in 3D in a new window using MayaVi.
        The mouse can be used to control or explore the 3D view.

        """
        for s in self.segments:
            s.draw_mayavi(mlabobj)
        L = 0.4
        x_cone, y_cone, z_cone = self._make_mayavi_cone_pos()
        mlabobj.mesh(x_cone, y_cone, z_cone + L, color=(0, 0, 1))
        mlabobj.mesh(x_cone, z_cone + L, y_cone, color=(0, 1, 0))
        mlabobj.mesh(z_cone + L, x_cone, y_cone, color=(1, 0, 0))
        x_cyl, y_cyl, z_cyl = self._make_mayavi_cyl_pos()
        mlabobj.mesh(x_cyl, y_cyl, z_cyl, color=(0, 0, 1))
        mlabobj.mesh(x_cyl, z_cyl, y_cyl, color=(0, 1, 0))
        mlabobj.mesh(z_cyl, x_cyl, y_cyl, color=(1, 0, 0))
        #x_plate,  y_plate, z_plate = self._make_mayavi_plate_pos()
        #mlabobj.contour3d(x_plate, y_plate, z_plate + L, color=(0, 0, 1))
        #mlabobj.contour3d(x_plate, z_plate + L, y_plate, color=(0, 1, 0))
        #mlabobj.contour3d(z_plate + L, x_plate, y_plate, color=(1, 0, 0))

    def _update_mayavi(self):
        """Updates all of the segments for MayaVi."""
        for s in self.segments:
            s._update_mayavi()

    def _make_mayavi_cone_pos(self):
        L2 = 0.04
        R2 = L2
        [theta, z] = np.mgrid[0:3*np.pi*(1+2/10):np.pi/10, 0:L2+L2/10:L2/10]
        r = R2 * (1 - z/L2)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x, y, z

    def _make_mayavi_cyl_pos(self):
        L1 = 0.4
        R1 = 0.02
        [theta, z] = np.mgrid[0:3*np.pi*(1+2/10):np.pi/10, 0:L1+L1/10:L1/10]
        x = R1 * np.cos(theta)
        y = R1 * np.sin(theta)
        return x, y, z

    def _make_mayavi_plate_pos(self):
        R1 = 0.04
        [theta, z] = np.mgrid[0:3*np.pi*(1+2/10):np.pi/10, 0:.02:.01]
        x = R1 * np.cos(theta)
        y = R1 * np.sin(theta)
        return x, y, z

    def _draw_mayavi_inertia_ellipsoid(self, mlabobj):
        """Draws the inertia ellipsoid centered at the human's center of mass.
        TODO describe what it is."""
        # First get the eigenvectors and values.
        self._generate_mesh_inertia_ellipsoid()
        self._ellipsoid_mesh = mlabobj.mesh(*self._ellipsoid_mesh_points,
                color=(1, 1, 1), opacity=0.2)

    def _update_mayavi_inertia_ellipsoid(self):
        """Updates the mesh in MayaVi."""
        self._generate_mesh_inertia_ellipsoid()
        self._ellipsoid_mesh.mlab_source.set(x=self._ellipsoid_mesh_points[0],
                y=self._ellipsoid_mesh_points[1],
                z=self._ellipsoid_mesh_points[2])

    def _generate_mesh_inertia_ellipsoid(self):
        """Generates a mesh for MayaVi."""
        self._ellipsoid_mesh_points = self._make_inertia_ellipsoid_pos()

    def _make_inertia_ellipsoid_pos(self):
        """Generates coordinates to be used for 3D visualization purposes."""
        eigvals, eigvecs = np.linalg.eig(self.inertia)
        axes = 1.0/np.sqrt(eigvals)
        N = 50
        u = np.linspace(0, 2.0 * np.pi, N)
        v = np.linspace(0, np.pi, N)
        x = axes[0] * np.outer(np.cos(u), np.sin(v))
        y = axes[1] * np.outer(np.sin(u), np.sin(v))
        z = axes[2] * np.outer(np.ones(np.size(u)), np.cos(v))
        for i in np.arange(N):
            for j in np.arange(N):
                POS = np.array([[x[i,j]],[y[i,j]],[z[i,j]]])
                POS = eigvecs * POS
                x[i,j] = POS[0,0]
                y[i,j] = POS[1,0]
                z[i,j] = POS[2,0]
        x = self.center_of_mass[0,0] + x
        y = self.center_of_mass[1,0] + y
        z = self.center_of_mass[2,0] + z
        return x, y, z

    def _make_sphere_octant(self, octant_no):
        """Returns coordinates that define an octant of a sphere. This method
        is not currently used, but could be used in rendering. The idea is to
        use it for drawing a center of mass ball.

        Parameters
        ----------
        octact_no : int
            Integer in the range [1, 8] to identify the octant for which points
            are desired. The octants are defined as follows:
            
            1.  x > 0, y > 0, z > 0
            2.  x < 0, y > 0, z > 0
            3.  x < 0, y < 0, z > 0
            4.  x > 0, y < 0, z > 0
            5.  x > 0, y > 0, z < 0
            6.  x < 0, y > 0, z < 0
            7.  x < 0, y < 0, z < 0
            8.  x > 0, y < 0, z < 0

        Returns
        -------
        x : np.array
            x-coordinates for the octant.
        y : np.array
            y-coordinates for the octant.
        z : np.array
            z-coordinates for the octant.

        """
        if not octant_no in [1, 2, 3, 4, 5, 6, 7, 8]:
            raise ValueError("Octant number %i is invalid." % octant_no)

        N = 30

        # Phi, azimuthal.
        if octant_no in [1, 5]:
            u = np.linspace(0, 0.5 * np.pi, N)
        elif octant_no in [2, 6]:
            u = np.linspace(0.5 * np.pi, np.pi, N)
        elif octant_no in [3, 7]:
            u = np.linspace(np.pi, 1.5 * np.pi , N)
        elif octant_no in [4, 8]:
            u = np.linspace(1.5 * np.pi, 2.0 * np.pi,  N)

        # Theta, colatitude.
        if octant_no in [1, 2, 3, 4]:
            v = np.linspace(0, 0.5 * np.pi, N)
        else:
            v = np.linspace(0.5 * np.pi, np.pi, N)

        R = 0.05
        x = R * np.outer(np.cos(u), np.sin(v))
        y = R * np.outer(np.sin(u), np.sin(v))
        z = R * np.outer(np.ones(np.size(u)), np.cos(v))
        return x, y, z

    def _define_torso_solids(self):
        """Defines the solids (from solid.py) that create the torso of
        the human. This requires the definition of 2D stadium levels using
        the input measurement parameters.

        """

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
        self._Ls = []
        self._s = []
        self._Ls.append( sol.Stadium('Ls0: hip joint centre',
                                    'perimwidth', meas['Ls0p'], meas['Ls0w']))
        self._Ls.append( sol.Stadium('Ls1: umbilicus',
                                    'perimwidth', meas['Ls1p'], meas['Ls1w']))
        self._Ls.append( sol.Stadium('Ls2: lowest front rib',
                                    'perimwidth', meas['Ls2p'], meas['Ls2w']))
        self._Ls.append( sol.Stadium('Ls3: nipple',
                                    'perimwidth', meas['Ls3p'], meas['Ls3w']))
        self._Ls.append( sol.Stadium('Ls4: shoulder joint centre',
                                    'depthwidth', meas['Ls4d'], meas['Ls4w']))
        # Yeadon's ISEG code uses the value 0.57. Up through version 0.95 of
        # this package, we used the value 0.6 instead. There was no good
        # justification for this, other than that 0.57 seemed equally
        # unjustifiable. The reason why the next two lines exist at all is
        # that it's not possible to measure a perimeter, etc at the acromion,
        # so we find this stadium's parameters as a function of the Ls4
        # parameters.
        # Previous code:
        #radius = 0.6 * self._Ls[4].radius # see Yeadon's ISEG code
        #thick = 0.6 * self._Ls[4].width / 2.0 - radius
        # New code:
        radiusLs5 = 0.57 * self._Ls[4].radius
        thicknessLs5 = self._Ls[4].width / 2.0 - radiusLs5
        self._Ls.append( sol.Stadium('Ls5: acromion',
                                    'thicknessradius', thicknessLs5, radiusLs5))
        self._Ls.append( sol.Stadium('Ls5: acromion/bottom of neck',
                                    'perimeter',meas['Ls5p'], '=p'))
        self._Ls.append( sol.Stadium('Ls6: beneath nose',
                                    'perimeter', meas['Ls6p'], '=p'))
        self._Ls.append( sol.Stadium('Ls7: above ear',
                                    'perimeter', meas['Ls7p'], '=p'))
        # define solids: this can definitely be done in a loop
        self._s.append( sol.StadiumSolid( 's0: hip joint centre',
                self.segmental_densities[self._density_set]['abdomen-pelvis'],
                self._Ls[0],
                self._Ls[1],
                s0h))
        self._s.append( sol.StadiumSolid( 's1: umbilicus',
                self.segmental_densities[self._density_set]['abdomen-pelvis'],
                self._Ls[1],
                self._Ls[2],
                s1h))
        self._s.append( sol.StadiumSolid( 's2: lowest front rib',
                self.segmental_densities[self._density_set]['thorax'],
                self._Ls[2],
                self._Ls[3],
                s2h))
        self._s.append( sol.StadiumSolid( 's3: nipple',
                self.segmental_densities[self._density_set]['thorax'],
                self._Ls[3],
                self._Ls[4],
                s3h))
        self._s.append( sol.StadiumSolid( 's4: shoulder joint centre',
                self.segmental_densities[self._density_set]['shoulders'],
                self._Ls[4],
                self._Ls[5],
                s4h))
        self._s.append( sol.StadiumSolid( 's5: acromion',
                self.segmental_densities[self._density_set]['head-neck'],
                self._Ls[6],
                self._Ls[7],
                s5h))
        self._s.append( sol.StadiumSolid( 's6: beneath nose',
                self.segmental_densities[self._density_set]['head-neck'],
                self._Ls[7],
                self._Ls[8],
                s6h))
        self._s.append( sol.Semiellipsoid( 's7: above ear',
                self.segmental_densities[self._density_set]['head-neck'],
                meas['Ls7p'],
                s7h))

    def _define_arm_solids(self):
        """Defines the solids (from solid.py) that create the arms of the
        human. This requires the definition of 2D stadium levels using the
        input measurement parameters .

        """
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
        self._La = []
        self._a = []
        self._La.append( sol.Stadium('La0: shoulder joint centre',
                                    'perimeter', meas['La0p'], '=p'))
        self._La.append( sol.Stadium('La1: mid-arm',
                                    'perimeter', meas['La1p'], '=p'))
        self._La.append( sol.Stadium('La2: lowest front rib',
                                    'perimeter', meas['La2p'], '=p'))
        self._La.append( sol.Stadium('La3: nipple',
                                    'perimeter', meas['La3p'], '=p'))
        self._La.append( sol.Stadium('La4: wrist joint centre',
                                    'perimwidth', meas['La4p'], meas['La4w']))
        self._La.append( sol.Stadium('La5: base of thumb',
                                    'perimwidth', meas['La5p'], meas['La5w']))
        self._La.append( sol.Stadium('La6: knuckles',
                                    'perimwidth', meas['La6p'], meas['La6w']))
        self._La.append( sol.Stadium('La7: fingernails',
                                    'perimwidth', meas['La7p'], meas['La7w']))
        # define left arm solids
        self._a.append( sol.StadiumSolid( 'a0: shoulder joint centre',
                self.segmental_densities[self._density_set]['upper-arm'],
                self._La[0],
                self._La[1],
                a0h))
        self._a.append( sol.StadiumSolid( 'a1: mid-arm',
                self.segmental_densities[self._density_set]['upper-arm'],
                self._La[1],
                self._La[2],
                a1h))
        self._a.append( sol.StadiumSolid( 'a2: elbow joint centre',
                self.segmental_densities[self._density_set]['forearm'],
                self._La[2],
                self._La[3],
                a2h))
        self._a.append( sol.StadiumSolid( 'a3: maximum forearm perimeter',
                self.segmental_densities[self._density_set]['forearm'],
                self._La[3],
                self._La[4],
                a3h))
        self._a.append( sol.StadiumSolid( 'a4: wrist joint centre',
                self.segmental_densities[self._density_set]['hand'],
                self._La[4],
                self._La[5],
                a4h))
        self._a.append( sol.StadiumSolid( 'a5: base of thumb',
                self.segmental_densities[self._density_set]['hand'],
                self._La[5],
                self._La[6],
                a5h))
        self._a.append( sol.StadiumSolid( 'a6: knuckles',
                self.segmental_densities[self._density_set]['hand'],
                self._La[6],
                self._La[7],
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
        self._Lb = []
        self._b = []
        self._Lb.append( sol.Stadium('Lb0: shoulder joint centre',
                                    'perimeter', meas['Lb0p'], '=p'))
        self._Lb.append( sol.Stadium('Lb1: mid-arm',
                                    'perimeter', meas['Lb1p'], '=p'))
        self._Lb.append( sol.Stadium('Lb2: lowest front rib',
                                    'perimeter', meas['Lb2p'], '=p'))
        self._Lb.append( sol.Stadium('Lb3: nipple',
                                    'perimeter', meas['Lb3p'], '=p'))
        self._Lb.append( sol.Stadium('Lb4: wrist joint centre',
                                    'perimwidth', meas['Lb4p'], meas['Lb4w']))
        self._Lb.append( sol.Stadium('Lb5: base of thumb',
                                    'perimwidth', meas['Lb5p'], meas['Lb5w']))
        self._Lb.append( sol.Stadium('Lb6: knuckles',
                                    'perimwidth', meas['Lb6p'], meas['Lb6w']))
        self._Lb.append( sol.Stadium('Lb7: fingernails',
                                    'perimwidth', meas['Lb7p'], meas['Lb7w']))
        # define right arm solids
        self._b.append( sol.StadiumSolid( 'b0: shoulder joint centre',
                self.segmental_densities[self._density_set]['upper-arm'],
                self._Lb[0],
                self._Lb[1],
                b0h))
        self._b.append( sol.StadiumSolid( 'b1: mid-arm',
                self.segmental_densities[self._density_set]['upper-arm'],
                self._Lb[1],
                self._Lb[2],
                b1h))
        self._b.append( sol.StadiumSolid( 'b2: elbow joint centre',
                self.segmental_densities[self._density_set]['forearm'],
                self._Lb[2],
                self._Lb[3],
                b2h))
        self._b.append( sol.StadiumSolid( 'b3: maximum forearm perimeter',
                self.segmental_densities[self._density_set]['forearm'],
                self._Lb[3],
                self._Lb[4],
                b3h))
        self._b.append( sol.StadiumSolid( 'b4: wrist joint centre',
                self.segmental_densities[self._density_set]['hand'],
                self._Lb[4],
                self._Lb[5],
                b4h))
        self._b.append( sol.StadiumSolid( 'b5: base of thumb',
                self.segmental_densities[self._density_set]['hand'],
                self._Lb[5],
                self._Lb[6],
                b5h))
        self._b.append( sol.StadiumSolid( 'b6: knuckles',
                self.segmental_densities[self._density_set]['hand'],
                self._Lb[6],
                self._Lb[7],
                b6h))

    def _define_leg_segments(self):
        """Defines the solids (from solid.py) that create the legs of the
        human. This requires the definition of 2D stadium levels using
        the input measurement parameters .

        """
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
        self._Lj = []
        self._j = []
        Lj0p = 2 * np.pi * 0.5 * np.sqrt(np.abs(self._Ls[0].radius *
                                                self._Ls[0].width))
        self._Lj.append( sol.Stadium('Lj0: hip joint centre',
                                    'perimeter', Lj0p, '=p'))
        self._Lj.append( sol.Stadium('Lj1: crotch',
                                    'perimeter', meas['Lj1p'], '=p'))
        self._Lj.append( sol.Stadium('Lj2: mid-thigh',
                                    'perimeter', meas['Lj2p'], '=p'))
        self._Lj.append( sol.Stadium('Lj3: knee joint centre',
                                    'perimeter', meas['Lj3p'], '=p'))
        self._Lj.append( sol.Stadium('Lj4: maximum calf perimeter',
                                    'perimeter', meas['Lj4p'], '=p'))
        self._Lj.append( sol.Stadium('Lj5: ankle joint centre',
                                    'perimeter', meas['Lj5p'], '=p'))
        self._Lj.append( sol.Stadium('Lj6: heel',
                                    'perimwidth', meas['Lj6p'], meas['Lj6d'],
                                    'AP'))
        self._Lj.append( sol.Stadium('Lj7: arch',
                                    'perimeter', meas['Lj7p'], '=p'))
        self._Lj.append( sol.Stadium('Lj8: ball',
                                    'perimwidth', meas['Lj8p'], meas['Lj8w']))
        self._Lj.append( sol.Stadium('Lj9: toe nails',
                                    'perimwidth', meas['Lj9p'], meas['Lj9w']))
        # define left leg solids
        self._j.append( sol.StadiumSolid( 'j0: hip joint centre',
                self.segmental_densities[self._density_set]['thigh'],
                self._Lj[0],
                self._Lj[1],
                j0h))
        self._j.append( sol.StadiumSolid( 'j1: crotch',
                self.segmental_densities[self._density_set]['thigh'],
                self._Lj[1],
                self._Lj[2],
                j1h))
        self._j.append( sol.StadiumSolid( 'j2: mid-thigh',
                self.segmental_densities[self._density_set]['thigh'],
                self._Lj[2],
                self._Lj[3],
                j2h))
        self._j.append( sol.StadiumSolid( 'j3: knee joint centre',
                self.segmental_densities[self._density_set]['lower-leg'],
                self._Lj[3],
                self._Lj[4],
                j3h))
        self._j.append( sol.StadiumSolid( 'j4: maximum calf parimeter',
                self.segmental_densities[self._density_set]['lower-leg'],
                self._Lj[4],
                self._Lj[5],
                j4h))
        self._j.append( sol.StadiumSolid( 'j5: ankle joint centre',
                self.segmental_densities[self._density_set]['foot'],
                self._Lj[5],
                self._Lj[6],
                j5h))
        self._j.append( sol.StadiumSolid( 'j6: heel',
                self.segmental_densities[self._density_set]['foot'],
                self._Lj[6],
                self._Lj[7],
                j6h))
        self._j.append( sol.StadiumSolid( 'j7: arch',
                self.segmental_densities[self._density_set]['foot'],
                self._Lj[7],
                self._Lj[8],
                j7h))
        self._j.append( sol.StadiumSolid( 'k8: ball',
                self.segmental_densities[self._density_set]['foot'],
                self._Lj[8],
                self._Lj[9],
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
        self._Lk = []
        self._k = []
        Lk0p = 2 * np.pi * 0.5 * np.sqrt(np.abs(self._Ls[0].radius *
                                                self._Ls[0].width))
        self._Lk.append( sol.Stadium('Lk0: hip joint centre',
                                    'perimeter', Lk0p, '=p'))
        self._Lk.append( sol.Stadium('Lk1: crotch',
                                    'perimeter', meas['Lk1p'], '=p'))
        self._Lk.append( sol.Stadium('Lk2: mid-thigh',
                                    'perimeter', meas['Lk2p'], '=p'))
        self._Lk.append( sol.Stadium('Lk3: knee joint centre',
                                    'perimeter', meas['Lk3p'], '=p'))
        self._Lk.append( sol.Stadium('Lk4: maximum calf perimeter',
                                    'perimeter', meas['Lk4p'], '=p'))
        self._Lk.append( sol.Stadium('Lk5: ankle joint centre',
                                    'perimeter', meas['Lk5p'], '=p'))
        self._Lk.append( sol.Stadium('Lk6: heel',
                                    'perimwidth', meas['Lk6p'], meas['Lk6d'],
                                    'AP'))
        self._Lk.append( sol.Stadium('Lk7: arch',
                                    'perimeter', meas['Lk7p'], '=p'))
        self._Lk.append( sol.Stadium('Lk8: ball',
                                    'perimwidth', meas['Lk8p'], meas['Lk8w']))
        self._Lk.append( sol.Stadium('Lk9: toe nails',
                                    'perimwidth', meas['Lk9p'], meas['Lk9w']))
        self._k.append( sol.StadiumSolid( 'k0: hip joint centre',
                self.segmental_densities[self._density_set]['thigh'],
                self._Lk[0],
                self._Lk[1],
                k0h))
        self._k.append( sol.StadiumSolid( 'k1: crotch',
                self.segmental_densities[self._density_set]['thigh'],
                self._Lk[1],
                self._Lk[2],
                k1h))
        self._k.append( sol.StadiumSolid( 'k2: mid-thigh',
                self.segmental_densities[self._density_set]['thigh'],
                self._Lk[2],
                self._Lk[3],
                k2h))
        self._k.append( sol.StadiumSolid( 'k3: knee joint centre',
                self.segmental_densities[self._density_set]['lower-leg'],
                self._Lk[3],
                self._Lk[4],
                k3h))
        self._k.append( sol.StadiumSolid( 'k4: maximum calf perimeter',
                self.segmental_densities[self._density_set]['lower-leg'],
                self._Lk[4],
                self._Lk[5],
                k4h))
        self._k.append( sol.StadiumSolid( 'k5: ankle joint centre',
                self.segmental_densities[self._density_set]['foot'],
                self._Lk[5],
                self._Lk[6],
                k5h))
        self._k.append( sol.StadiumSolid( 'k6: heel',
                self.segmental_densities[self._density_set]['foot'],
                self._Lk[6],
                self._Lk[7],
                k6h))
        self._k.append( sol.StadiumSolid( 'k7: arch',
                self.segmental_densities[self._density_set]['foot'],
                self._Lk[7],
                self._Lk[8],
                k7h))
        self._k.append( sol.StadiumSolid( 'k8: ball',
                self.segmental_densities[self._density_set]['foot'],
                self._Lk[8],
                self._Lk[9],
                k8h))

    def _define_segments(self):
        """Define segment objects using previously defined solids.
        This is where the definition of segment position and rotation really
        happens. There are 9 segments. Each segment has a base, located
        at a joint, and an orientation given by the input joint angle
        parameters.

        """
        # define all segments
        # pelvis
        Ppos = self.coord_sys_pos
        PRotMat = (self.coord_sys_orient *
                   inertia.euler_123([self.CFG['somersalt'],
                                    self.CFG['tilt'],
                                    self.CFG['twist']]))
        self.P = seg.Segment( 'P: Pelvis', Ppos, PRotMat,
                              [self._s[0],self._s[1]] , (1,0,0))
        # thorax
        Tpos = self._s[1].endpos
        TRotMat = self._s[1].rot_mat * inertia.rotate_space_123(
                                    [self.CFG['PTsagittalFlexion'],
                                     self.CFG['PTfrontalFlexion'],0])
        self.T = seg.Segment( 'T: Thorax', Tpos, TRotMat,
                              [self._s[2]], (1,.5,0))
        # chest-head
        Cpos = self._s[2].endpos
        CRotMat = self._s[2].rot_mat * inertia.rotate_space_123(
                                    [0,
                                     self.CFG['TClateralSpinalFlexion'],
                                     self.CFG['TCspinalTorsion']])
        self.C = seg.Segment( 'C: Chest-head', Cpos, CRotMat,
                              [self._s[3],self._s[4],self._s[5],self._s[6],
                               self._s[7]], (1,1,0))
        # left upper arm
        dpos = np.array([[self._s[3].stads[1].width/2],[0.0],
                         [self._s[3].height]])
        A1pos = self._s[3].pos + self._s[3].rot_mat * dpos
        A1RotMat = self._s[3].rot_mat * (inertia.rotate_space_123(
                                       [0,-np.pi,0]) *
                                          inertia.euler_123(
                                          [self.CFG['CA1elevation'],
                                          -self.CFG['CA1abduction'],
                                          -self.CFG['CA1rotation']]))
        self.A1 = seg.Segment( 'A1: Left upper arm', A1pos, A1RotMat,
                               [self._a[0],self._a[1]] , (0,1,0))
        # left forearm-hand
        A2pos = self._a[1].endpos
        A2RotMat = self._a[1].rot_mat * inertia.rotate_space_123(
                                     [self.CFG['A1A2flexion'],0,0])
        self.A2 = seg.Segment( 'A2: Left forearm-hand', A2pos, A2RotMat,
                               [self._a[2],self._a[3],self._a[4],self._a[5],
                                self._a[6]], (1,0,0))
        # right upper arm
        dpos = np.array([[-self._s[3].stads[1].width/2],[0.0],
                         [self._s[3].height]])
        B1pos = self._s[3].pos + self._s[3].rot_mat * dpos
        B1RotMat = self._s[3].rot_mat * (inertia.rotate_space_123(
                                       [0,-np.pi,0]) *
                                           inertia.euler_123(
                                           [self.CFG['CB1elevation'],
                                           self.CFG['CB1abduction'],
                                           self.CFG['CB1rotation']]))
        self.B1 = seg.Segment( 'B1: Right upper arm', B1pos, B1RotMat,
                               [self._b[0],self._b[1]], (0,1,0))
        # right forearm-hand
        B2pos = self._b[1].endpos
        B2RotMat = self._b[1].rot_mat * inertia.rotate_space_123(
                                     [self.CFG['B1B2flexion'],0,0])
        self.B2 = seg.Segment( 'B2: Right forearm-hand', B2pos, B2RotMat,
                               [self._b[2],self._b[3],self._b[4],self._b[5],
                                self._b[6]], (1,0,0))
        # left thigh
        dpos = np.array([[.5*self._s[0].stads[0].thickness+
                          .5*self._s[0].stads[0].radius],[0.0],[0.0]])
        J1pos = self._s[0].pos + self._s[0].rot_mat * dpos
        J1RotMat = self._s[0].rot_mat * (inertia.rotate_space_123(
                                       np.array([0,np.pi,0])) *
                                          inertia.rotate_space_123(
                                          [self.CFG['PJ1flexion'],
                                           -self.CFG['PJ1abduction'],0]))
        self.J1 = seg.Segment( 'J1: Left thigh', J1pos, J1RotMat,
                               [self._j[0],self._j[1],self._j[2]], (0,1,0))
        # left shank-foot
        J2pos = self._j[2].endpos
        J2RotMat = self._j[2].rot_mat * inertia.rotate_space_123(
                                     [-self.CFG['J1J2flexion'],0,0])
        self.J2 = seg.Segment( 'J2: Left shank-foot', J2pos, J2RotMat,
                               [self._j[3],self._j[4],self._j[5],self._j[6],
                                self._j[7],self._j[8]], (1,0,0))
        # right thigh
        dpos = np.array([[-.5*self._s[0].stads[0].thickness-
                           .5*self._s[0].stads[0].radius],[0.0],[0.0]])
        K1pos = self._s[0].pos + self._s[0].rot_mat * dpos
        K1RotMat = self._s[0].rot_mat * (inertia.rotate_space_123(
                                       np.array([0,np.pi,0])) *
                                       inertia.rotate_space_123(
                                          [self.CFG['PK1flexion'],
                                           self.CFG['PK1abduction'],0]))
        self.K1 = seg.Segment( 'K1: Right thigh', K1pos, K1RotMat,
                               [self._k[0],self._k[1],self._k[2]], (0,1,0))
        # right shank-foot
        K2pos = self._k[2].endpos
        K2RotMat = self._k[2].rot_mat * inertia.rotate_space_123(
                                      [-self.CFG['K1K2flexion'],0,0])
        self.K2 = seg.Segment( 'K2: Right shank-foot', K2pos, K2RotMat,
                               [self._k[3],self._k[4],self._k[5],self._k[6],
                                self._k[7],self._k[8]], (1,0,0))

    def scale_human_by_mass(self, measmass):
        """Takes a measured mass and scales all densities by that mass so that
        the mass of the human is the same as the mesaured mass. Mass must be
        in units of kilograms to be consistent with the densities used.

        Parameters
        ----------
        measmass : float
            Measured mass of the human in kilograms.

        """
        massratio = measmass / self.mass
        # The following attempts to take care of the unlikely case where the
        # density set is changed after construction of a Human.
        for key, val in self.segmental_densities.items():
            for segment, density in val.items():
                self.segmental_densities[key][segment] = density * massratio
        self.update()
        if round(measmass, 2) != round(self.mass, 2):
            raise Exception("Attempted to scale mass by a "
                  "measured mass, but did not succeed. "
                  "Measured mass:", round(measmass,
                          2),"self.mass:",round(self.mass, 2))

    def _read_measurements(self, fname):
        """Reads a measurement input .txt file, in YAML format,  and assigns
        the measurements to fields in the self.meas dict. This method is called
        by the constructor.

        Parameters
        ----------
        fname : str
            Filename or path to measurement file.

        """
        # initialize measurement conversion factor
        self.measurementconversionfactor = 0
        # open measurement file
        fid = open(fname, 'r')
        mydict = yaml.load(fid.read())
        fid.close()
        # loop until all 95 parameters are read in
        for key, val in mydict.items():
            if key == 'measurementconversionfactor':
                self.measurementconversionfactor = val
            elif key == 'totalmass':
                # scale densities
                self.meas_mass = val
            else:
                # If inappropriate value.
                if val == None or val <= 0:
                    raise ValueError("Variable {0} has inappropriate "
                            "value.".format( key))
                # If key is unexpected.
                if key not in self.measnames:
                    raise ValueError("Variable {0} is not valid name for a "
                        "measurement.".format(key))
                self.meas[key] = float(val)
        if len(self.meas) != len(self.measnames):
            raise Exception("There should be {0} measurements, but {1} were "
                    "found.".format(len(self.measnames), len(self.meas)))
        if self.measurementconversionfactor == 0:
            raise Exception("Variable measurementconversionfactor not "
                    "provided or is 0. Set as 1 if measurements are given "
                    "in meters.")
        # multiply all values by conversion factor
        for key, val in self.meas.items():
            self.meas[key] = val * self.measurementconversionfactor

    def write_measurements(self, fname):
        """Writes the keys and values of the self.meas dict to a text file.
        Units of measurements is meters.

        Parameters
        ----------
        fname : str
            Filename or path to measurement output .txt file.

        """
        # Need to make sure we don't modify self.meas: make shallow copy.
        mydict = copy.copy(self.meas)
        # Add total mass.
        mydict['totalmass'] = self.meas_mass
        # Add measurement conversion factor.
        mydict['measurementconversionfactor'] = 1
        fid = open(fname, 'w')
        yaml.dump(mydict, fid, default_flow_style=False)
        fid.close()

    def write_meas_for_ISEG(self, fname):
        """Writes the values of the self.meas dict to a .txt file that is
        formidable as input to Yeadon's ISEG fortran code that performs
        similar calculations to this package. ISEG is published in Yeadon's
        dissertation.

        Parameters
        ----------
        fname : str
            Filename or path for ISEG .txt input file.

        """
        fid = open(fname,'w')
        n = self.meas
        m = copy.copy(self.meas)

        # Convert units.
        SI = 1./1000.
        for key, val in m.items(): m[key] = val/SI

        # pelvis, torso, chest-head
        fid.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(m['Ls1L'],
            m['Ls2L'], m['Ls3L'], m['Ls4L'], m['Ls5L'], m['Ls6L'], m['Ls7L'],
            m['Ls8L']))
        fid.write("{0},{1},{2},{3},{4},{5},{6}\n".format(m['Ls0p'], m['Ls1p'],
            m['Ls2p'], m['Ls3p'], m['Ls5p'], m['Ls6p'], m['Ls7p']))
        fid.write("{0},{1},{2},{3},{4},{5}\n".format(m['Ls0w'], m['Ls1w'],
            m['Ls2w'], m['Ls3w'], m['Ls4w'], m['Ls4d']))

        # arms
        fid.write("{0},{1},{2},{3},{4},{5}\n".format(m['La2L'], m['La3L'],
            m['La4L'], m['La5L'], m['La6L'], m['La7L']))
        fid.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(m['La0p'],
            m['La1p'], m['La2p'], m['La3p'], m['La4p'], m['La5p'], m['La6p'],
            m['La7p']))
        fid.write("{0},{1},{2},{3}\n".format(m['La4w'], m['La5w'], m['La6w'],
            m['La7w']))
        fid.write("{0},{1},{2},{3},{4},{5}\n".format(m['Lb2L'], m['Lb3L'],
            m['Lb4L'], m['Lb5L'], m['Lb6L'], m['Lb7L']))
        fid.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(m['Lb0p'],
            m['Lb1p'], m['Lb2p'], m['Lb3p'], m['Lb4p'], m['Lb5p'], m['Lb6p'],
            m['Lb7p']))
        fid.write("{0},{1},{2},{3}\n".format(m['Lb4w'], m['Lb5w'], m['Lb6w'],
            m['Lb7w']))

        # legs
        fid.write("{0},{1},{2},{3},{4},{5},{6}\n".format(m['Lj1L'], m['Lj3L'],
            m['Lj4L'], m['Lj5L'], m['Lj6L'], m['Lj8L'], m['Lj9L']))
        fid.write("{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(m['Lj1p'],
            m['Lj2p'], m['Lj3p'], m['Lj4p'], m['Lj5p'], m['Lj6p'], m['Lj7p'],
            m['Lj8p'], m['Lj9p']))
        fid.write("{0},{1},{2}\n".format(m['Lj6d'], m['Lj8w'], m['Lj9w']))
        fid.write("{0},{1},{2},{3},{4},{5},{6}\n".format(m['Lk1L'], m['Lk3L'],
            m['Lk4L'], m['Lk5L'], m['Lk6L'], m['Lk8L'], m['Lk9L']))
        fid.write("{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(m['Lk1p'],
            m['Lk2p'], m['Lk3p'], m['Lk4p'], m['Lk5p'], m['Lk6p'], m['Lk7p'],
            m['Lk8p'], m['Lk9p']))
        fid.write("{0},{1},{2}\n".format(m['Lk6d'], m['Lk8w'], m['Lk9w']))

        # This line contains ISEG's "XHEIGHT" and "XMASS" variables. XMASS is
        # used for mass/density correction in his code.
        fid.write("{0},{1}\n".format(500,
            self.meas_mass if self.meas_mass > 0 else 200))
        fid.close()

    def _read_CFG(self, CFGfname):
        """Reads in a text file that contains the joint angles of the human.
        There is little error-checking for this. Make sure that the input
        is consistent with template input .txt files, or with the output
        from the :py:meth:`yeadon.Human.write_CFG()` method. Text file is
        formatted using YAML syntax.

        Parameters
        ----------
        CFGfname : str
            Filename or path to configuration input .txt file.

        """
        self.CFG = dict()
        with open(CFGfname, 'r') as fid:
            mydict = yaml.load(fid.read())
            for key, val in mydict.items():
                if key not in self.CFGnames:
                    mes = "'{}' is not a correct variable name.".format(key)
                    raise StandardError(mes)
                if val == None:
                    raise StandardError(
                            "Variable {0} has no value.".format(key))
                self.CFG[key] = float(val)
            fid.close()

        if len(self.CFG) != len(self.CFGnames):
            raise StandardError("Number of CFG variables, {0}, is "
                    "incorrect.".format(len(self.CFG)))

    def write_CFG(self, CFGfname):
        """Writes the keys and values of the self.CFG dict to a .txt file.
        Text file is formatted using YAML syntax.

        Parameters
        ----------
        CFGfname : str
            Filename or path to configuration output .txt file

        """
        fid = open(CFGfname, 'w')
        yaml.dump(self.CFG, fid, default_flow_style=False)
        fid.close()


