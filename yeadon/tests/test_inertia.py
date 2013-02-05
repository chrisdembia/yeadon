#!/usr/bin/env python

from numpy import testing, pi, sin, cos, zeros, mat
from numpy.random import random
from yeadon import inertia

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


#TODO: test parallel_axis
#TODO: test rotate3_inertia
