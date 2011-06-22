# mymath
import numpy as np

zunit = np.array([[0],[0],[1]])

def Rotate3(angles):
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
	
def RotateExternal(angles):
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
