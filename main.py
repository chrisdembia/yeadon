import stadium as stad
#import segment
import human as hum
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import data
import densities


# INPUTS ARE 95 MEASUREMENTS, DENSITIES, AND ORIENTATION ANGLES


# read input file of 95 measurements
# create solid objects
# create segment objects
# create human object
# plot human, no angles

# read in angles file
# plot human, with joint angles

# plot human conforming to a bicycle


# SECOND ITERATION: MOVE FROM FILE INPUTS (FOR ANGLES ONLY) TO QT GUI


externalangles = np.zeros( 3 ) # 0: somersalt, 1: tilt, 2: twist
externalangles[0] = 0
jointangles = np.zeros( 18 )
PTangles = np.zeros( 2 ) # 0: sagittal flexion, 1: frontal flexion
# PTangles[0] = np.pi/10
# PTangles[1] = np.pi/10

TCangles = np.zeros( 2 ) # 0: spinal torsion, 1: lateral spinal flexion
#TCangles[0] = np.pi/5
TCangles[1] = 0

CA1angles = np.zeros( 3 )
CB1angles = np.zeros( 3 )
A1A2angle = 0
B1B2angle = 0
PJ1angles = np.zeros( 2 )
PK1angles = np.zeros( 2 )
J1J2angle = 0
K1K2angle = 0
print "Creating human object."
H = hum.human(externalangles, PTangles, TCangles, CA1angles, CB1angles, A1A2angle, B1B2angle, PJ1angles, PK1angles, J1J2angle, K1K2angle)
H.draw()
