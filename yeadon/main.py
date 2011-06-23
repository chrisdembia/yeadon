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
measurements = 0;
# WHAT ARE THE JOINT LIMITS?
DOF = {      'somersalt' : 0.0,
	              'tilt' : 0.0,
     	         'twist' : 0.0,
	 'PTsagittalFlexion' : 0.0,
      'PTfrontalFlexion' : 0.0,
       'TCspinalTorsion' : 0.0,
'TClateralSpinalFlexion' : 0.0,
          'CA1elevation' : 0.0,
          'CA1abduction' : 0.0,
           'CA1rotation' : 0.0,
          'CB1elevation' : 0.0,
          'CB1abduction' : 0.0,
           'CB1rotation' : 0.0,
           'A1A2flexion' : 0.0,
           'B1B2flexion' : 0.0,
            'PJ1flexion' : 0.0,
          'PJ1abduction' : 0.0,
            'PK1flexion' : 0.0,
          'PK1abduction' : 0.0,
           'J1J2flexion' : 0.0,
           'K1K2flexion' : 0.0}  
                 
print "Creating human object."
H = hum.human(measurements,DOF)

H.draw()

H.printProperties()

# INTERACT WITH THE USER



DOF = {      'somersalt' : np.pi/4,
	              'tilt' : np.pi/4,
     	         'twist' : np.pi/4,
	 'PTsagittalFlexion' : 0.0,
      'PTfrontalFlexion' : 0.0,
       'TCspinalTorsion' : 0.0,
'TClateralSpinalFlexion' : 0.0,
          'CA1elevation' : np.pi/2,
          'CA1abduction' : np.pi/2,
           'CA1rotation' : 0.0,
          'CB1elevation' : np.pi/2,
          'CB1abduction' : np.pi/2,
           'CB1rotation' : 0.0,
           'A1A2flexion' : np.pi/2,
           'B1B2flexion' : np.pi/2,
            'PJ1flexion' : np.pi/2,
          'PJ1abduction' : np.pi/2,
            'PK1flexion' : np.pi/2,
          'PK1abduction' : np.pi/2,
           'J1J2flexion' : np.pi/2,
           'K1K2flexion' : np.pi/2}        

DOF = {      'somersalt' : np.pi/2 * 0.2,
	              'tilt' : 0.0,
     	         'twist' : 0.0,
	 'PTsagittalFlexion' : np.pi/2 * 0.1,
      'PTfrontalFlexion' : 0.0,
       'TCspinalTorsion' : 0.0,
'TClateralSpinalFlexion' : 0.0,
          'CA1elevation' : np.pi/4,
          'CA1abduction' : 0.0,
           'CA1rotation' : 0.0,
          'CB1elevation' : np.pi/4,
          'CB1abduction' : 0.0,
           'CB1rotation' : 0.0,
           'A1A2flexion' : np.pi/4,
           'B1B2flexion' : np.pi/4,
            'PJ1flexion' : np.pi/2 * 1.2,
          'PJ1abduction' : 0.0,
            'PK1flexion' : np.pi/2 * 1.2,
          'PK1abduction' : 0.0,
           'J1J2flexion' : np.pi/2 * 1.2,
           'K1K2flexion' : np.pi/2 * 1.2}   


















