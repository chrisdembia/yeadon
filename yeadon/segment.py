"""Segment objects are used by the human module. A segment has a position, and
an orientation. All constituent solids of a segment have the same orientation.
That is to say that the base of the segment is at a joint in the human. The
user does not interact with this module.

"""
# Use Python3 integer division rules.
from __future__ import division

# external imports
import numpy as np

# local imports
from . import inertia
from .utils import printoptions


class Segment(object):

    @property
    def mass(self):
        """Mass of the segment, in units of kg."""
        return self._mass

    @property
    def center_of_mass(self):
        """Center of mass of the segment, a np.ndarray, in units of m,
        expressed in the global frame, from the bottom center of the pelvis
        (Ls0)."""
        return self._center_of_mass

    @property
    def inertia(self):
        """Inertia matrix of the segment, a np.matrix, in units of kg-m^2,
        about the center of mass of the human, expressed in the global
        frame."""
        return self._inertia

    @property
    def rel_center_of_mass(self):
        """Center of mass of the segment, a np.ndarray, in units of m,
        expressed in the frame of the segment, from the origin of the
        segment."""
        return self._rel_center_of_mass

    @property
    def rel_inertia(self):
        """Inertia matrix/dyadic of the segment, a np.matrix, in units of
        kg-m^2, about the center of mass of the segment, expressed in the frame
        of the segment."""
        return self._rel_inertia

    @property
    def pos(self):
        """Position of the origin of the segment, a np.ndarray, in units of m,
        expressed in the global frame, from the bottom center of the pelvis
        (Ls0)."""
        return self._pos

    @property
    def end_pos(self):
        """Position of the center of the last (farthest from pelvis) stadium in
        this segment, a np.ndarray, in units of m, expressed in the global
        frame, from the bottom center of the pelvis (Ls0)."""
        return self._end_pos

    @property
    def rot_mat(self):
        """Rotation matrix specifying the orientation of this segment relative
        to the orientation of the global frame, a np.matrix, unitless.
        Multiplying a vector expressed in this segment's frame with this
        rotation matrix on the left gives that same vector, but expressed in
        the global frame."""
        return self._rot_mat

    def __init__(self, label, pos, rot_mat, solids, color,
                 build_toward_positive_z=True):
        """Initializes a segment object. Stores inputs as instance variables,
        calculates the orientation of the segment's child solids, and
        calculates the "relative" inertia parameters (mass, center of mass
        and inertia) of the segment.

        Parameters
        ----------
        label : str
            The ID and name of the segment.
        pos : numpy.array, shape(3,1)
            The vector position of the segment's base,
            with respect to the global frame.
        rot_mat : numpy.matrix, shape(3,3)
            The orientation of the segment is given by a rotation matrix that
            specifies the orientation of the segment with respect to the fixed
            human frame. That is, rot_mat is (^N R ^A), where N is the fixed
            human frame, and A is the frame fixed to this segment. If v is a
            vector and (^A v) is its representation in A, then (^N R ^A * ^A v)
            = (^N v) is its representation in N.
        solids : list of solid objects
            The solid objects that compose the segment
        color : tuple (3,)
            Color with which to plot this segment in the plotting functions.
            RGB tuple with float values between 0 and 1.
        build_toward_positive_z : bool, optional
            The order of the solids matters. By default they are stacked on top
            of each other in the segment's local +z direction. If this is set to
            False, then they are stacked in the local -z direction. This is
            done so that, for example, in the default configuration, the arms
            are directed down.

        """
        self.label = label
        if pos.shape != (3, 1):
            raise ValueError("Position must be 3-D.")
        self._pos = pos
        self._rot_mat = np.asmatrix(rot_mat)
        self.solids = solids
        self.nSolids = len(self.solids)
        self.color = color
        self._build_toward_positive_z = build_toward_positive_z
        # must set the position of constituent solids before being able to
        # calculate relative/local properties, or set end_pos/length.
        self._set_orientations()
        if self._build_toward_positive_z:
            self._end_pos = self.solids[-1].end_pos
        else:
            self._end_pos = self.solids[-1].pos
        self.length = np.linalg.norm(self._end_pos - self.pos)
        self.calc_rel_properties()

    def _set_orientations(self):
        """Sets the position (self.pos) and rotation matrix (self.rot_mat)
        for all solids in the segment by calling each constituent
        solid's set_orientation method. The position of the i-th solid,
        expressed in the global frame, is given by the sum
        of the segment's base position and the directed height of all the
        solids of the segment up to the i-th solid.

        """
        # pos and rot_mat for first solid
        self.solids[0].set_orientation(self.pos, self.rot_mat,
                self._build_toward_positive_z)
        # pos and rot_mat for remaining solids
        for i in np.arange(self.nSolids):
            if i != 0:
                if self._build_toward_positive_z:
                    pos = self.solids[i-1].end_pos
                else:
                    pos = self.solids[i-1].pos
                self.solids[i].set_orientation(pos, self.rot_mat,
                        self._build_toward_positive_z)

    def calc_rel_properties(self):
        """Calculates the mass, relative/local center of mass, and
        relative/local inertia tensor (about the segment's center of mass).
        Also computes the center of mass of each constituent solid with
        respect to the segment's base in the segment's reference frame.

        """
        # mass
        self._mass = 0.0
        for s in self.solids:
            self._mass += s.mass
        # relative position of each solid w.r.t. segment orientation and
        # segment's origin
        solidpos = []
        # center of mass of each solid w.r.t. segment orientation and
        # segment's origin
        solidCOM = []
        z_unit_vector = np.array([[0, 0, 1]]).T
        if self._build_toward_positive_z:
            solidpos.append(np.zeros((3, 1)))
            for i in np.arange(self.nSolids):
                if i != 0:
                    solidpos.append( solidpos[i-1] +
                                          self.solids[i-1].height *
                                          z_unit_vector)
            solidCOM.append(self.solids[0].rel_center_of_mass)
            for i in np.arange(self.nSolids):
                if i != 0:
                    solidCOM.append( solidpos[i] +
                                          self.solids[i].rel_center_of_mass)
        else: # not self._build_toward_positive_z
            # solidpos
            last_pos = np.zeros((3, 1))
            for solid in self.solids:
                solidpos.append(last_pos - solid.height * z_unit_vector)
                last_pos = solidpos[-1]
            # solidCOM
            for i in np.arange(self.nSolids):
                solidCOM.append(solidpos[i] +
                        self.solids[i].rel_center_of_mass)
        # TODO above code could be substantially cleaned up.
        # relative center of mass
        relmoment = np.zeros((3, 1))
        for i in np.arange(self.nSolids):
            relmoment += self.solids[i].mass * solidCOM[i]
        self._rel_center_of_mass = relmoment / self.mass
        # relative Inertia
        self._rel_inertia = np.mat(np.zeros((3, 3)))
        for i in np.arange(self.nSolids):
            dist = solidCOM[i] - self.rel_center_of_mass
            self._rel_inertia += np.mat(inertia.parallel_axis(
                                      self.solids[i].rel_inertia,
                                      self.solids[i].mass,
                                      [dist[0, 0], dist[1, 0], dist[2, 0]]))

    def calc_properties(self):
        """Calculates the segment's center of mass with respect to the bottm
        center of the pelvis (Ls0) and the segment's inertia in the global
        frame but about the segment's center of mass.

        """
        # center of mass
        self._center_of_mass = self.pos + self.rot_mat * self.rel_center_of_mass
        # inertia in frame f w.r.t. segment's COM
        self._inertia = inertia.rotate_inertia(self.rot_mat, self.rel_inertia)

    def __str__(self):
        return(self._properties_string())

    def print_properties(self, precision=5, suppress=True):
        """Prints mass, center of mass (in segment and global frames),
        and inertia (in solid and global frames).

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
        print(self._properties_string())

    def _properties_string(self, precision=5, suppress=True):
        """Prints mass, center of mass (in segment and global frames),
        and inertia (in solid and global frames).

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
        # self.COM, etc. needs to be defined first.
        if not hasattr(self, 'center_of_mass') or not hasattr(self, 'inertia'):
            self.calc_properties()

        template = \
