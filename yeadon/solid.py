"""Solid objects are used by the segment module. A solid has a position, and
orientation (defined by a rotation matrix). This module also contains the
class definition for stadium objects, which are used to construct
StadiumSolid solids. The Solid class has two subclasses: the StadiumSolid and
Semiellipsoid classes.

"""
# Use Python3 integer division rules.
from __future__ import division
import warnings

import numpy as np

import inertia
from .utils import printoptions

class Stadium(object):
    """Stadium, the 2D shape.

    """
    validStadiaLabels = {
        'Ls0': 'hip joint centre',
        'Ls1': 'umbilicus',
        'Ls2': 'lowest front rib',
        'Ls3': 'nipple',
        'Ls4': 'shoulder joint centre',
        'Ls5': 'acromion',
        'Ls6': 'beneath nose',
        'Ls7': 'above ear',
        'La0': 'shoulder joint centre',
        'La1': 'mid-arm',
        'La2': 'elbow joint centre',
        'La3': 'maximum forearm perimeter',
        'La4': 'wrist joint centre',
        'La5': 'base of thumb',
        'La6': 'knuckles',
        'La7': 'fingernails',
        'Lb0': 'shoulder joint centre',
        'Lb1': 'mid-arm',
        'Lb2': 'elbow joint centre',
        'Lb3': 'maximum forearm perimeter',
        'Lb4': 'wrist joint centre',
        'Lb5': 'base of thumb',
        'Lb6': 'knuckles',
        'Lb7': 'fingernails',
        'Lj0': 'hip joint centre',
        'Lj1': 'crotch',
        'Lj2': 'mid-thigh',
        'Lj3': 'knee joint centre',
        'Lj4': 'maximum calf perimeter',
        'Lj5': 'ankle joint centre',
        'Lj6': 'heel',
        'Lj7': 'arch',
        'Lj8': 'ball',
        'Lj9': 'toe nails',
        'Lk0': 'hip joint centre',
        'Lk1': 'crotch',
        'Lk2': 'mid-thigh',
        'Lk3': 'knee joint centre',
        'Lk4': 'maximum calf perimeter',
        'Lk5': 'ankle joint centre',
        'Lk6': 'heel',
        'Lk7': 'arch',
        'Lk8': 'ball',
        'Lk9': 'toe nails'}

    def __init__(self, label, inID, in1, in2=None, alignment='ML'):
        """Defines a 2D stadium shape and checks inputs for errors. A stadium,
        described in Yeadon 1990-ii, is defined by two parameters. Stadia can
        depracate to circles if their "thickness" is 0.

        Parameters
        ----------
        label : str
            Name of the stadium level, according to Yeadon 1990-ii.
        inID : str
            Identifies the type of information for the next two inputs.
            'perimwidth' for perimeter and width input, 'depthwidth' for
            depth and width input, 'perimeter' or 'radius' for a circle,
            'thicknessradius' for thickness and radius input.
        in1 : float
            Either perimeter, depth, or thickness, as determined by inID
        in2 : float
            Either width, or radius, as determined by inID
        alignment = 'ML' : str
            Identifies the long direction of the stadium. 'ML' stands for
            medio-lateral. Aleternatively, 'AP' (anteroposterior) can be
            supplied. The only 'AP' stadiums should be at the heels.

        """
        if label == 'Ls5: acromion/bottom of neck':
            self.label = label
        elif label in [lab + ': ' + desc for lab, desc in
                self.validStadiaLabels.items()]:
            self.label = label
        else:
            raise ValueError("'{}' is not a valid label.".format(label))

        if inID == 'perimwidth':
            self.perimeter = in1
            self.width = in2
            self.thickness = ((np.pi * self.width - self.perimeter) /
                          (2.0 * np.pi - 4.0))
            self.radius = ((self.perimeter - 2.0 * self.width)  /
                           (2.0 * np.pi - 4.0))
        elif inID == 'depthwidth':
            self.width = in2
            self.perimeter = 2.0 * in2 + (np.pi - 2.0) * in1
            self.thickness = ((np.pi * self.width - self.perimeter) /
                          (2.0 * np.pi - 4.0))
            self.radius = (self.perimeter - 2.0 * self.width) / (2.0 * np.pi -
                    4.0)
        elif inID == 'perimeter':
            self._set_as_circle(in1 / (2.0 * np.pi))
        elif inID == 'radius':
            self._set_as_circle(in1)
        elif inID == 'thicknessradius':
            self.thickness = in1
            self.radius = in2
            self.perimeter = 4.0 * self.thickness + 2.0 * np.pi * self.radius
            self.width = 2.0 * self.thickness + 2.0 * self.radius
        else:
            raise ValueError("Stadium " + self.label +
                " not defined properly, " + inID + " is not valid. You must " +
                "use inID= perimwidth, depthwidth, perimeter, or radius.")
        if self.radius == 0:
            raise ValueError("Radius of stadium '%' is zero." % self.radius)
        if self.radius < 0 or self.thickness < 0:
            warnings.warn("Stadium '{}' is defined "
                "incorrectly, r must be positive and t must be nonnegative. "
                "r = {} and t = {} . This means that 2 < perimeter/width < pi. "
                "Currently, this ratio is {}.\n".format(self.label,
                    self.radius, self.thickness, self.perimeter / self.width))
            if inID == 'perimwidth':
                self._set_as_circle(in1 / (2.0 * np.pi))
                print "Fix: stadium set as circle with perimeter as given."
            elif inID == 'depthwidth':
                self._set_as_circle(0.5 * in2)
                print "Fix: stadium set as circle with diameter of given width."
            else:
                raise ValueError("Negative radius/thickness cannot be "
                        "corrected.")
        if alignment != 'AP' and alignment != 'ML':
            raise ValueError("Error: stadium " + self.label +
                " alignment is not valid, must be either AP or ML")
        else:
            self.alignment = alignment

    def _set_as_circle(self, radius):
        """Sets radius, perimeter, thickness, and width if thickness is 0."""
        self.radius = radius
        self.perimeter = 2.0 * np.pi * self.radius
        self.thickness = 0.0
        self.width = self.perimeter / np.pi

