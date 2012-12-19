#!/usr/bin/env python

from numpy import testing, pi, array, matrix, sin, cos, zeros
from yeadon.solid import Stadium, Solid

# TODO Test Stadium negative radius/thickness issue in constructor.

def test_stadium():

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
    testing.assert_almost_equal(dw.thickness, thickness_from_depth_width(depth,
        width))
    testing.assert_almost_equal(dw.perimeter, perimeter_from_depth_width(depth,
        width))

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

    #TODO: Add testing for Stadium.plot

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
    # Likins, Levinson, 1982
    C = matrix([[c2 * c3, s1 * s2 * c3 + s3 * c1, -c1 * s2 * c3 + s3 * s1],
                [-c2 * s3, -s1 * s2 * s3 + c3 * c1, c1 * s2 * s3 + c3 *s1],
                [s2, -s1 * c2, c1 * c2]])

    sol.set_orientation(position, C)
    testing.assert_allclose(sol.pos, position)
    testing.assert_allclose(sol.rot_mat, C)
    testing.assert_allclose(sol.endpos, position + (height * C * array([[0],
        [0], [1]])))
    testing.assert_allclose(sol.Inertia, zeros((3, 3)))

    #TODO: complete tests for solid and the remaining classes in solid.py
