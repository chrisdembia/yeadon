import numpy as np
#mymath

# unit vector; useful for locating segments
zunit = np.array([[0],[0],[1]])

def Rotate3(angles):
	'''Produces a three-dimensional rotation matrix as rotations around the three cartesian axes.
	
	Parameters
	----------
	angles : numpy.array or list or tuple, shape(3,)
		Three angles (in units of radians) that specify the orientation of a new reference frame with respect to a fixed reference frame. The first angle is a pure rotation about the x-axis, the second about the y-axis, and the third about the z-axis. All rotations are with respect to the initial fixed frame, and they occur in the order x, then y, then z.
		
	Returns
	-------
	R : numpy.matrix, shape(3,3)
		Three dimensional rotation matrix about three different orthogonal axes.
	'''
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

	return Rz*Ry*Rx
	
def RotateRel(angles):
	'''The three-dimensional relative rotation matrix from Yeadon 1989-i used to describe the orientation of a human with respect to a fixed frame.
	
	Parameters
	----------
	angles : numpy.array or list or tuple, shape(3,)
		Three angles (in units of radians) that specify the orientation of a new reference frame with respect to a fixed reference frame. The first angle, phi, is a rotation about the fixed frame's x-axis. The second angle, theta, is a rotation about the new y-axis (which is realized after the phi rotation). The third angle, psi, is a rotation about the new z-axis (which is realized after the theta rotation). Thus, all three angles are "relative" rotations with respect to the new frame. Note: if the rotations are viewed as occuring in the opposite direction (z, then y, then x), all three rotations are with respect to the initial fixed frame rather than "relative".
		
	Returns
	-------
	R : numpy.matrix, shape(3,3)
		Three dimensional rotation matrix about three different orthogonal axes.
	'''
	cphi = np.cos(angles[0])
	sphi= np.sin(angles[0])

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
		         
	return R1*R2*R3

def RotateInertia(RotMat,relInertia):
	'''Rotates an inertia tensor. A derivation of the formula in this function can be found in Crandall 1968, Dynamics of mechanical and electromechanical systems. This function only transforms an inertia tensor for rotations with respect to a fixed point. To translate an inertia tensor, one must use the parallel axis analogue for tensors. An inertia tensor contains both moments of inertia and products of inertia for a mass in a cartesian (xyz) frame.
	
	Parameters
	----------
	RotMat : numpy.matrix, shape(3,3)
		Three-dimensional rotation matrix specifying the coordinate frame that the input inertia tensor is in, with respect to a fixed coordinate system in which one desires to express the inertia tensor.
	relInertia : numpy.matrix, shape(3,3)
		Three-dimensional cartesian inertia tensor describing the inertia of a mass in a rotated coordinate frame.
				 
	Returns
	-------
	Inertia : numpy.matrix, shape(3,3) 
		Inertia tensor with respect to a fixed coordinate system ("unrotated").

	'''
	return RotMat * relInertia * RotMat.T
