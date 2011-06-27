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
        The moment of inertia about of the body about a point located by d.

    '''
    a = d[0]
    b = d[1]
    c = d[2]
    dMat = np.zeros((3, 3), dtype=object)
    dMat[0] = np.array([b**2 + c**2, -a * b, -a * c])
    dMat[1] = np.array([-a * b, c**2 + a**2, -b * c])
    dMat[2] = np.array([-a * c, -b * c, a**2 + b**2])
    return Ic + m * dMat

def inertia_components(jay, beta):
    '''Returns the 2D orthogonal inertia tensor.

    When at least three moments of inertia and their axes orientations are
    known relative to a common inertial frame of a planar object, the orthoganl
    moments of inertia relative the frame are computed.

    Parameters
    ----------
    jay : ndarray, shape(n,)
        An array of at least three moments of inertia. (n >= 3)
    beta : ndarray, shape(n,)
        An array of orientation angles corresponding to the moments of inertia
        in jay.

    Returns
    -------
    eye : ndarray, shape(3,)
        Ixx, Ixz, Izz

    '''
    sb = np.sin(beta)
    cb = np.cos(beta)
    betaMat = np.matrix(np.vstack((cb**2, -2 * sb * cb, sb**2)).T)
    eye = np.squeeze(np.asarray(np.dot(betaMat.I, jay)))
    return eye

def tube_inertia(l, m, ro, ri):
    '''Calculate the moment of inertia for a tube (or rod) where the x axis is
    aligned with the tube's axis.

    Parameters
    ----------
    l : float
        The length of the tube.
    m : float
        The mass of the tube.
    ro : float
        The outer radius of the tube.
    ri : float
        The inner radius of the tube. Set this to zero if it is a rod instead
        of a tube.

    Returns
    -------
    Ix : float
        Moment of inertia about tube axis.
    Iy, Iz : float
        Moment of inertia about normal axis.

    '''
    Ix = m / 2. * (ro**2 + ri**2)
    Iy = m / 12. * (3 * ro**2 + 3 * ri**2 + l**2)
    Iz = Iy
    return Ix, Iy, Iz
    
def cylinder_inertia(l, m, ro, ri):
    '''Calculate the moment of inertia for a hollow cylinder (or solid cylinder) where the x axis is
    aligned with the cylinder's axis.

    Parameters
    ----------
    l : float
        The length of the cylinder.
    m : float
        The mass of the cylinder.
    ro : float
        The outer radius of the cylinder.
    ri : float
        The inner radius of the cylinder. Set this to zero for a solid cylinder.

    Returns
    -------
    Ix : float
        Moment of inertia about cylinder axis.
    Iy, Iz : float
        Moment of inertia about cylinder axis.

    '''
    Ix = m / 2. * (ro**2 + ri**2)
    Iy = m / 12. * (3 * ro**2 + 3 * ri**2 + l**2)
    Iz = Iy
    return Ix, Iy, Iz

def total_com(coordinates, masses):
    '''Returns the center of mass of a group of objects if the indivdual
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

    '''
    products = masses * coordinates
    mT = np.sum(masses)
    cT = np.sum(products, axis=1) / mT
    return mT, cT

def rotate_inertia_tensor(I, angle):
    '''Returns inertia tensor rotated through angle. Only for 2D'''
    ca = np.cos(angle)
    sa = np.sin(angle)
    C    =  np.array([[ca, 0., -sa],
                      [0., 1., 0.],
                      [sa, 0., ca]])
    Irot =  np.dot(C, np.dot(I, C.T))
    return Irot
