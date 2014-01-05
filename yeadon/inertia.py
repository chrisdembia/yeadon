# Use Python3 integer division rules.
from __future__ import division

import warnings

import numpy as np

from .exceptions import YeadonDeprecationWarning

# Display our warnings to the user.
warnings.simplefilter('always', YeadonDeprecationWarning)


def parallel_axis(Ic, m, d):
    '''Returns the moment of inertia of a body about a different point.

    Parameters
    ----------
    Ic : array_like, shape(3,3)
        The moment of inertia about the center of mass of the body with
        respect to an orthogonal coordinate system.
    m : float
        The mass of the body.
    d : array_like, shape(3,) or shape(3, 1) or shape(1, 3)
        The distances along the x, y, and z axes that locate the new point
        relative to the center of mass of the body.

    Returns
    -------
    I : numpy.matrix, shape(3,3)
        The moment of inertia of a body about a point located by the
        distances in `d`.

    '''

    Ic = np.asmatrix(Ic)
    d = np.asmatrix(d).reshape((3, 1))

    a = d[0, 0]
    b = d[1, 0]
    c = d[2, 0]

    dMat = np.zeros((3, 3), dtype=Ic.dtype)

    dMat[0] = np.array([b ** 2 + c ** 2, -a * b, -a * c])
    dMat[1] = np.array([-a * b, c ** 2 + a ** 2, -b * c])
    dMat[2] = np.array([-a * c, -b * c, a ** 2 + b ** 2])

    return Ic + m * dMat


def rotate_space_123(angles):
    """Returns the direction cosine matrix relating a reference frame B
    rotated relative to reference frame A through the x, y, then z axes of
    reference frame A (spaced fixed rotations).

    Parameters
    ----------
    angles : numpy.array or list or tuple, shape(3,)
        Three angles (in units of radians) that specify the orientation of
        a new reference frame with respect to a fixed reference frame.
        The first angle is a pure rotation about the x-axis, the second about
        the y-axis, and the third about the z-axis. All rotations are with
        respect to the initial fixed frame, and they occur in the order x,
        then y, then z.

    Returns
    -------
    R : numpy.matrix, shape(3,3)
        Three dimensional rotation matrix about three different orthogonal axes.

    Notes
    -----

    R = |c2 * c3    s1 * s2 * c3 - s3 * c1   c1 * s2 * c3 + s3 * s1|
        |c2 * s3    s1 * s2 * s3 + c3 * c1   c1 * s2 * s3 - c3 * s1|
        |-s2        s1 * c2                  c1 * c2               |

    where

    s1, s2, s3 = sine of the first, second and third angles, respectively
    c1, c2, c3 = cosine of the first, second and third angles, respectively

    So the unit vector b1 in the B frame can be expressed in the A frame (unit
    vectors a1, a2, a3) with:

    b1 = c2 * c3 * a1 + c2 * s3 * a2 - s2 * a3

    Thus a vector vb which is expressed in frame B can be expressed in A by
    pre-multiplying by R:

    va = R * vb

    """
    cx = np.cos(angles[0])
    sx = np.sin(angles[0])

    cy = np.cos(angles[1])
    sy = np.sin(angles[1])

    cz = np.cos(angles[2])
    sz = np.sin(angles[2])

    Rz = np.mat([[ cz,-sz,  0],
                 [ sz, cz,  0],
                 [  0,  0,  1]])

    Ry = np.mat([[ cy,  0, sy],
                 [  0,  1,  0],
                 [-sy,  0, cy]])

    Rx = np.mat([[  1,  0,  0],
                 [  0, cx, -sx],
                 [  0, sx,  cx]])

    return Rz * Ry * Rx

