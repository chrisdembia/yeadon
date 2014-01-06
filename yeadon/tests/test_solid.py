#!/usr/bin/env python

# Use Python3 integer division rules.
from __future__ import division

import sys
import os
import unittest
import warnings

from numpy import testing, pi, array, matrix, sin, cos, zeros, array, mat, \
        arctan

from yeadon.solid import Stadium, Solid, StadiumSolid
from yeadon import inertia

warnings.filterwarnings('ignore', category=DeprecationWarning)


class StadiumSolidCheck(unittest.TestCase):
    """To check the formulae in yeadon.solid against those in the Yeadon1990-ii
    paper.

    """
    def __init__(self, density, thick0, rad0, thick1, rad1, height):
        self.D = density
        self.t0 = thick0
        self.r0 = rad0
        self.t1 = thick1
        self.r1 = rad1
        self.h = height
        self.a = (self.r1 - self.r0) / self.r0
        self.b = (self.t1 - self.t0) / self.t0

    def mass(s):
        return s.D * s.h * s.r0 * (
                4.0 * s.t0 * s._F1(s.a, s.b) +
                pi * s.r0 * s._F1(s.a, s.a)
                )

    def mass_center(s):
        return s.D * s.h**2 * (
                4.0 * s.r0 * s.t0 * s._F2(s.a, s.b) +
                pi * s.r0**2 * s._F2(s.a, s.a)
                ) / s.mass()

    def inertia_zz(s):
        """About center of mass."""
        return s.D * s.h * (
                4.0 * s.r0 * s.t0**3 * s._F4(s.a, s.b) / 3.0 +
                pi * s.r0**2 * s.t0**2 * s._F5(s.a, s.b) +
                4.0 * s.r0**3 * s.t0 * s._F4(s.b, s.a) +
                pi * s.r0**4 * s._F4(s.a, s.a) / 2.0
                )

    def inertia_yy(s):
        """About center of mass."""
        Jy_integral = (4.0 * s.r0 * s.t0**3 * s._F4(s.a, s.b) / 3.0 +
                pi * s.r0**2 * s.t0**2 * s._F5(s.a, s.b) +
                8.0 * s.r0**3 * s.t0 * s._F4(s.b, s.a) / 3.0 +
                pi * s.r0**4 * s._F4(s.a, s.a) / 4.0
                )
        z2A_integral = (4.0 * s.r0 * s.t0 * s._F3(s.a, s.b) +
                pi * s.r0**2 * s._F3(s.a, s.a))
        about_origin = s.D * s.h * Jy_integral + s.D * s.h**3 * z2A_integral
        return about_origin - s.mass() * s.mass_center()**2

    def inertia_xx(s):
        """About center of mass."""
        Jz_integral = (4.0 * s.r0 * s.t0**3 * s._F4(s.a, s.b) / 3.0 +
                pi * s.r0**4 * s._F4(s.a, s.a) / 4.0)
        z2A_integral = (4.0 * s.r0 * s.t0 * s._F3(s.a, s.b) +
                pi * s.r0**2 * s._F3(s.a, s.a))
        about_origin = s.D * s.h * Jz_integral + s.D * s.h**3 * z2A_integral
        return about_origin - s.mass() * s.mass_center()**2

    @staticmethod
    def _F1(a, b):
        return 1.0 + (a + b)/2.0 + a*b/3.0

    @staticmethod
    def _F2(a, b):
        return 0.5 + (a + b)/3.0 + a*b/4.0

    @staticmethod
    def _F3(a, b):
        return 1/3.0 + (a + b)/4.0 + a*b/5.0

    @staticmethod
    def _F4(a, b):
        return (1.0 + (a + 3.0*b)/2.0 + (3.0*a*b + 3.0*b**2)/3.0 +
                (3.0*a*b**2 + b**3)/4.0 + a*b**3/5.0)

    @staticmethod
    def _F5(a, b):
        return (1.0 + (2.0*a + 2.0*b)/2.0 + (a**2 + 4.0*a*b + b**2)/3.0 +
                2.0*a*b*(a + b)/4.0 + a**2 * b**2 / 5.0)


