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


externalangles = np.zeros( 3 )
externalangles[0] = 0
jointangles = np.zeros( 18 )

print "Creating human object."
H = hum.human(externalangles)
H.draw()
