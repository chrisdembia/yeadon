#!/usr/bin/env python

from numpy import testing, pi, sin, cos
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

#TODO: test parallel_axis
#TODO: test rotate3_inertia