# define some useful functions for 2D stadia
def radius_from_perimeter_width(perimeter, width):
    """Returns the radius of the stadium given the perimeter and width."""
    return (perimeter - 2.0 * width) / (2 * pi - 4)

def thickness_from_perimeter_width(perimeter, width):
    """Returns the thickness of the stadium given the perimeter and
    width."""
    return 0.5 * width - radius_from_perimeter_width(perimeter, width)

def radius_from_depth(depth):
    return depth / 2.0

def thickness_from_depth_width(depth, width):
    return (width - depth) / 2.0

def perimeter_from_depth_width(depth, width):
    return 2 * (width - depth) + pi * depth

class TestStadium(unittest.TestCase):

    def test_init(self):
        # perimeter and width
        perimeter = 2.5
        width = 1.0
        pw = Stadium('La6: knuckles', 'perimwidth', perimeter, width)
        assert pw.label == 'La6: knuckles'
        assert pw.alignment == 'ML'
        testing.assert_almost_equal(pw.perimeter, perimeter)
        testing.assert_almost_equal(pw.width, width)
        testing.assert_almost_equal(pw.radius,
                radius_from_perimeter_width(perimeter, width))
        testing.assert_almost_equal(pw.thickness,
                thickness_from_perimeter_width(perimeter, width))

        # depth and width
        depth = 1.0
        width = 5.0
        dw = Stadium('La6: knuckles', 'depthwidth', depth, width, 'AP')
        assert dw.label == 'La6: knuckles'
        assert dw.alignment == 'AP'
        testing.assert_almost_equal(dw.width, width)
        testing.assert_almost_equal(dw.radius, radius_from_depth(depth))
        testing.assert_almost_equal(dw.thickness,
                thickness_from_depth_width(depth, width))
        testing.assert_almost_equal(dw.perimeter,
                perimeter_from_depth_width(depth, width))

        # perim
        perimeter = 5.0
        p = Stadium('Lk2: mid-thigh', 'perimeter', perimeter)
        assert p.label == 'Lk2: mid-thigh'
        assert p.alignment == 'ML'
        testing.assert_almost_equal(p.perimeter, perimeter)
        testing.assert_almost_equal(p.width, perimeter / pi)
        testing.assert_almost_equal(p.thickness, 0.0)
        testing.assert_almost_equal(p.radius, perimeter / 2.0 / pi)

        # radius
        radius = 1.0
        r = Stadium('Lk2: mid-thigh', 'radius', radius)
        assert r.label == 'Lk2: mid-thigh'
        assert r.alignment == 'ML'
        testing.assert_almost_equal(r.radius, radius)
        testing.assert_almost_equal(r.perimeter, 2.0 * pi * radius)
        testing.assert_almost_equal(r.thickness, 0.0)
        testing.assert_almost_equal(r.width, 2 * radius)

        # thickness and radius
        thickness = 10.0
        radius = 1.0
        tr = Stadium('Lk2: mid-thigh', 'thicknessradius', thickness, radius)
        assert tr.label == 'Lk2: mid-thigh'
        assert tr.alignment == 'ML'
        testing.assert_almost_equal(tr.radius, radius)
        testing.assert_almost_equal(tr.thickness, thickness)
        testing.assert_almost_equal(tr.perimeter, 2.0 * pi * radius + 4.0 *
                thickness)
        testing.assert_almost_equal(tr.width, 2 * radius + 2.0 * thickness)

    def test_invalid_stadium(self):
        """Tests that if a stadium is defined in such a way that it is invalid
        (negative radius or negative thickness), the correct action is taken.

        """
        # TODO Redirecting stdout is not working.
        actual_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            stad = Stadium('Lb1: mid-arm', 'perimwidth', 1.9, 1.0)
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "incorrectly" in str(w[-1].message)
            testing.assert_almost_equal(stad.perimeter, 1.9)
            testing.assert_almost_equal(stad.radius, 1.9 / (2.0 * pi))
            testing.assert_almost_equal(stad.thickness, 0.0)
            testing.assert_almost_equal(stad.width, 1.9 / pi)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            stad = Stadium('Lb1: mid-arm', 'perimwidth', 3.15, 1.0)
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            testing.assert_almost_equal(stad.perimeter, 3.15)
            testing.assert_almost_equal(stad.radius, 3.15 / (2.0 * pi))
            testing.assert_almost_equal(stad.thickness, 0.0)
            testing.assert_almost_equal(stad.width, 3.15 / pi)

        width = 1.0
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            depth = (1.9 - 2.0 * width) / (pi - 2.0)
            stad = Stadium('Lb1: mid-arm', 'depthwidth', depth, width)
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            testing.assert_almost_equal(stad.perimeter, pi * width )
            testing.assert_almost_equal(stad.radius, 0.5 * width)
            testing.assert_almost_equal(stad.thickness, 0.0)
            testing.assert_almost_equal(stad.width, width)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            depth = (3.15 - 2.0 * width) / (pi - 2.0)
            stad = Stadium('Lb1: mid-arm', 'depthwidth', depth, width)
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            testing.assert_almost_equal(stad.perimeter, pi * width )
            testing.assert_almost_equal(stad.radius, 0.5 * width)
            testing.assert_almost_equal(stad.thickness, 0.0)
            testing.assert_almost_equal(stad.width, width)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertRaises(ValueError, Stadium, 'Lb1: mid-arm',
                    'thicknessradius', -.1, -.5)
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertRaises(ValueError, Stadium, 'Lb1: mid-arm',
                    'thicknessradius', 1.0, -.3)
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertRaises(ValueError, Stadium, 'Lb1: mid-arm',
                    'thicknessradius', -.1, 2)
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)

        # Radius cannot be zero.
        self.assertRaises(ValueError, Stadium, 'Lb1: mid-arm',
                'thicknessradius', -.1, 0)
        self.assertRaises(ValueError, Stadium, 'Lb1: mid-arm',
                'thicknessradius', 0, 0)

        sys.stdout = actual_stdout