"""\
{label} properties:

Mass (kg):

{mass:1.{precision}f}

COM in segment's frame from segment's origin (m):

{rel_center_of_mass}

COM in global frame from bottom center of pelvis (Ls0) (m):

{center_of_mass}

Inertia tensor in segment's frame about segment's COM (kg-m^2):

{rel_inertia}

Inertia tensor in global frame about segment's COM (kg-m^2):

{inertia}
"""

        with printoptions(precision=precision, suppress=suppress):
            return template.format(label=self.label,
                                  mass=self.mass,
                                  precision=precision,
                                  rel_center_of_mass=self.rel_center_of_mass,
                                  center_of_mass=self.center_of_mass,
                                  rel_inertia=self.rel_inertia,
                                  inertia=self.inertia)

    def print_solid_properties(self, precision=5, suppress=True):
        """Calls the print_properties() member method of each of this
        segment's solids. See the solid class's definition of
        print_properties(self) for more detail.

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
        for s in self.solids:
            s.print_properties(precision=precision, suppress=suppress)

    def draw_mayavi(self, mlabobj):
        """Draws in a MayaVi window all the solids within this segment.  """
        for s in self.solids:
            s.draw_mayavi(mlabobj, self.color)

    def _update_mayavi(self):
        """Updates all of the solids in this segment for MayaVi."""
        for s in self.solids:
            s._update_mayavi()
