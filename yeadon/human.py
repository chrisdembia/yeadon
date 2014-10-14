"""The human module defines the Human class, which is composed of Segment's.
The Human class has methods to define the constituent segments from inputs,
calculates their properties, and manages file input/output.

"""

# Use Python3 integer division rules.
from __future__ import division
import copy
import warnings

import numpy as np
import yaml
try:
    from mayavi import mlab
except ImportError:
    pass

import inertia
import solid as sol
import segment as seg
from .utils import printoptions
from exceptions import YeadonDeprecationWarning

# Display our warnings to the user.
warnings.simplefilter('always', YeadonDeprecationWarning)


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

    CFGnames = ('somersault',
                'tilt',
                'twist',
                'PTsagittalFlexion',
                'PTbending',
                'TCspinalTorsion',
                'TCsagittalSpinalFlexion',
                'CA1extension',
                'CA1adduction',
                'CA1rotation',
                'CB1extension',
                'CB1abduction',
                'CB1rotation',
                'A1A2extension',
                'B1B2extension',
                'PJ1extension',
                'PJ1adduction',
                'PK1extension',
                'PK1abduction',
                'J1J2flexion',
                'K1K2flexion')

    CFGbounds = [[-np.pi, np.pi],                   # somersault
                 [-np.pi, np.pi],                   # tilt
                 [-np.pi, np.pi],                   # twist
                 [-np.pi / 2.0, np.pi],             # PTsagittalFlexion
                 [-np.pi / 2.0, np.pi / 2.0],       # PTbending
                 [-np.pi / 2.0, np.pi / 2.0],       # TCspinalTorsion
                 [-np.pi / 2.0, np.pi / 2.0],       # TCsagittalSpinalFlexion
                 [-np.pi, np.pi / 2.0],             # CA1extension
                 [-3.0 * np.pi / 2.0, np.pi / 2.0], # CA1adduction
                 [-np.pi, np.pi],                   # CA1rotation
                 [-np.pi, np.pi / 2.0],             # CB1extension
                 [-np.pi / 2.0, 3.0 * np.pi / 2.0], # CB1abduction
                 [-np.pi, np.pi],                   # CB1rotation
                 [-np.pi, 0.0],                     # A1A2extension
                 [-np.pi, 0.0],                     # B1B2extension
                 [-np.pi, np.pi / 2.0],             # PJ1extension
                 [-np.pi / 2.0, np.pi / 2.0],       # PJ1adduction
                 [-np.pi, np.pi / 2.0],             # PK1extension
                 [-np.pi / 2.0, np.pi / 2.0],       # PK1abduction
                 [0, np.pi],                        # J1J2flexion
                 [0, np.pi]]                        # K1K2flexion

    _deprecated_CFGnames = {
            'somersalt': 'somersault',
            'CA1elevation': 'CA1extension',
            'CB1elevation': 'CB1extension',
            'CA1abduction': 'CA1adduction',
            'A1A2flexion': 'A1A2extension',
            'B1B2flexion': 'B1B2extension',
            'TClateralSpinalFlexion': 'TCsagittalSpinalFlexion',
            'PJ1flexion': 'PJ1extension',
            'PK1flexion': 'PK1extension',
            'PJ1abduction': 'PJ1adduction',
            'PTfrontalFlexion': 'PTbending',
            }

    @property
    def mass(self):
        """Mass of the human, in units of kg."""
        return self._mass

    @property
    def center_of_mass(self):
        """Center of mass of the human, a np.ndarray, in units of m, expressed
        the global frame, from the bottom center of the pelvis (center of the
        Ls0 stadium)."""
        return self._center_of_mass

    @property
    def inertia(self):
        """Inertia matrix/dyadic of the human, a np.matrix, in units of
        kg-m^2, about the center of mass of the human, expressed in the global
        frame.  """
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
            stadium solids and a semi-ellipsoid with which to define the
            model's geometry. See online documentation on how to take the
            measurements.  If its type is str, it is the path to a measurements
            input file.  See the template .txt file for example input. If its
            type is a dict, it is a dictionary with keys that are the names of
            the variables in the text file. In this latter case, units must be
            in meters and a measured mass override cannot be provided.
        CFG : str or dict, optional
            The configuration of the human (radians). If its type is str, it is
            the path to a CFG input file in YAML syntax (see template
            CFGtemplate.txt). If its type is dict, it must have an entry for
            each of the 21 names in Human.CFGnames or in the template. If not
            provided, the human is in a default configuration in which all
            joint angles are set to zero.
        symmetric : bool, optional
            True by default. Decides whether or not to average the measurements
            of the left and right limbs of the human. This has nothing to with
            the configuration being symmetric.
        density_set : str, optional
            Selects a set of densities to use for the body segments. Either
            'Chandler', 'Clauser', or 'Dempster'. 'Dempster' is the default.
            See class attribute `segmental_densities` to inspect their values.

        """
        # Initialize position and orientation of entire body.
        self._coord_sys_pos = np.array([[0],[0],[0]])
        self._coord_sys_orient = inertia.rotate_space_123((0,0,0))

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

    def update(self):
        """Redefines all solids and then calls yeadon.Human._update_segments.
        Called by the method yeadon.Human.scale_human_by_mass. The method is
        to be used in instances in which measurements change.

        """
        self._define_torso_solids()
        self._define_arm_solids()
        self._define_leg_solids()
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
        self.segments = [self.P, self.T, self.C,
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
        # TODO: Should this actually be errors? There probably isn't any reason
        # to bound these, but there could be reason to avoid the singularities
        # in the direction cosine matrices for each joint rotation.
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
        leftidxs = np.concatenate((np.arange(21, 39), np.arange(57, 76)), 1)
        rightidx = np.concatenate((np.arange(39, 57), np.arange(76, 95)), 1)
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
        if varname in self._deprecated_CFGnames:
            msg = ("'{0}' should be called '{1}'."
                   " This will raise an error in future versions.".format(
                       varname, self._deprecated_CFGnames[varname]))
            warnings.warn(msg, YeadonDeprecationWarning)
            varname = self._deprecated_CFGnames[varname]
        elif varname not in self.CFGnames:
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

        Parameters
        ----------
        CFG : dict
            Stores the 21 joint angles.

        """
        for depr_name, new_name in self._deprecated_CFGnames.items():
            if depr_name in CFG:
                msg = ("'{0}' should be called '{1}'."
                       " This will raise an error in future versions.".format(
                           depr_name, new_name))
                warnings.warn(msg, YeadonDeprecationWarning)
                value = CFG.pop(depr_name)
                CFG[new_name] = value

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
            dist = self.center_of_mass - s.center_of_mass
            self._inertia += np.mat(
                inertia.parallel_axis(s.inertia,
                                      s.mass,
                                      [dist[0,0],dist[1,0],dist[2,0]]))

    def __str__(self):
        return(self._properties_string())

    def print_properties(self, precision=5, suppress=True):
        """Prints human mass, center of mass, and inertia.

        Parameters
        ----------
        precision : integer, default=5
            The precision for floating point representation.
        suppress : boolean, default=True
            Print very small values as 0 instead of scientific notation.

        Notes
        -----
        See numpy.set_printoptions for more details on the optional
        arguments.

        """
        print(self._properties_string(precision=precision, suppress=suppress))

    def _properties_string(self, precision=5, suppress=True):
        """Prints human mass, center of mass, and inertia.

        Parameters
        ----------
        precision : integer, default=5
            The precision for floating point representation.
        suppress : boolean, default=True
            Print very small values as 0 instead of scientific notation.

        Notes
        -----
        See numpy.set_printoptions for more details on the optional
        arguments.

        """
        template = \
