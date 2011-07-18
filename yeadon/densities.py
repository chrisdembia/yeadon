'''This script sets the densities to be used in the yeadon segments. 
There are three density sets to choose from: Chandler, Dempster, and
Clauser. On average, the Dempster densities are slightly higher than the
other densities.

'''
import numpy as np

# densities come from Yeadon 1990-ii, but really from Dempster 1995

# raw units from the paper are kg/L

LitersPerCubicMeter = 1000.0
secondconversion = 1.0

DensityOfSegments = np.zeros( 10 )

densityset = 'Dempster'

if densityset == 'Chandler':
    DensityOfSegments[0] = 1.056 # head-neck
    DensityOfSegments[1] = 0.853 # shoulders
    DensityOfSegments[2] = 0.853 # thorax
    DensityOfSegments[3] = 0.853 # abdomen-pelvis
    DensityOfSegments[4] = 1.005 # upper arm
    DensityOfSegments[5] = 1.052 # forearm
    DensityOfSegments[6] = 1.080 # hand
    DensityOfSegments[7] = 1.020 # thigh
    DensityOfSegments[8] = 1.078 # lower leg
    DensityOfSegments[9] = 1.091 # foot
elif densityset == 'Dempster':
    DensityOfSegments[0] = 1.11 # head-neck
    DensityOfSegments[1] = 1.04 # shoulders
    DensityOfSegments[2] = 0.92 # thorax
    DensityOfSegments[3] = 1.01 # abdomen-pelvis
    DensityOfSegments[4] = 1.07 # upper arm
    DensityOfSegments[5] = 1.13 # forearm
    DensityOfSegments[6] = 1.16 # hand
    DensityOfSegments[7] = 1.05 # thigh
    DensityOfSegments[8] = 1.09 # lower leg
    DensityOfSegments[9] = 1.10 # foot
elif densityset == 'Clauser':
    DensityOfSegments[0] = 1.070 # head-neck
    DensityOfSegments[1] = 1.019 # shoulders
    DensityOfSegments[2] = 1.019 # thorax
    DensityOfSegments[3] = 1.019 # abdomen-pelvis
    DensityOfSegments[4] = 1.056 # upper arm
    DensityOfSegments[5] = 1.089 # forearm
    DensityOfSegments[6] = 1.109 # hand
    DensityOfSegments[7] = 1.044 # thigh
    DensityOfSegments[8] = 1.085 # lower leg
    DensityOfSegments[9] = 1.084 # foot


DensityOfSegmentsConverted = DensityOfSegments * LitersPerCubicMeter * secondconversion

# torso
Ds = np.zeros( 8 )
Ds[0] = DensityOfSegmentsConverted[3]
Ds[1] = DensityOfSegmentsConverted[3]
Ds[2] = DensityOfSegmentsConverted[2]
Ds[3] = DensityOfSegmentsConverted[2]
Ds[4] = DensityOfSegmentsConverted[1]
Ds[5] = DensityOfSegmentsConverted[0]
Ds[6] = DensityOfSegmentsConverted[0]
Ds[7] = DensityOfSegmentsConverted[0]

# left arm
Da = np.zeros( 7 )
Da[0] = DensityOfSegmentsConverted[4]
Da[1] = DensityOfSegmentsConverted[4]
Da[2] = DensityOfSegmentsConverted[5]
Da[3] = DensityOfSegmentsConverted[5]
Da[4] = DensityOfSegmentsConverted[6]
Da[5] = DensityOfSegmentsConverted[6]
Da[6] = DensityOfSegmentsConverted[6]

# right arm
Db = Da.copy()
# Db1 = Da1 # = DensityOfSegmentsConverted[4]
# Db2 = Da2 # = DensityOfSegmentsConverted[4]
# Db3 = Da3 # = DensityOfSegmentsConverted[5]
# Db4 = Da4 # = DensityOfSegmentsConverted[5]
# Db5 = Da5 # = DensityOfSegmentsConverted[6]
# Db6 = Da6 # = DensityOfSegmentsConverted[6]
# Db7 = Da7 # = DensityOfSegmentsConverted[6]

# left leg
Dj = np.zeros( 9 )
Dj[0] = DensityOfSegmentsConverted[7]
Dj[1] = DensityOfSegmentsConverted[7]
Dj[2] = DensityOfSegmentsConverted[7]
Dj[3] = DensityOfSegmentsConverted[8]
Dj[4] = DensityOfSegmentsConverted[8]
Dj[5] = DensityOfSegmentsConverted[9]
Dj[6] = DensityOfSegmentsConverted[9]
Dj[7] = DensityOfSegmentsConverted[9]
Dj[8] = DensityOfSegmentsConverted[9]

# right leg
Dk = Dj.copy()
# Dk1 = Dj1 # = DensityOfSegmentsConverted[7]
# Dk2 = Dj2 # = DensityOfSegmentsConverted[7]
# Dk3 = Dj3 # = DensityOfSegmentsConverted[7]
# Dk4 = Dj4 # = DensityOfSegmentsConverted[8]
# Dk5 = Dj5 # = DensityOfSegmentsConverted[8]
# Dk6 = Dj6 # = DensityOfSegmentsConverted[9]
# Dk7 = Dj7 # = DensityOfSegmentsConverted[9]
# Dj8 = Dj8 # = DensityOfSegmentsConverted[9]
# Dj9 = Dj9 # = DensityOfSegmentsConverted[9]

# print "Segment densities loaded."



























