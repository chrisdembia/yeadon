#!/usr/bin/env python

# standard lib
import warnings

# external
from numpy import testing, pi, sin, cos, zeros, mat, arctan
from numpy.random import random

# local
from .. import inertia

# Don't show deprecation warnings when running tests.
warnings.filterwarnings('ignore', category=DeprecationWarning)

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

# TODO : test parallel_axis, additional (non-diagonal) cases


def test_rotate_inertia():
    """Ensures that expressing an inertia tensor with respect to another
    frame is correct."""

    # Note that I_b = R^T * I_a * R where R is defined such that v_a = R *
    # v_b.

    I_a = mat([[1.0, 0.0, 0.0],
               [0.0, 2.0, 0.0],
               [0.0, 0.0, 3.0]])

    # Space fixed rotation 231 about -pi/2, pi/2, 0
    R = mat([[0.0, -1.0, 0.0],
             [0.0, 0.0, -1.0],
             [1.0, 0.0, 0.0]])

    I_b = inertia.rotate_inertia(R, I_a)

    expected_I_b = mat([[3.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0],
                        [0.0, 0.0, 2.0]])

    testing.assert_allclose(I_b, expected_I_b)

    # Make an arbitrary inertia tensor and rotate through Space fixed 123
    # angles: pi, pi / 2, and pi. This will make xb = -z_a, y_b = y_a, and
    # z_b = x_a.

    I_a = mat([[1.0, 4.0, 5.0],
               [4.0, 2.0, 6.0],
               [5.0, 6.0, 3.0]])

    R = inertia.rotate_space_123((pi, pi / 2, pi))

    I_b = inertia.rotate_inertia(R, I_a)

    expected_I_b = mat([[3.0, -6.0, -5.0],
                        [-6.0, 2.0, 4.0],
                        [-5.0, 4.0, 1.0]])

    testing.assert_allclose(I_b, expected_I_b)

    # This inertia matrix describes two 1kg point masses at (0, 2, 1) and
    # (0, -2, -1) in the global reference frame, A.
    I_a = mat([[10.0, 0.0, 0.0],
               [0.0, 2.0, -4.0],
               [0.0, -4.0, 8.0]])

    # If we want the inertia about a new reference frame, B, such that the
    # two masses lie on the yb axis we can rotate about xa through the angle
    # arctan(1/2). Note that this function returns R from va = R * vb.
    R = inertia.rotate_space_123((arctan(1.0 / 2.0), 0.0, 0.0))

    I_b = inertia.rotate_inertia(R, I_a)

    expected_I_b = mat([[10.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0],
                        [0.0, 0.0, 10.0]])

    testing.assert_allclose(I_b, expected_I_b)
