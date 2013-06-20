#!/usr/bin/env python

from numpy import testing, pi, sin, cos, zeros, mat
from numpy.random import random
from yeadon import inertia

def test_euler_rotation(display=False):
    # body-three 1-2-3
    a = [15., 0., 0.]
    order = (1, 2, 3)
    R = inertia.euler_rotation(a, order)
    C = mat([[1., 0., 0.],
             [0., cos(a[0]), sin(a[0])],
             [0., -sin(a[0]), cos(a[0])]])
    if display:
        print "body-three 1-2-3"
        print R
        print C
        print '-' * 79

    testing.assert_almost_equal(R, C)

    # body-three 1-2-3
    a = [0.34, 23.6, -0.2]
    c1 = cos(a[0])
    c2 = cos(a[1])
    c3 = cos(a[2])
    s1 = sin(a[0])
    s2 = sin(a[1])
    s3 = sin(a[2])

    order = (1, 2, 3)
    R = inertia.euler_rotation(a, order)

    # definition of body 1-2-3 rotations from Spacecraft Dynamics, Kane,
    # Likins, Levinson, 1982 page 423 (this is the transpose of what is
    # presented)
    C = mat([[c2 * c3, s1 * s2 * c3 + s3 * c1, -c1 * s2 * c3 + s3 * s1],
             [-c2 * s3, -s1 * s2 * s3 + c3 * c1, c1 * s2 * s3 + c3 *s1],
             [s2, -s1 * c2, c1 * c2]])

    if display:
        print "body-three 1-2-3"
        print R
        print C
        print '-' * 79

    testing.assert_almost_equal(R, C)

    # test 3-1-3
    a = [1., 1.1, 1.2]
    c1 = cos(a[0])
    c2 = cos(a[1])
    c3 = cos(a[2])
    s1 = sin(a[0])
    s2 = sin(a[1])
    s3 = sin(a[2])

    order = (3, 1, 3)

    R = inertia.euler_rotation(a, order)

    # definition of body 3-1-3 rotations from Spacecraft Dynamics, Kane,
    # Likins, Levinson, 1982 page 424 (this is the transpose of what is
    # presented)
    C = mat([[-s1 * c2 * s3 + c3 * c1, c1 * c2 * s3 + c3 *s1, s2 *s3],
             [-s1 * c2 * c3 - s3 * c1, c1 * c2 * c3 - s3 * s1, s2 * c3],
             [s1 * s2, -c1 * s2, c2]])
    if display:
        print "body-two 3-1-"
        print R
        print C
        print '-' * 79

    testing.assert_almost_equal(R, C)

    # test 1-3-2
    a = [0.234, 0.0004, 0.50505]
    c1 = cos(a[0])
    c2 = cos(a[1])
    c3 = cos(a[2])
    s1 = sin(a[0])
    s2 = sin(a[1])
    s3 = sin(a[2])

    order = (1, 3, 2)

    R = inertia.euler_rotation(a, order)

    # definition of body-three 1-3-2 rotations from Spacecraft Dynamics, Kane,
    # Likins, Levinson, 1982 page 423 (this is the transpose of what is
    # presented)

    C = mat([[c2 * c3, c1 * s2 * c3 + s3 * s1, s1 * s2 * c3 - s3 * c1],
             [-s2, c1 * c2, s1 * c2],
             [c2 * s3, c1 * s2 * s3 - c3 * s1, s1 * s2 * s3 + c3 * c1]])

    if display:
        print '-' * 79
        print "body-three 1-3-2"
        print R
        print C

    testing.assert_almost_equal(R, C)

    # test 2-1-3
    a = [0.234, 0.0004, 0.50505]
    c1 = cos(a[0])
    c2 = cos(a[1])
    c3 = cos(a[2])
    s1 = sin(a[0])
    s2 = sin(a[1])
    s3 = sin(a[2])

    order = (2, 1, 3)

    R = inertia.euler_rotation(a, order)

    # definition of body 2-1-3 rotations from Spacecraft Dynamics, Kane,
    # Likins, Levinson, 1982 page 423 (this is the transpose of what is
    # presented)

    C = mat([[s1 * s2 * s3 + c3 * c1, c2 * s3, c1 * s2 * s3 - c3 * s1],
             [s1 * s2 * c3 - s3 * c1, c2 * c3, c1 * s2 * c3 + s3 * s1],
             [s1 * c2, -s2, c1 * c2]])

    if display:
        print '-' * 79
        print "body-three 2-1-3"
        print R
        print C
    testing.assert_almost_equal(R, C)