"""\
Mass (kg):

{mass:1.{precision}f}

COM in global frame from bottom center of pelvis (Ls0) (m):

{center_of_mass}

Inertia tensor in global frame about human's COM (kg-m^2):

{inertia}
"""

        with printoptions(precision=precision, suppress=suppress):
            return template.format(mass=self.mass,
                                  precision=precision,
                                  center_of_mass=self.center_of_mass,
                                  inertia=self.inertia)

    def _translate_coord_sys(self, vec):
        """Moves the cooridinate system from the center of the bottom of the
        human's pelvis to a location defined by the input to this method.
        Note that if this method is used along with
        yeadon.Human.rotate_coord_sys, the vector components for the inputs
        to this function are in the new coordinate frame defined by the input
        to yeadon.Human.rotate_coord_sys (rather than in the original frame
        of the yeadon module).

        CAUTION: THIS METHOD IS UNTESTED.

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
        self._coord_sys_pos = newpos
        self._update_segments()

    def _rotate_coord_sys(self, varin):
        """Rotates the coordinate system. For list or tuple input, the order of
        the rotations is x, then, y, then z.

        CAUTION: THIS METHOD IS UNTESTED.

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
        self._coord_sys_orient = rotmat
        self._update_segments()

    def _transform_coord_sys(self, vec, rotmat):
        """Calls both yeadon.Human.translate_coord_sys and
        yeadon.Human.rotate_coord_sys.

        CAUTION: THIS METHOD IS UNTESTED.

        Parameters
        ----------
        vec : list or tuple (3,)
            See yeadon.Human.translate_coord_sys
        rotmat

        """
        self.translate_coord_sys(vec)
        self.rotate_coord_sys(rotmat)

    def inertia_transformed(self, pos=None, rotmat=None):
        """Returns an inertia tensor of the human with respect to the
        position provided in `pos` and a new frame that is defined by
        rotation relative to the global frame with the direction cosine
        matrix `rotmat`. The position is to be provided from the origin of
        the global frame, which is at the center of the Ls0 stadium (bottom
        of pelvis), and its components are expressed in the basis of the
        global frame. This method does NOT alter any attributes of the Human
        (it is 'const').

        Parameters
        ----------
        pos : array_like, (3,), (1, 3), or (3, 1), optional
            Position vector from the origin (center of Ls0) to the point
            about which the user desires the inertia tensor. This position
            vector must be expressed in the global reference frame. If not
            provided, the tensor is given about the center of mass of the
            human.
        rotmat : np.matrix (3,3), optional
            If not provided, the returned tensor is expressed in the global
            frame, else the returned tensor is expressed in the rotated
            reference frame. Consider N to be the global frame and B to be
            the frame in which the user desires the inertia tensor. Then
            `rotmat` is the rotation matrix that converts a vector expressed
            in the basis B to a vector expressed in the basis N (i.e. vN =
            rotmat * vB). That is, the columns of `rotmat` are the unit
            vectors b_x, b_y, and b_z, each expressed in the basis given by
            the unit vectors n_x, n_y, n_z.

        Returns
        -------
        transformed : np.matrix (3,3)
            If B is the frame in which the user desires the inertia tensor,
            this method returns ^{B}I^{H/P}, where P is the point specified
            by `pos`, and H is the human system.

        Notes
        -----
        If N is the global frame, B is the frame in which the user desires
        the inertia tensor, then `rotmat` = ^{N}R^{B}.

        """
        # Shifting the inertia must happen first, because the position the
        # user provides is in the global frame.

        if pos is not None:
            pos = np.asmatrix(pos).reshape((3, 1))
            transformed = inertia.parallel_axis(self.inertia, self.mass, pos
                                                - self.center_of_mass)
        else:
            transformed = self.inertia.copy()

        if rotmat is not None:
            transformed = inertia.rotate_inertia(rotmat, transformed)

        return transformed

    def combine_inertia(self, objlist):
        """Returns the inertia properties of a combination of solids
        and/or segments of the human, using the fixed human frame (or the
        modified fixed frame as given by the user). Be careful with inputs:
        do not specify a solid that is part of a segment that you have also
        specified. This method does not assign anything to any object
        attributes (it is 'const'), it simply returns the desired quantities.

        See documentation for description of the global frame.

        Parameters
        ----------
        objlist : tuple
            Tuple of strings that identify a solid or segment. The
            strings can be any of the following:

            * solids: 's0' through 's7', 'a0' through 'a6', 'b0' through 'b6',
              'j0' through 'j8', 'k0' through 'k8'
            * segments: 'P', 'T', 'C', 'A1', 'A2', 'B1', 'B2', 'J1', 'J2',
              'K1', 'K2'

        Returns
        -------
        combined_mass : float
            Sum of the masses of the input solids and/or segments.
        combined_COM : np.array (3,1)
            Position of the center of mass of the input solids and/or segments,
            expressed in the global frame .
        combined_inertia : np.matrix (3,3)
            Inertia tensor about the combined_COM, expressed in the global frame.

        """
        if objlist == []:
            raise Exception("Empty input.")
        # Preparing.
        solidkeys = [
                's0','s1','s2','s3','s4','s5','s6','s7',
                'a0','a1','a2','a3','a4','a5','a6',
                'b0','b1','b2','b3','b4','b5','b6',
                'j0','j1','j2','j3','j4','j5','j6','j7','j8',
                'k0','k1','k2','k3','k4','k5','k6','k7','k8',]
        segmentkeys = ['P','T','C','A1','A2','B1','B2','J1','J2','K1','K2']
        solidvals = self._s + self._a_solids + self._b_solids + self._j_solids + self._k_solids
        ObjDict = dict(zip(solidkeys + segmentkeys, solidvals + self.segments))

        # Error-check.
        for key in (solidkeys + segmentkeys):
            if objlist.count(key) > 1:
                raise Exception("An object is listed more than once. "
                        "A solid/segment can only be listed once.")
        for segkey in segmentkeys:
            if objlist.count(segkey) == 1:
                # this segment is listed as input
                for solobj in objlist:
                    for segsol in ObjDict[segkey].solids:
                        if solobj == segsol.label[0:2]:
                            raise Exception("A solid {0} and its parent "
                                    "segment {1} have both been given "
                                    "as inputs. This duplicates that solid's "
                                    "contribution.".format(solobj, segkey))

        # Perform computations.
        combined_mass = 0.0
        combinedMoment = np.zeros( (3,1) )
        for objstr in objlist:
            if ObjDict.has_key(objstr) == False:
                raise Exception("The string {0!r} does not identify a segment "
                      "or solid of the human.".format(objstr))
            obj = ObjDict[objstr]
            combined_mass += obj.mass
            combinedMoment += obj.mass * obj.center_of_mass
        combined_COM = combinedMoment / combined_mass
        combined_inertia = np.mat(np.zeros( (3,3) ))
        # Move inertia tensor of an object from the point it is currently about
        # (the object's COM) so that it is about combined_COM.
        for objstr in objlist:
            obj = ObjDict[objstr]
            dist = combined_COM - obj.center_of_mass
            combined_inertia += np.mat(inertia.parallel_axis(
                                       obj.inertia,
                                       obj.mass,
                                       [dist[0,0],dist[1,0],dist[2,0]]))
        return combined_mass, combined_COM, combined_inertia

    def get_segment_by_name(self, name):
        """Returns a segment given its name."""
        labels = [s.label[0:len(name)] for s in self.segments]
        return self.segments[labels.index(name)]

    def draw(self, mlabobj=None, gui=False):
        """Draws the human in 3D in a new window using MayaVi.
        The mouse can be used to control or explore the 3D view.

        Parameters
        ----------
        mlabobj : mayavi.mlab, optional, default=None
            A mayavi mlab object. If None a new one will be created.
        gui: boolean, optional, default=False
            If false the mlab.show() command will be called and the scene
            will be displayed to the screen.

        """
        def make_drawing(mlabobj):
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

        if mlabobj is None:
            try:
                mlabobj = mlab
            except NameError:
                raise('MayaVi is not installed, this method is not available.')
            else:
                make_drawing(mlabobj)
        else:
            make_drawing(mlabobj)

        if gui == False:
            mlabobj.show()

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

    def _draw_mayavi_mass_center_sphere(self, mlabobj):
        """Draws a sphere representing the mass center of the human."""
        x, y, z = self.center_of_mass.flatten()
        # 75 kg person has a 0.1 m diameter sphere
        size = self.mass / 75.0 * 0.1
        self._mass_center_sphere = mlabobj.points3d(x, y, z, size,
                                                    scale_factor=1.0)

    def _update_mayavi_mass_center_sphere(self):
        x, y, z = self.center_of_mass.flatten()
        self._mass_center_sphere.mlab_source.set(x=x, y=y, z=z)

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
                                    'perimeter',meas['Ls5p'], ''))
        self._Ls.append( sol.Stadium('Ls6: beneath nose',
                                    'perimeter', meas['Ls6p'], ''))
        self._Ls.append( sol.Stadium('Ls7: above ear',
                                    'perimeter', meas['Ls7p'], ''))
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

        arm_solid_density_sets = ['upper-arm',
                                  'upper-arm',
                                  'forearm',
                                  'forearm',
                                  'hand',
                                  'hand',
                                  'hand']

        # get solid heights from length measurements
        left_arm_solid_heights = [
            meas['La2L'] * 0.5,
            meas['La2L'] - meas['La2L'] * 0.5,
            meas['La3L'] - meas['La2L'],
            meas['La4L'] - meas['La3L'],
            meas['La5L'],
            meas['La6L'] - meas['La5L'],
            meas['La7L'] - meas['La6L']]

        # left arm
        self._La = []
        self._La.append( sol.Stadium('La0: shoulder joint centre',
                                    'perimeter', meas['La0p'], ''))
        self._La.append( sol.Stadium('La1: mid-arm',
                                    'perimeter', meas['La1p'], ''))
        self._La.append( sol.Stadium('La2: elbow joint centre',
                                    'perimeter', meas['La2p'], ''))
        self._La.append( sol.Stadium('La3: maximum forearm perimeter',
                                    'perimeter', meas['La3p'], ''))
        self._La.append( sol.Stadium('La4: wrist joint centre',
                                    'perimwidth', meas['La4p'], meas['La4w']))
        self._La.append( sol.Stadium('La5: base of thumb',
                                    'perimwidth', meas['La5p'], meas['La5w']))
        self._La.append( sol.Stadium('La6: knuckles',
                                    'perimwidth', meas['La6p'], meas['La6w']))
        self._La.append( sol.Stadium('La7: fingernails',
                                    'perimwidth', meas['La7p'], meas['La7w']))
        # define left arm solids
        left_arm_solid_tags = ['a0: shoulder joint centre',
                               'a1: mid-arm',
                               'a2: elbow joint centre',
                               'a3: maximum forearm perimeter',
                               'a4: wrist joint centre',
                               'a5: base of thumb',
                               'a6: knuckles']

        # build the list of stadium solids starting at the shoulder going down
        # to the arm
        self._a_solids = []
        for i, (tag, density_set, height) in enumerate(
                zip(left_arm_solid_tags, arm_solid_density_sets,
                    left_arm_solid_heights)):

            self._a_solids.append(sol.StadiumSolid(tag,
                    self.segmental_densities[self._density_set][density_set],
                    self._La[i + 1], #1, 2, 3, 4, 5, 6, 7
                    self._La[i], #0, 1, 2, 3, 4, 5, 6
                    height))

        # get solid heights from length measurements
        right_arm_solid_heights = [
            meas['Lb2L'] * 0.5,
            meas['Lb2L'] - meas['Lb2L'] * 0.5,
            meas['Lb3L'] - meas['Lb2L'],
            meas['Lb4L'] - meas['Lb3L'],
            meas['Lb5L'],
            meas['Lb6L'] - meas['Lb5L'],
            meas['Lb7L'] - meas['Lb6L']]

        # right arm
        self._Lb = []
        self._Lb.append( sol.Stadium('Lb0: shoulder joint centre',
                                    'perimeter', meas['Lb0p'], ''))
        self._Lb.append( sol.Stadium('Lb1: mid-arm',
                                    'perimeter', meas['Lb1p'], ''))
        self._Lb.append( sol.Stadium('Lb2: elbow joint centre',
                                    'perimeter', meas['Lb2p'], ''))
        self._Lb.append( sol.Stadium('Lb3: maximum forearm perimeter',
                                    'perimeter', meas['Lb3p'], ''))
        self._Lb.append( sol.Stadium('Lb4: wrist joint centre',
                                    'perimwidth', meas['Lb4p'], meas['Lb4w']))
        self._Lb.append( sol.Stadium('Lb5: base of thumb',
                                    'perimwidth', meas['Lb5p'], meas['Lb5w']))
        self._Lb.append( sol.Stadium('Lb6: knuckles',
                                    'perimwidth', meas['Lb6p'], meas['Lb6w']))
        self._Lb.append( sol.Stadium('Lb7: fingernails',
                                    'perimwidth', meas['Lb7p'], meas['Lb7w']))
        # define right arm solids
        right_arm_solid_tags = ['b0: shoulder joint centre',
                                'b1: mid-arm',
                                'b2: elbow joint centre',
                                'b3: maximum forearm perimeter',
                                'b4: wrist joint centre',
                                'b5: base of thumb',
                                'b6: knuckles']

        # build the list of stadium solids starting at the shoulder going down
        # to the arm
        self._b_solids = []
        for i, (tag, density_set, height) in enumerate(
                zip(right_arm_solid_tags, arm_solid_density_sets,
                    right_arm_solid_heights)):

            self._b_solids.append(sol.StadiumSolid(tag,
                    self.segmental_densities[self._density_set][density_set],
                    self._La[i + 1], #1, 2, 3, 4, 5, 6, 7
                    self._La[i], #0, 1, 2, 3, 4, 5, 6
                    height))

    def _define_leg_solids(self):
        """Defines the solids (from solid.py) that create the legs of the
        human. This requires the definition of 2D stadium levels using
        the input measurement parameters .

        """
        meas = self.meas
        # get solid heights from length measurements
        left_leg_solid_heights = [
            meas['Lj1L'],
            (meas['Lj3L'] + meas['Lj1L']) * 0.5 - meas['Lj1L'],
            meas['Lj3L'] - (meas['Lj3L'] + meas['Lj1L']) * 0.5,
            meas['Lj4L'] - meas['Lj3L'],
            meas['Lj5L'] - meas['Lj4L'],
            meas['Lj6L'],
            (meas['Lj8L'] + meas['Lj6L']) * 0.5 - meas['Lj6L'],
            meas['Lj8L'] - (meas['Lj8L'] + meas['Lj6L']) * 0.5,
            meas['Lj9L'] - meas['Lj8L']]
        # left leg
        self._Lj = []
        Lj0p = 2 * np.pi * 0.5 * np.sqrt(np.abs(self._Ls[0].radius *
                                                self._Ls[0].width))
        self._Lj.append( sol.Stadium('Lj0: hip joint centre',
                                    'perimeter', Lj0p, ''))
        self._Lj.append( sol.Stadium('Lj1: crotch',
                                    'perimeter', meas['Lj1p'], ''))
        self._Lj.append( sol.Stadium('Lj2: mid-thigh',
                                    'perimeter', meas['Lj2p'], ''))
        self._Lj.append( sol.Stadium('Lj3: knee joint centre',
                                    'perimeter', meas['Lj3p'], ''))
        self._Lj.append( sol.Stadium('Lj4: maximum calf perimeter',
                                    'perimeter', meas['Lj4p'], ''))
        self._Lj.append( sol.Stadium('Lj5: ankle joint centre',
                                    'perimeter', meas['Lj5p'], ''))
        self._Lj.append( sol.Stadium('Lj6: heel',
                                    'perimwidth', meas['Lj6p'], meas['Lj6d'],
                                    'AP'))
        self._Lj.append( sol.Stadium('Lj7: arch',
                                    'perimeter', meas['Lj7p'], ''))
        self._Lj.append( sol.Stadium('Lj8: ball',
                                    'perimwidth', meas['Lj8p'], meas['Lj8w']))
        self._Lj.append( sol.Stadium('Lj9: toe nails',
                                    'perimwidth', meas['Lj9p'], meas['Lj9w']))
        # define left leg solids

        leg_solid_density_sets = ['thigh',
                'thigh',
                'thigh',
                'lower-leg',
                'lower-leg',
                'foot',
                'foot',
                'foot',
                'foot']

        left_leg_solid_tags = [
            'j0: hip joint centre',
            'j1: crotch',
            'j2: mid-thigh',
            'j3: knee joint centre',
            'j4: maximum calf perimeter',
            'j5: ankle joint centre',
            'j6: heel',
            'j7: arch',
            'j8: ball']

        # build the list of stadium solids starting at the shoulder going down
        # to the arm
        self._j_solids = []
        for i, (tag, density_set, height) in enumerate(
                zip(left_leg_solid_tags, leg_solid_density_sets,
                    left_leg_solid_heights)):

            self._j_solids.append(sol.StadiumSolid(tag,
                    self.segmental_densities[self._density_set][density_set],
                    self._Lj[i + 1], #1, 2, 3, 4, 5, 6, 7, ...
                    self._Lj[i], #0, 1, 2, 3, 4, 5, 6, ...
                    height))

        # right leg

        # get solid heights from length measurements
        right_leg_solid_heights = [
            meas['Lk1L'],
            (meas['Lk3L'] + meas['Lk1L']) * 0.5 - meas['Lk1L'],
            meas['Lk3L'] - (meas['Lk3L'] + meas['Lk1L']) * 0.5,
            meas['Lk4L'] - meas['Lk3L'],
            meas['Lk5L'] - meas['Lk4L'],
            meas['Lk6L'],
            (meas['Lk8L'] + meas['Lk6L']) * 0.5 - meas['Lk6L'],
            meas['Lk8L'] - (meas['Lk8L'] + meas['Lk6L']) * 0.5,
            meas['Lk9L'] - meas['Lk8L']]

        self._Lk = []
        Lk0p = 2 * np.pi * 0.5 * np.sqrt(np.abs(self._Ls[0].radius *
                                                self._Ls[0].width))
        self._Lk.append( sol.Stadium('Lk0: hip joint centre',
                                    'perimeter', Lk0p, ''))
        self._Lk.append( sol.Stadium('Lk1: crotch',
                                    'perimeter', meas['Lk1p'], ''))
        self._Lk.append( sol.Stadium('Lk2: mid-thigh',
                                    'perimeter', meas['Lk2p'], ''))
        self._Lk.append( sol.Stadium('Lk3: knee joint centre',
                                    'perimeter', meas['Lk3p'], ''))
        self._Lk.append( sol.Stadium('Lk4: maximum calf perimeter',
                                    'perimeter', meas['Lk4p'], ''))
        self._Lk.append( sol.Stadium('Lk5: ankle joint centre',
                                    'perimeter', meas['Lk5p'], ''))
        self._Lk.append( sol.Stadium('Lk6: heel',
                                    'perimwidth', meas['Lk6p'], meas['Lk6d'],
                                    'AP'))
        self._Lk.append( sol.Stadium('Lk7: arch',
                                    'perimeter', meas['Lk7p'], ''))
        self._Lk.append( sol.Stadium('Lk8: ball',
                                    'perimwidth', meas['Lk8p'], meas['Lk8w']))
        self._Lk.append( sol.Stadium('Lk9: toe nails',
                                    'perimwidth', meas['Lk9p'], meas['Lk9w']))

        right_leg_solid_tags = [
            'k0: hip joint centre',
            'k1: crotch',
            'k2: mid-thigh',
            'k3: knee joint centre',
            'k4: maximum calf perimeter',
            'k5: ankle joint centre',
            'k6: heel',
            'k7: arch',
            'k8: ball']

        self._k_solids = []
        for i, (tag, density_set, height) in enumerate(
                zip(right_leg_solid_tags, leg_solid_density_sets,
                    right_leg_solid_heights)):

            self._k_solids.append(sol.StadiumSolid(tag,
                    self.segmental_densities[self._density_set][density_set],
                    self._Lk[i + 1], #1, 2, 3, 4, 5, 6, 7, ...
                    self._Lk[i], #0, 1, 2, 3, 4, 5, 6, ...
                    height))

    def _define_segments(self):
        """Define segment objects using previously defined solids.
        This is where the definition of segment position and rotation really
        happens. There are 9 segments. Each segment has a base, located
        at a joint, and an orientation given by the input joint angle
        parameters.

        """

        # pelvis
        Ppos = self._coord_sys_pos
        PRotMat = (self._coord_sys_orient *
            inertia.euler_123([self.CFG['somersault'],
                               self.CFG['tilt'],
                               self.CFG['twist']]))
        self.P = seg.Segment('P: Pelvis',
                              Ppos,
                              PRotMat,
                              [self._s[0], self._s[1]],
                              (1.0, 0.0, 0.0))

        # thorax
        Tpos = self.P.end_pos
        TRotMat = (self.P.rot_mat *
            inertia.euler_123([self.CFG['PTsagittalFlexion'],
                                      self.CFG['PTbending'],
                                      0.0]))
        self.T = seg.Segment('T: Thorax',
                             Tpos,
                             TRotMat,
                             [self._s[2]],
                             (1.0, 0.5, 0.0))

        # chest-head
        Cpos = self.T.end_pos
        CRotMat = (self.T.rot_mat *
            inertia.euler_123([self.CFG['TCsagittalSpinalFlexion'],
                               0.0,
                               self.CFG['TCspinalTorsion']]))
        self.C = seg.Segment('C: Chest-head',
                             Cpos,
                             CRotMat,
                             [self._s[3], self._s[4], self._s[5], self._s[6],
                                self._s[7]],
                             (1.0, 1.0, 0.0))

        # arms

        Ls3_Ls4_solid = self._s[3] # nipple to shoulder
        shoulder_width = Ls3_Ls4_solid.stads[1].width

        # left upper arm
        local_left_shoulder_point = \
                np.array([[shoulder_width / 2.0], [0.0], [Ls3_Ls4_solid.height]])
        A1RotMat = (self.C.rot_mat *
             inertia.euler_123([self.CFG['CA1extension'],
                                self.CFG['CA1adduction'],
                                self.CFG['CA1rotation']]))
        A1pos = Ls3_Ls4_solid.pos + self.C.rot_mat * \
            local_left_shoulder_point
        self.A1 = seg.Segment('A1: Left upper arm', A1pos, A1RotMat,
                              [self._a_solids[0], self._a_solids[1]], (0, 1, 0),
                              build_toward_positive_z=False)

        # left forearm-hand
        A2RotMat = (self.A1.rot_mat *
            inertia.euler_123([self.CFG['A1A2extension'], 0.0, 0.0]))
        A2pos = self.A1.end_pos
        self.A2 = seg.Segment('A2: Left forearm-hand',
                              A2pos,
                              A2RotMat,
                              [self._a_solids[x] for x in range(2, 7)],
                              (1.0, 0.0, 0.0),
                              build_toward_positive_z=False)

        # right upper arm
        local_right_shoulder_point = \
                np.array([[-shoulder_width / 2.0], [0.0], [Ls3_Ls4_solid.height]])
        B1RotMat = (self.C.rot_mat *
                inertia.euler_123([self.CFG['CB1extension'],
                                   self.CFG['CB1abduction'],
                                   self.CFG['CB1rotation']]))
        B1pos = Ls3_Ls4_solid.pos + self.C.rot_mat * \
            local_right_shoulder_point
        self.B1 = seg.Segment('B1: Right upper arm',
                               B1pos,
                               B1RotMat,
                               [self._b_solids[0], self._b_solids[1]],
                               (0.0, 1.0, 0.0),
                               build_toward_positive_z=False)

        # right forearm-hand
        B2RotMat = (self.B1.rot_mat *
            inertia.euler_123([self.CFG['B1B2extension'], 0.0, 0.0]))
        B2pos = self.B1.end_pos
        self.B2 = seg.Segment('B2: Right forearm-hand',
                              B2pos,
                              B2RotMat,
                              [self._b_solids[x] for x in range(2, 7)],
                              (1.0, 0.0, 0.0),
                              build_toward_positive_z=False)

        # legs
        Ls0_Ls1_solid = self._s[0]
        hip_width = Ls0_Ls1_solid.stads[0].thickness + \
            Ls0_Ls1_solid.stads[0].radius

        # left thigh
        local_left_hip_point = np.array([[hip_width / 2.0],
                                         [0.0],
                                         [0.0]])
        J1RotMat = (self.P.rot_mat *
             inertia.euler_123([self.CFG['PJ1extension'],
                                self.CFG['PJ1adduction'],
                                0.0]))
        J1pos = Ls0_Ls1_solid.pos + self.P.rot_mat * \
            local_left_hip_point
        self.J1 = seg.Segment('J1: Left thigh',
                              J1pos,
                              J1RotMat,
                              [self._j_solids[0], self._j_solids[1],
                                  self._j_solids[2]],
                              (0.0, 1.0, 0.0),
                              build_toward_positive_z=False)

        # left shank-foot
        J2RotMat = (self.J1.rot_mat *
            inertia.euler_123([self.CFG['J1J2flexion'], 0.0, 0.0]))
        J2pos = self.J1.end_pos
        self.J2 = seg.Segment('J2: Left shank-foot',
                              J2pos,
                              J2RotMat,
                              [self._j_solids[n] for n in range(3, 9)],
                              (1.0, 0.0, 0.0),
                              build_toward_positive_z=False)

        # right thigh
        local_right_hip_point = np.array([[-hip_width / 2.0],
                                          [0.0],
                                          [0.0]])
        K1RotMat = (self.P.rot_mat *
             inertia.euler_123([self.CFG['PK1extension'],
                                       self.CFG['PK1abduction'],
                                       0.0]))
        K1pos = Ls0_Ls1_solid.pos + self.P.rot_mat * \
            local_right_hip_point
        self.K1 = seg.Segment('K1: Right thigh',
                              K1pos,
                              K1RotMat,
                              [self._k_solids[0], self._k_solids[1],
                                  self._k_solids[2]],
                              (0.0, 1.0, 0.0),
                              build_toward_positive_z=False)

        # right shank-foot
        K2RotMat = (self.K1.rot_mat *
            inertia.euler_123([self.CFG['K1K2flexion'], 0.0, 0.0]))
        K2pos = self.K1.end_pos
        self.K2 = seg.Segment('K2: Right shank-foot',
                               K2pos,
                               K2RotMat,
                               [self._k_solids[n] for n in range(3, 9)],
                               (1.0, 0.0, 0.0),
                               build_toward_positive_z=False)

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
                if key in self._deprecated_CFGnames.keys():
                    msg = ("'{0}' should be called '{1}'."
                        " This will raise an error in future versions.".format(
                            key, self._deprecated_CFGnames[key]))
                    warnings.warn(msg, YeadonDeprecationWarning)
                    key = self._deprecated_CFGnames[key]
                elif key not in self.CFGnames:
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