def test_solid():
    label = 'Test'
    density = 3.0
    height = 5.0
    sol = Solid(label, density, height)
    assert sol.label == label
    testing.assert_almost_equal(sol.density, density)
    testing.assert_almost_equal(sol.height, height)
    position = array([1., 2., 3.])
    # body-three 1-2-3
    angles = array([0.34, 23.6, -0.2])
    c1 = cos(angles[0])
    c2 = cos(angles[1])
    c3 = cos(angles[2])
    s1 = sin(angles[0])
    s2 = sin(angles[1])
    s3 = sin(angles[2])
    # definition of body 1-2-3 rotations from Spacecraft Dynamics, Kane,
    # Likins, Levinson, 1982 page 423 (this is the transpose of what is
    # presented)
    C = matrix([[c2 * c3, s1 * s2 * c3 + s3 * c1, -c1 * s2 * c3 + s3 * s1],
                [-c2 * s3, -s1 * s2 * s3 + c3 * c1, c1 * s2 * s3 + c3 *s1],
                [s2, -s1 * c2, c1 * c2]])

    sol.set_orientation(position, C, True)
    testing.assert_allclose(sol.pos, position)
    testing.assert_allclose(sol._rot_mat, C)
    testing.assert_allclose(sol.end_pos, position + (height * C * array([[0],
        [0], [1]])))
    testing.assert_allclose(sol.inertia, zeros((3, 3)))

    #TODO: complete tests for solid and the remaining classes in solid.py

