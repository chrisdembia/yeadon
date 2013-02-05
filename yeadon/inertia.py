# Use Python3 integer division rules.
from __future__ import division

import numpy as np

def parallel_axis(Ic, m, d):
    '''Returns the moment of inertia of a body about a different point.

    Parameters
    ----------
    Ic : ndarray, shape(3,3)
        The moment of inertia about the center of mass of the body with respect
        to an orthogonal coordinate system.
    m : float
        The mass of the body.
    d : ndarray, shape(3,)
        The distances along the three ordinates that located the new point
        relative to the center of mass of the body.

    Returns
    -------
    I : ndarray, shape(3,3)
        The moment of inertia of a body about a point located by the distances
        in d.

    '''
    a = d[0]
    b = d[1]
    c = d[2]
    dMat = np.zeros((3, 3), dtype=Ic.dtype)
    dMat[0] = np.array([b**2 + c**2, -a * b, -a * c])
    dMat[1] = np.array([-a * b, c**2 + a**2, -b * c])
    dMat[2] = np.array([-a * c, -b * c, a**2 + b**2])
    return Ic + m * dMat

def rotate_space_123(angles):
    """
    Returns the direction cosine matrix relating a reference frame B rotated
    relative to reference frame A through the x, y, then z axes of reference
    frame A (spaced fixed rotations).

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
    Returns the direction cosine matrix as a function of the Euler 123 angles
    (body fixed rotation).

    Parameters
    ----------
    angles : numpy.array or list or tuple, shape(3,)
        Three angles (in units of radians) that specify the orientation of a
        new reference frame with respect to a fixed reference frame. The first
        angle, phi, is a rotation about the fixed frame's x-axis. The second
        angle, theta, is a rotation about the new y-axis (which is realized
        after the phi rotation). The third angle, psi, is a rotation about the
        new z-axis (which is realized after the theta rotation). Thus, all
        three angles are "relative" rotations with respect to the new frame.
        Note: if the rotations are viewed as occuring in the opposite direction
        (z, then y, then x), all three rotations are with respect to the
        initial fixed frame rather than "relative".

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

    s1, s2, s3 = sine of the first, second and third angles, respectively
    c1, c2, c3 = cosine of the first, second and third angles, respectively

    So the unit vector b1 in the B frame can be expressed in the A frame (unit
    vectors a1, a2, a3) with:

    b1 = c2 * c3 * a1 + (s1 * s2 * c3 + s3 * c1) * a2 +
         (-c1 * c2 * c3 + s3 * s1) * a3

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

def rotate3_inertia(rot_mat, relInertia):
    """
    Rotates an inertia tensor. A derivation of the formula in this function
    can be found in Crandall 1968, Dynamics of mechanical and electromechanical
    systems. This function only transforms an inertia tensor for rotations with
    respect to a fixed point. To translate an inertia tensor, one must use the
    parallel axis analogue for tensors. An inertia tensor contains both moments
    of inertia and products of inertia for a mass in a cartesian (xyz) frame.

    Parameters
    ----------
    rot_mat : numpy.matrix, shape(3,3)
        Three-dimensional rotation matrix specifying the coordinate frame that
        the input inertia tensor is in, with respect to a fixed coordinate
        system in which one desires to express the inertia tensor.
    relInertia : numpy.matrix, shape(3,3)
        Three-dimensional cartesian inertia tensor describing the inertia of a
        mass in a rotated coordinate frame.

    Returns
    -------
    Inertia : numpy.matrix, shape(3,3)
        Inertia tensor with respect to a fixed coordinate system ("unrotated").

    """
    return rot_mat * relInertia * rot_mat.T

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