def euler_123(angles):
    """
    Returns the direction cosine matrix of rotated frame B with respect to
    frame A as a function of the Euler 123 angles (body fixed rotation).

    Parameters
    ----------
    angles : array_like, shape(3,)
        Three angles (in units of radians) that specify the orientation of a
        new reference frame, B, with respect to a fixed reference frame, A. The
        first angle, phi, is a rotation about the fixed frame's x-axis. The
        second angle, theta, is a rotation about the new y-axis (which is
        realized after the phi rotation). The third angle, psi, is a rotation
        about the new z-axis (which is realized after the theta rotation).
        Thus, all three angles are "relative" rotations with respect to each
        new frame.  Note: if the rotations are viewed as occuring in the
        opposite direction (z, then y, then x), all three rotations are with
        respect to the initial fixed frame rather than "relative".

    Returns
    -------
    R : numpy.matrix, shape(3,3)
        Three dimensional rotation matrix about three different orthogonal axes.

    Notes
    -----

    R = | c2 * c3                  -c2 * s3                   s2     |
        | s1 * s2 * c3 + s3 * c1   -s1 * s2 * s3 + c3 * c1   -s1 * c2|
        |-c1 * s2 * c3 + s3 * s1    c1 * s2 * s3 + c3 * s1    c1 * c2|

    where

    s1, s2, s3 = sine of the first, second, and third angles, respectively
    c1, c2, c3 = cosine of the first, second, and third angles, respectively

    So the unit vector b1 in the B frame can be expressed in the A frame (unit
    vectors a1, a2, a3) with:

    b1 = c2 * c3 * a1 + (s1 * s2 * c3 + s3 * c1) * a2 +
         (-c1 * c2 * c3 + s3 * s1) * a3

    The rotation matrix is defined such that a R times a vector v_b in the
    rotated reference frame equals the same vector, v_a, expressed in the
    unrotated reference frame.

        R * v_b = v_a

    Where v_a is the vector expressed in the original fixed reference frame and
    v_b is the same vector expressed in the rotated reference frame.

    """

    cphi = np.cos(angles[0])
    sphi = np.sin(angles[0])

    cthe = np.cos(angles[1])
    sthe = np.sin(angles[1])

    cpsi = np.cos(angles[2])
    spsi = np.sin(angles[2])

    R1 = np.mat([[     1,     0,     0],
                 [     0,  cphi, -sphi],
                 [     0,  sphi,  cphi]])

    R2 = np.mat([[  cthe,     0,  sthe],
                 [     0,     1,     0],
                 [ -sthe,     0,  cthe]])

    R3 = np.mat([[  cpsi,  -spsi,     0],
                 [  spsi,  cpsi,     0],
                 [     0,     0,     1]])

    return R1 * R2 * R3


def rotate3_inertia(rotation_matrix, inertia):

    __doc__ = rotate_inertia.__doc__

    # TODO : Remove this function in Yeadon 2.0.

    msg = ("rotate3_inertia has been renamed to rotate_inertia, this " +
           "function signature will be removed in Yeadon 2.0.")
    warnings.warn(msg, YeadonDeprecationWarning)

    return rotate_inertia(rotation_matrix, inertia)


def rotate_inertia(rotation_matrix, inertia):
    """Returns an inertia tensor expressed in a reference frame which has
    been rotated with respect to the frame the inertia tensor is currently
    expressed in.

    Parameters
    ----------
    rotation_matrix : numpy.matrix, shape(3,3)
        Three-dimensional rotation/transformation/direction-cosine matrix
        that transforms a vector in the rotated reference frame into one in
        the current reference frame.
    inertia : numpy.matrix, shape(3,3)
        Three-dimensional cartesian tensor describing the inertia of a rigid
        body in a reference frame.

    Returns
    -------
    rotated_inertia : numpy.matrix, shape(3,3)
        The inertia tensor expressed in the rotated reference frame.

    Notes
    -----

    The provided inertia tensor is expressed in a reference frame, A, and
    there is a reference frame, B, which is rotated with respect to A such
    that a vector, v, expressed in B as v_b can be expressed in A as v_a by
    pre-multiplying by the rotation matrix, R:

    v_a = R * v_b

    Angular momentum of a rigid body expressed in A is defined as:

    H_a = I_a * w_a

    where H_a and w_a are the angular momentum and angular rate vectors,
    respectively and I_a is the inertia tensor, all expressed in A.
    Expressing H_a and w_a in B gives:

    R * H_b = I_a * R * w_b

    R * I_b * w_b = I_a * R * w_b

    So,

    R * I_b = I_a * R

    and thus:

    I_b = R^T * I_a * R

    """
    return rotation_matrix.T * inertia * rotation_matrix


def total_com(coordinates, masses):
    """
    Returns the center of mass of a group of objects if the indivdual
    centers of mass and mass is provided.

    coordinates : ndarray, shape(3,n)
        The rows are the x, y and z coordinates, respectively and the columns
        are for each object.
    masses : ndarray, shape(3,)
        An array of the masses of multiple objects, the order should correspond
        to the columns of coordinates.

    Returns
    -------
    mT : float
        Total mass of the objects.
    cT : ndarray, shape(3,)
        The x, y, and z coordinates of the total center of mass.

    """
    products = masses * coordinates
    mT = np.sum(masses)
    cT = np.sum(products, axis=1) / mT
    return mT, cT

def principal_axes(I):
    """
    Returns the principal moments of inertia and the orientation.

    Parameters
    ----------
    I : ndarray, shape(3,3)
        An inertia tensor.

    Returns
    -------
    Ip : ndarray, shape(3,)
        The principal moments of inertia. This is sorted smallest to largest.
    C : ndarray, shape(3,3)
        The rotation matrix.

    """
    Ip, C = np.linalg.eig(I)
    indices = np.argsort(Ip)
    Ip = Ip[indices]
    C = C.T[indices]
    return Ip, C