def test_rotations():
    angles = pi * random(3)

    s1 = sin(angles[0])
    s2 = sin(angles[1])
    s3 = sin(angles[2])

    c1 = cos(angles[0])
    c2 = cos(angles[1])
    c3 = cos(angles[2])

    R = [[c2 * c3, s1 * s2 * c3 - s3 * c1, c1 * s2 * c3 + s3 * s1],
         [c2 * s3, s1 * s2 * s3 + c3 * c1, c1 * s2 * s3 - c3 * s1],
         [-s2, s1 * c2, c1 * c2]]

    testing.assert_allclose(R, inertia.rotate_space_123(angles))

    R = [[c2 * c3, -c2 * s3, s2],
         [s1 * s2 * c3 + s3 * c1, -s1 * s2 * s3 + c3 * c1, -s1 * c2],
         [-c1 * s2 * c3 + s3 * s1, c1 * s2 * s3 + c3 * s1, c1 * c2]]

    testing.assert_allclose(R, inertia.euler_123(angles))

    angles = -pi * random(3)

    s1 = sin(angles[0])
    s2 = sin(angles[1])
    s3 = sin(angles[2])

    c1 = cos(angles[0])
    c2 = cos(angles[1])
    c3 = cos(angles[2])

    R = [[c2 * c3, s1 * s2 * c3 - s3 * c1, c1 * s2 * c3 + s3 * s1],
         [c2 * s3, s1 * s2 * s3 + c3 * c1, c1 * s2 * s3 - c3 * s1],
         [-s2, s1 * c2, c1 * c2]]

    testing.assert_allclose(R, inertia.rotate_space_123(angles))

    R = [[c2 * c3, -c2 * s3, s2],
         [s1 * s2 * c3 + s3 * c1, -s1 * s2 * s3 + c3 * c1, -s1 * c2],
         [-c1 * s2 * c3 + s3 * s1, c1 * s2 * s3 + c3 * s1, c1 * c2]]

    testing.assert_allclose(R, inertia.euler_123(angles))

def test_parallel_axis():
    """Only covers the case that the inertia tensor is diagonal."""

    inertia1 = mat(zeros((3, 3)))
    inertia1[0, 0] = 5
    inertia1[1, 1] = 6
    inertia1[2, 2] = 7

    # Moving 3 unit over on the x-axis.
    dpos = [3, 0, 0]
    inertia2 = inertia.parallel_axis(inertia1, 1, dpos)
    testing.assert_almost_equal(inertia2[0, 0], inertia1[0, 0])
    testing.assert_almost_equal(inertia2[1, 1], inertia1[1, 1] + dpos[0]**2)
    testing.assert_almost_equal(inertia2[2, 2], inertia1[2, 2] + dpos[0]**2)

    dpos = [0, 4, 0]
    inertia2 = inertia.parallel_axis(inertia1, 1, dpos)
    testing.assert_almost_equal(inertia2[1, 1], inertia1[1, 1])
    testing.assert_almost_equal(inertia2[0, 0], inertia1[0, 0] + dpos[1]**2)
    testing.assert_almost_equal(inertia2[2, 2], inertia1[2, 2] + dpos[1]**2)

    dpos = [0, 0, 5]
    inertia2 = inertia.parallel_axis(inertia1, 1, dpos)
    testing.assert_almost_equal(inertia2[2, 2], inertia1[2, 2])
    testing.assert_almost_equal(inertia2[0, 0], inertia1[0, 0] + dpos[2]**2)
    testing.assert_almost_equal(inertia2[1, 1], inertia1[1, 1] + dpos[2]**2)

    dpos = [3, 4, 5]
    inertia2 = inertia.parallel_axis(inertia1, 1, dpos)
    testing.assert_almost_equal(inertia2[0, 0],
            inertia1[0, 0] + dpos[1]**2 + dpos[2]**2)
    testing.assert_almost_equal(inertia2[1, 1],
            inertia1[1, 1] + dpos[0]**2 + dpos[2]**2)
    testing.assert_almost_equal(inertia2[2, 2],
            inertia1[2, 2] + dpos[0]**2 + dpos[1]**2)


#TODO: test parallel_axis, additional (non-diagonal) cases
#TODO: test rotate3_inertia