class Solid(object):
    """Solid. Has two subclasses, stadiumsolid and semiellipsoid. This base
    class manages setting orientation, and calculating properties.

    """
    # Transparency for plotting.
    alpha = .5

    @property
    def mass(self):
        """Mass of the solid, a float in units of kg."""
        return self._mass

    @property
    def center_of_mass(self):
        """Center of mass of the solid, a np.ndarray of shape (3,1), in
        units of m, expressed in the global frame, from the bottom center of
        the pelvis (Ls0)."""
        return self._center_of_mass

    @property
    def inertia(self):
        """Inertia matrix of the solid, a np.matrix of shape (3,3), in units
        of kg-m^2, about the center of mass of the human, expressed in the
        global frame.
        """
        return self._inertia

    @property
    def rel_center_of_mass(self):
        """Center of mass of the solid, a np.ndarray of shape (3,1), in
        units of m, expressed in the frame of the solid, from the origin of
        the solid."""
        return self._rel_center_of_mass

    @property
    def rel_inertia(self):
        """Inertia matrix of the solid, a np.matrix of shape (3,3), in units
        of kg-m^2, about the center of mass of the solid, expressed in the
        frame of the solid."""
        return self._rel_inertia

    @property
    def pos(self):
        """Position of the origin of the solid, which is the center of the
        surface closest to the pelvis, a np.ndarray of shape (3,1), in units
        of m, expressed in the global frame, from the bottom center of the
        pelvis (Ls0)."""
        return self._pos

    @property
    def end_pos(self):
        """Position of the point on the solid farthest from the origin along
        the longitudinal axis of the segment, a np.ndarray of shape (3,1),
        in units of m, expressed in the global frame, from the bottom center
        of the pelvis (Ls0)."""
        return self._end_pos

    def __init__(self, label, density, height):
        """Defines a solid. This is a base class. Sets the alpha value to
        be used for drawing with MayaVi.

        Parameters
        ----------
        label : str
            Name of the solid
        density : float
            In units (kg/m^3), used to calculate the solid's mass
        height : float
            Distance from bottom to top of the solid

        """
        #TODO: Check for valid labels
        self.label = label
        #TODO: Check that these two are floats
        self.density = density
        self.height = height
        self._rel_inertia = np.zeros((3, 3)) # this gets set in subclasses
        self._mass = 0.0
        self._rel_center_of_mass = np.array([[0.0], [0.0], [0.0]])

    def set_orientation(self, proximal_pos, rot_mat, build_toward_positive_z):
        """Sets the position, rotation matrix of the solid, and calculates
        the "absolute" properties (center of mass, and inertia tensor) of the
        solid.

        Parameters
        ----------
        proximal_pos : np.array (3,1)
            Position of center of proximal end of solid in the absolute fixed
            coordinates of the human.
        rot_mat : np.matrix (3,3)
            Orientation of solid, with respect to the fixed coordinate system.
        build_toward_positive_z : bool, optional
            The order of the solids in the parent segment matters. By default
            they are stacked on top of each other in the segment's local +z
            direction. If this is set to False, then they are stacked in the
            local -z direction. This is done so that, for example, in the default
            configuration, the arms are directed down.

        """
        self._rot_mat = rot_mat
        if build_toward_positive_z:
            self._pos = proximal_pos
            self._end_pos = self.pos + (self.height * self._rot_mat *
                                      np.array([[0], [0], [1]]))
        else:
            self._end_pos = proximal_pos
            self._pos = self._end_pos - (self.height * self._rot_mat *
                    np.array([[0], [0], [1]]))
        self.calc_properties()

    def calc_properties(self):
        """Sets the center of mass and inertia of the solid, both with respect
        to the fixed human frame.

        """
        try:
            try:
                # Here is v_a = R * v_b, where A is global frame and B is
                # rotated frame relative to A.
                self._center_of_mass = (self.pos + self._rot_mat *
                        self.rel_center_of_mass)
            except AttributeError as err:
                err.message = err.message + \
                    '. You must set the orientation before attempting ' + \
                    'to calculate the properties.'
                raise
        except AttributeError as e:
            print(e.message)

        self._inertia = inertia.rotate_inertia(self._rot_mat, self.rel_inertia)

    def print_properties(self, precision=5, suppress=True):
        """Prints mass, center of mass (in solid and global frames), and
        inertia (in solid and global frames).

        The solid's origin is at the bottom center of the proximal stadium
        (or stadium closest to the pelvis, Ls0).

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

COM in solid's frame from solid's origin (m):

{rel_center_of_mass}

COM in global frame from bottom center of pelvis (Ls0) (m):

{center_of_mass}

Inertia tensor in solid's frame about solid's COM (kg-m^2):

{rel_inertia}

Inertia tensor in global frame about solid's COM (kg-m^2):

{inertia}
"""

        with printoptions(precision=precision, suppress=suppress):
            print(template.format(label=self.label,
                                  mass=self.mass,
                                  precision=precision,
                                  rel_center_of_mass=self.rel_center_of_mass,
                                  center_of_mass=self.center_of_mass,
                                  rel_inertia=self.rel_inertia,
                                  inertia=self.inertia))

    def draw_mayavi(self, mlabobj, col):
        raise NotImplementedError()