def test_stadiumsolid_inertial_properties():
    """Checks the inertial property calculations of the StadiumSolid."""

    density = 1.5
    height = 4
    rad0 = 3
    thick0 = 1
    rad1 = 1
    thick1 = 2

    # Create stadiumsolid using the yeadon package.
    stad1 = Stadium('Ls1: umbilicus', 'thicknessradius', thick0, rad0)
    stad2 = Stadium('Lb1: mid-arm', 'thicknessradius', thick1, rad1)
    solid = StadiumSolid('solid', density, stad1, stad2, height)

    # Create stadiumsolid for checking.
    solid_des = StadiumSolidCheck(density, thick0, rad0, thick1, rad1, height)

    testing.assert_almost_equal(solid.mass, solid_des.mass())
    testing.assert_almost_equal(solid.rel_center_of_mass[2],
            solid_des.mass_center())
    testing.assert_almost_equal(solid.rel_inertia[2, 2], solid_des.inertia_zz())
    testing.assert_almost_equal(solid.rel_inertia[1, 1], solid_des.inertia_yy())
    testing.assert_almost_equal(solid.rel_inertia[0, 0], solid_des.inertia_xx())

    # Switch the order of the stadia and ensure everything still works out.
    solid = StadiumSolid('solid', density, stad2, stad1, height)

    # Create stadiumsolid for checking.
    solid_des = StadiumSolidCheck(density, thick1, rad1, thick0, rad0, height)

    testing.assert_almost_equal(solid.mass, solid_des.mass())
    testing.assert_almost_equal(solid.rel_center_of_mass[2],
            solid_des.mass_center())
    testing.assert_almost_equal(solid.rel_inertia[2, 2], solid_des.inertia_zz())
    testing.assert_almost_equal(solid.rel_inertia[1, 1], solid_des.inertia_yy())
    testing.assert_almost_equal(solid.rel_inertia[0, 0], solid_des.inertia_xx())

def test_stadiumsolidcheck_symmetry():
    """Tests the symmetry of the stadiumsolid formulae, as Yeadon presented
    them (not as implemented). That means, if we switch which stadium we call 0
    or 1, we look at if the mass/volume, center of mass, moments of inertia
    change.

    """
    density = 1.5
    height = 4

    # Same top and bottom.
    r = 3; t = 2;
    solid_desA = StadiumSolidCheck(density, t, r, t, r, height)
    testing.assert_almost_equal(solid_desA.mass(),
            density * height * (4 * r * t + pi * r**2))

    # Diff r, same t.
    r0 = 3; t0 = 2; r1 = 2; t1 = 2;
    solid_desA = StadiumSolidCheck(density, t0, r0, t1, r1, height)
    solid_desB = StadiumSolidCheck(density, t1, r1, t0, r0, height)
    testing.assert_almost_equal(solid_desA.mass(), solid_desB.mass())
    testing.assert_almost_equal(solid_desA.mass_center(),
            height - solid_desB.mass_center())
    testing.assert_almost_equal(solid_desA.inertia_zz(), solid_desB.inertia_zz())
    testing.assert_almost_equal(solid_desA.inertia_yy(), solid_desB.inertia_yy())
    testing.assert_almost_equal(solid_desA.inertia_xx(), solid_desB.inertia_xx())

    # Same r, diff t.
    r0 = 3; t0 = 2; r1 = 3; t1 = 1;
    solid_desA = StadiumSolidCheck(density, t0, r0, t1, r1, height)
    solid_desB = StadiumSolidCheck(density, t1, r1, t0, r0, height)
    testing.assert_almost_equal(solid_desA.mass(), solid_desB.mass())
    testing.assert_almost_equal(solid_desA.mass_center(),
            height - solid_desB.mass_center())
    testing.assert_almost_equal(solid_desA.inertia_zz(), solid_desB.inertia_zz())
    testing.assert_almost_equal(solid_desA.inertia_yy(), solid_desB.inertia_yy())
    testing.assert_almost_equal(solid_desA.inertia_xx(), solid_desB.inertia_xx())

    # Diff r, diff t, one is included in the other.
    r0 = 3; t0 = 2; r1 = 2; t1 = 1;
    solid_desA = StadiumSolidCheck(density, t0, r0, t1, r1, height)
    solid_desB = StadiumSolidCheck(density, t1, r1, t0, r0, height)
    testing.assert_almost_equal(solid_desA.mass(), solid_desB.mass())
    testing.assert_almost_equal(solid_desA.mass_center(),
            height - solid_desB.mass_center())
    testing.assert_almost_equal(solid_desA.inertia_zz(), solid_desB.inertia_zz())
    testing.assert_almost_equal(solid_desA.inertia_yy(), solid_desB.inertia_yy())
    testing.assert_almost_equal(solid_desA.inertia_xx(), solid_desB.inertia_xx())

    # Diff r, diff t, overlap.
    r0 = 3; t0 = 1; r1 = 2; t1 = 5;
    solid_desA = StadiumSolidCheck(density, t0, r0, t1, r1, height)
    solid_desB = StadiumSolidCheck(density, t1, r1, t0, r0, height)
    testing.assert_almost_equal(solid_desA.mass(), solid_desB.mass())
    testing.assert_almost_equal(solid_desA.mass_center(),
            height - solid_desB.mass_center())
    testing.assert_almost_equal(solid_desA.inertia_zz(), solid_desB.inertia_zz())
    testing.assert_almost_equal(solid_desA.inertia_yy(), solid_desB.inertia_yy())
    testing.assert_almost_equal(solid_desA.inertia_xx(), solid_desB.inertia_xx())