class StadiumSolid(Solid):
    """Stadium solid. Derived from the solid class.

    """
    def __init__(self, label, density, stadium0, stadium1, height):
        """Defines a stadium solid object. Creates its base object, and
        calculates relative/local inertia properties.

        Parameters
        ----------
        label : str
            Name of the solid.
        density : float
            Density of the solid (kg/m^3).
        stadium0 : :py:class:`Stadium`
            Lower stadium of the stadium solid.
        stadium1 : :py:class:`Stadium`
            Upper stadium of the stadium solid.
        height : float
            Distance between the lower and upper stadia.

        """
        super(StadiumSolid, self).__init__(label, density, height)
        self.stads = [stadium0, stadium1]
        self.alignment = 'ML'
        # if either stadium is oriented anteroposteriorly.
        # inertia must be rotated, and the plots must be modified
        if (self.stads[0].alignment == 'AP' or
            self.stads[1].alignment == 'AP'):
            self.alignment = 'AP'
        if stadium0.thickness == 0:
            self.degenerate_by_t0 = True
        else:
            self.degenerate_by_t0 = False
        self.calc_rel_properties()
        self._orig_mesh_points = list()
        self._orig_mesh_points.append(self._make_mesh(0))
        self._orig_mesh_points.append(self._make_mesh(1))

    def calc_rel_properties(self):
        """Calculates mass, relative center of mass, and relative/local
        inertia, according to formulae in Appendix B of Yeadon 1990-ii. If the
        stadium solid is arranged anteroposteriorly, the inertia is rotated
        by pi/2 about the z axis.

        """
        # There are two cases of stadium solid degeneracy to consider:
        # t0 = 0, and t0 = t1 = 0. The degeneracy arises when b has a
        # denominator of 0. The case that t1 = 0 is not an issue, then.
        # The way the case of t0 = 0 is handled is by switching the two stadia.
        # Note that thi affects how the relative center of mass is set, but
        # does not affect the mass or moments of inertia calculations.
        # The case in which t0 = t1 = 0, we set b to 1. That is because t = t0
        # (1 + bz) is going to be zero anyway, since t0 = 0.
        D = self.density
        h = self.height
        if self.degenerate_by_t0:
            # Swap the stadia.
            r0 = self.stads[1].radius
            t0 = self.stads[1].thickness
            r1 = self.stads[0].radius
            t1 = self.stads[0].thickness
        else:
            r0 = self.stads[0].radius
            t0 = self.stads[0].thickness
            r1 = self.stads[1].radius
            t1 = self.stads[1].thickness
        a = (r1 - r0) / r0
        if t0 == 0:
            # Truncated cone, since both thicknesses are zero.
            # b can be anything, because t = t0(1 + bz) = (0)(1 + bz) = 0.
            b = 1
        else:
            b = (t1 - t0) / t0
        self._mass = D * h * r0 * (4.0 * t0 * self._F1(a,b) +
                                  np.pi * r0 * self._F1(a,a))
        zcom = D * (h**2.0) * (4.0 * r0 * t0 * self._F2(a,b) +
                               np.pi * (r0**2.0) * self._F2(a,a)) / self.mass
        if self.degenerate_by_t0 and t0 != 0:
            # We swapped the stadia, and it's not a truncated cone.
            # Must define this intermediate because zcom above is still what
            # must be used for the parallel axis theorem below.
            adjusted_zcom = h - zcom
        else:
            adjusted_zcom = zcom
        self._rel_center_of_mass = np.array([[0.0],[0.0],[adjusted_zcom]])

        # moments of inertia
        Izcom = D * h * (4.0 * r0 * (t0**3.0) * self._F4(a,b) / 3.0 +
                         np.pi * (r0**2.0) * (t0**2.0) * self._F5(a,b) +
                         4.0 * (r0**3.0) * t0 * self._F4(b,a) +
                         np.pi * (r0**4.0) * self._F4(a,a) * 0.5 )
        # CAUGHT AN (minor) ERROR IN YEADON'S PAPER HERE. The Dh^3 in the
        # formula below is missing from the second formula for Iy^0 on page 73
        # of Yeadon1990-ii.
        Iy = (D * h * (4.0 * r0 * (t0**3.0) * self._F4(a,b) / 3.0 +
                       np.pi * (r0**2.0) * (t0**2.0) * self._F5(a,b) +
                       8.0 * (r0**3.0) * t0*self._F4(b,a) / 3.0 +
                      np.pi * (r0**4.0) * self._F4(a,a) * 0.25) +
              D * (h**3.0) * (4.0 * r0 * t0 * self._F3(a,b) +
                              np.pi * (r0**2.0) * self._F3(a,a)))
        Iycom = Iy - self.mass * (zcom**2.0)
        Ix = (D * h * (4.0 * r0 * (t0**3.0) * self._F4(a,b) / 3.0 +
                       np.pi * (r0**4.0) * self._F4(a,a) * 0.25) +
              D * (h**3.0) * (4.0 * r0 * t0 * self._F3(a,b) +
                              np.pi * (r0**2.0) * self._F3(a,a)))
        Ixcom = Ix - self.mass*(zcom**2.0)
        self._rel_inertia = np.mat([[Ixcom,0.0,0.0],
                                  [0.0,Iycom,0.0],
                                  [0.0,0.0,Izcom]])
        if self.alignment == 'AP':
            # rearrange to anterorposterior orientation
            self._rel_inertia = inertia.rotate_inertia(
                    inertia.rotate_space_123([0, 0, np.pi/2]), self.rel_inertia)

    def draw_mayavi(self, mlabobj, col):
        """Draws the initial stadium in 3D using MayaVi.

        Parameters
        ----------
        mlabobj : mayavi.soemthing
            The MayaVi object we can draw on.
        col : tuple (3,)
            Color as an rgb tuple, with values between 0 and 1.

        """
        self._generate_mesh()
        self._mesh = mlabobj.mesh(self._mesh_points['x'], self._mesh_points['y'],
                self._mesh_points['z'], color=col, opacity=Solid.alpha)

    def _update_mayavi(self):
        """Updates the mesh in MayaVi."""
        self._generate_mesh()
        self._mesh.mlab_source.set(x=self._mesh_points['x'],
                y=self._mesh_points['y'], z=self._mesh_points['z'])

    def _generate_mesh(self):
        """Generates grid points for a MayaVi mesh."""
        X0, Y0, Z0 = self._make_pos(0)
        X1, Y1, Z1 = self._make_pos(1)
        Xpts = np.array(np.concatenate( (X0, X1), axis=0))
        Ypts = np.array(np.concatenate( (Y0, Y1), axis=0))
        Zpts = np.array(np.concatenate( (Z0, Z1), axis=0))
        self._mesh_points = {'x': Xpts, 'y': Ypts, 'z': Zpts}

    def _make_mesh(self, i):
        """Generates the un-rotated coordinates of the solid. These values are
        saved at instantiation.

        Parameters
        ----------
        i : int
            Identifies which stadium to generate the mesh points for (the top
            or bottom).

        """
        theta = [np.linspace(0.0,np.pi/2,5)]
        x = self.stads[i].thickness + self.stads[i].radius * np.cos(theta);
        y = self.stads[i].radius * np.sin(theta);
        if self.alignment == 'AP':
            temp = x
            x = y
            y = temp
            del temp
        xrev = x[:, ::-1]
        yrev = y[:, ::-1]
        X = np.concatenate( (x, -xrev, -x, xrev), axis=1)
        Y = np.concatenate( (y, yrev, -y, -yrev), axis=1)
        Z = i*self.height*np.ones((1,20))
        POSES = np.concatenate( (X, Y, Z), axis=0)
        return POSES

    def _make_pos(self, i):
        """Generates coordinates to be used for 3D visualization purposes.

        """
        rotated_points = self._rot_mat * self._orig_mesh_points[i]
        X, Y, Z = np.vsplit(rotated_points, 3)
        X = X + self.pos[0]
        Y = Y + self.pos[1]
        Z = Z + self.pos[2]
        return X, Y, Z

    @staticmethod
    def _F1(a, b):
        """Integration term. See Yeadon 1990-ii Appendix 2."""
        return 1.0 + (a + b) * 0.5 + a * b / 3.0

    @staticmethod
    def _F2(a, b):
        """Integration term. See Yeadon 1990-ii Appendix 2."""
        return 0.5 + (a + b) / 3.0 + a * b * 0.25

    @staticmethod
    def _F3(a, b):
        """Integration term. See Yeadon 1990-ii Appendix 2."""
        return 1.0/3.0 + (a + b) / 4.0 + a * b *0.2

    @staticmethod
    def _F4(a, b):
        """Integration term. See Yeadon 1990-ii Appendix 2."""
        return (1.0 + (a + 3.0 * b) * 0.5 + (a * b + b**2.0) +
                      (3.0 * a * b**2.0 + b**3.0) * 0.25 + a * (b**3.0) * 0.2)

    @staticmethod
    def _F5(a, b):
        """Integration term. See Yeadon 1990-ii Appendix 2."""
        return (1.0 + (a + b) + (a**2.0 + 4.0 * a * b + b**2.0) / 3.0 +
                       a * b * (a + b) * 0.5 + (a**2.0) * (b**2.0) * 0.2)