def test_degenerate_stadiumsolid_symmetry():
    """Tests the validity, and symmetry, of the stadiumsolid formulae, as
    implemented with the t0 == 0 correction. That means, if we switch which
    stadium we call 0 or 1, we look at if the mass/volume, center of mass,
    moments of inertia change.

    """
    density = 1.5
    height = 4
    height_vec = array([[0], [0], [height]])

    # One thickness is 0.
    r0 = 5; t0 = 0; r1 = 2; t1 = 2;
    # For checking against.
    stad1_des = Stadium('Ls1: umbilicus', 'thicknessradius', 0.000000001, r0)

    stad1 = Stadium('Ls1: umbilicus', 'thicknessradius', t0, r0)
    stad2 = Stadium('Lb1: mid-arm', 'thicknessradius', t1, r1)

    solidA = StadiumSolid('solid', density, stad1_des, stad2, height)
    solidA_des= StadiumSolid('solid', density, stad1, stad2, height)
    solidB = StadiumSolid('solid', density, stad2, stad1_des, height)
    solidB_des = StadiumSolid('solid', density, stad2, stad1, height)

    testing.assert_almost_equal(solidB.mass, solidB_des.mass, decimal=4)
    testing.assert_allclose(solidB.rel_center_of_mass,
            solidB_des.rel_center_of_mass)
    testing.assert_almost_equal(solidB.rel_inertia[0,0],
            solidB_des.rel_inertia[0,0], decimal=4)
    testing.assert_almost_equal(solidB.rel_inertia[1,1],
            solidB_des.rel_inertia[1,1], decimal=4)
    testing.assert_almost_equal(solidB.rel_inertia[2,2],
            solidB_des.rel_inertia[2,2], decimal=4)

    testing.assert_almost_equal(solidA.mass, solidA_des.mass)
    testing.assert_allclose(solidA.rel_center_of_mass,
            solidA_des.rel_center_of_mass)
    testing.assert_almost_equal(solidA.rel_inertia[0,0],
            solidA_des.rel_inertia[0,0], decimal=4)
    testing.assert_almost_equal(solidA.rel_inertia[1,1],
            solidA_des.rel_inertia[1,1], decimal=4)
    testing.assert_almost_equal(solidA.rel_inertia[2,2],
            solidA_des.rel_inertia[2,2], decimal=4)

    testing.assert_almost_equal(solidA.mass, solidB.mass)
    testing.assert_allclose(solidA.rel_center_of_mass,
            height_vec - solidB.rel_center_of_mass)
    testing.assert_almost_equal(solidA.rel_inertia[0,0], solidB.rel_inertia[0,0])
    testing.assert_almost_equal(solidA.rel_inertia[1,1], solidB.rel_inertia[1,1])
    testing.assert_almost_equal(solidA.rel_inertia[2,2], solidB.rel_inertia[2,2])

    # Both thicknesses are zero.
    r0 = 3; t0 = 0; r1 = 2; t1 = 0;
    stad1 = Stadium('Ls1: umbilicus', 'thicknessradius', t0, r0)
    stad2 = Stadium('Lb1: mid-arm', 'thicknessradius', t1, r1)

    solidA = StadiumSolid('solid', density, stad1, stad2, height)
    solidB = StadiumSolid('solid', density, stad2, stad1, height)

    testing.assert_almost_equal(solidA.mass, solidB.mass)
    testing.assert_allclose(solidA.rel_center_of_mass,
            height_vec - solidB.rel_center_of_mass)
    testing.assert_almost_equal(solidA.rel_inertia[0,0], solidB.rel_inertia[0,0])
    testing.assert_almost_equal(solidA.rel_inertia[1,1], solidB.rel_inertia[1,1])
    testing.assert_almost_equal(solidA.rel_inertia[2,2], solidB.rel_inertia[2,2])

    # A third case for when both t0 and t0 are zero.
    # TODO

def test_stadiumsolidcheck_against_truncated_cone():
    """Tests the StadiumSolidCheck formulae above against truncated cone
    formulae for degenerate stadia; using a thin trapezium."""

    def truncated_cone_mass(density, radius0, radius1, height):
        return density / 3.0 * pi * height * (radius0**2 + radius1**2 +
                radius0 * radius1)

    density = 1.5
    height = 4
    rad0 = 3
    thick0 = 0.0000001
    rad1 = 4
    thick1 = 0.0000001

    # Create stadiumsolid for checking.
    solid_des = StadiumSolidCheck(density, thick0, rad0, thick1, rad1, height)

    testing.assert_almost_equal(solid_des.mass(),
            truncated_cone_mass(density, rad0, rad1, height), decimal=4)

    # Now only one level is a circle, so we'll add in an extruded triangle in the
    # middle to find its volume on our own (to check). Radii must be the same
    # for this to work out in the simple case.
    thick0 = 1
    rad1 = 3
    solid_des2 = StadiumSolidCheck(density, thick0, rad0, thick1, rad1, height)

    testing.assert_almost_equal(solid_des2.mass(),
            truncated_cone_mass(density, rad0, rad1, height) +
            density * (2 * thick0 * height * 0.5 * (rad0 * 2)), decimal=4)

def test_rotate_inertia():
    """Are we obtaining the global inertia properly?"""

    density = 1.5
    height = 4
    height_vec = array([[0], [0], [height]])

    # One thickness is 0.
    r0 = 5; t0 = 0; r1 = 2; t1 = 2;

    stad1 = Stadium('Ls1: umbilicus', 'thicknessradius', t0, r0)
    stad2 = Stadium('Lb1: mid-arm', 'thicknessradius', t1, r1)

    solidA = StadiumSolid('solid', density, stad1, stad2, height)

    # This inertia matrix describes two 1kg point masses at (0, 2, 1) and
    # (0, -2, -1) in the global reference frame, A.
    solidA._rel_inertia = mat([[10.0, 0.0, 0.0],
                             [0.0, 2.0, -4.0],
                             [0.0, -4.0, 8.0]])

    # If we want the inertia about a new reference frame, B, such that the
    # two masses lie on the yb axis we can rotate about xa through the angle
    # arctan(1/2). Note that this function returns R from va = R * vb.
    solidA._rot_mat = inertia.rotate_space_123((arctan(1.0 / 2.0), 0.0, 0.0))

    solidA.calc_properties()

    I_b = solidA.inertia

    expected_I_b = mat([[10.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0],
                        [0.0, 0.0, 10.0]])

    testing.assert_allclose(I_b, expected_I_b)