class Semiellipsoid(Solid):
    """Semiellipsoid."""

    n_mesh_points = 30
    def __init__(self,label,density,baseperim,height):
        """Defines a semiellipsoid (solid) object. Creates its base object, and
        calculates relative/local inertia properties. The base is circular (its
        height axis is pointed upwards), so only 2 parameters are needed to
        define the semiellipsoid.

        Parameters
        ----------
        label : str
            Name of the solid.
        density : float
            Density of the solid (kg/m^3).
        baseperimeter : float
            The base is circular.
        height : float
            The remaining minor axis.

        """
        super(Semiellipsoid, self).__init__(label, density, height)
        self.baseperimeter = baseperim
        self.radius = self.baseperimeter/(2.0*np.pi)
        self.calc_rel_properties()
        self._mesh_x, self._mesh_y, self._mesh_z = self._make_mesh()

    def calc_rel_properties(self):
        """Calculates mass, relative center of mass, and relative/local
        inertia, according to somewhat commonly availble formulae.

        """
        D = self.density
        r = self.radius
        h = self.height
        self._mass = D * 2.0/3.0 * np.pi * (r**2) * h
        self._rel_center_of_mass = np.array([[0.0],[0.0],[3.0/8.0 * h]])
        Izcom = D * 4.0/15.0 * np.pi * (r**4.0) * h
        Iycom = D * np.pi * (2.0/15.0 * (r**2.0) * h * (r**2.0 + h**2.0) -
            3.0/32.0 * (r**2.0) * (h**3.0))
        Ixcom = Iycom
        self._rel_inertia = np.mat([[Ixcom,0.0,0.0],
                                  [0.0,Iycom,0.0],
                                  [0.0,0.0,Izcom]])

    def draw_mayavi(self, mlabobj, col):
        """Draws the semiellipsoid in 3D using MayaVi.

        Parameters
        ----------
        mlabobj :
            The MayaVi object we can draw on.
        col : tuple (3,)
            Color as an rgb tuple, with values between 0 and 1.

        """
        self._generate_mesh()
        self._mesh = mlabobj.mesh(*self._mesh_points, color=col,
                opacity=Solid.alpha)

    def _update_mayavi(self):
        """Updates the mesh in MayaVi."""
        self._generate_mesh()
        self._mesh.mlab_source.set(x=self._mesh_points[0],
                y=self._mesh_points[1], z=self._mesh_points[2])

    def _generate_mesh(self):
        """Generates a mesh for MayaVi."""
        self._mesh_points = self._make_pos()

    def _make_mesh(self):
        """Generates the un-rotated coordinates of the solid. These values are
        saved at instantiation.

        """
        u = np.linspace(0, 2.0 * np.pi, self.n_mesh_points)
        v = np.linspace(0, np.pi / 2.0, self.n_mesh_points)
        x = self.radius * np.outer(np.cos(u), np.sin(v))
        y = self.radius * np.outer(np.sin(u), np.sin(v))
        z = self.height * np.outer(np.ones(np.size(u)), np.cos(v))
        return x, y, z

    def _make_pos(self):
        """Generates coordinates to be used for 3D visualization purposes,
        given the position and orientation of the solid.

        """
        x = np.zeros(self._mesh_x.shape)
        y = np.zeros(self._mesh_y.shape)
        z = np.zeros(self._mesh_z.shape)
        for i in np.arange(self.n_mesh_points):
            for j in np.arange(self.n_mesh_points):
                POS = np.array([
                    [self._mesh_x[i,j]],
                    [self._mesh_y[i,j]],
                    [self._mesh_z[i,j]]])
                POS = self._rot_mat * POS
                x[i,j] = POS[0,0]
                y[i,j] = POS[1,0]
                z[i,j] = POS[2,0]
        x = self.pos[0,0] + x
        y = self.pos[1,0] + y
        z = self.pos[2,0] + z
        return x, y, z
