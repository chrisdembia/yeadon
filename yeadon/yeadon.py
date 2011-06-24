import human as hum
import numpy as np
import measurements as meas

# INPUTS ARE 95 MEASUREMENTS, DENSITIES, AND ORIENTATION ANGLES

print "Starting YEADON."

# SECOND ITERATION: MOVE FROM FILE INPUTS (FOR ANGLES ONLY) TO QT GUI

# initialize the joint angle data
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

# methods to manage user actions in the main menu (below)
def modifyJointAngles():
	'''Called by command-line interaction to modify joint angles. Allows the user to first select a joint angle (from the dictionary DOF) to modify. Then, the user inputs a new value for that joint angle in units of pi-radians. The user continues to modify joint angles until the user quits. The user can quit at any time by entering q.
	'''
	# MUST UPDATE THE DRAW, etc.
	done = 0
	counter = 0
	while done != 1:
		counter += 1
		print "MODIFY JOINT ANGLES"
		print "-------------------"
		for i in np.arange(len(H.DOFnames)):
			print " ",i,":",H.DOFnames[i],"=",DOF[H.DOFnames[i]]/np.pi,"pi-rad"
		if counter == 1:
			idxIn = raw_input("Enter the number next to the joint angle to modify (q to quit): ")
		else:
			idxIn = raw_input("Modify another joint angle (q to quit):")
		if idxIn == 'q':
			done = 1
		else:
			valueIn = raw_input("Enter the new value for the joint angle in units of pi-rad (q to quit): ")
			if valueIn == 'q':
				done = 1
			else:
				DOF[ H.DOFnames[int(idxIn)] ] = float(valueIn) * np.pi
				while H.validateDOFs() == -1:
					valueIn = raw_input("Re-enter a value for this joint: ")
					DOF[ H.DOFnames[int(idxIn)] ] = float(valueIn) * np.pi

	H.DOF = DOF
	H.updateSegments()

def printSegmentProperties():
	'''EDIT
	'''
	printdone = 0
	while printdone != 1:
		print "\nPRINT SEGMENT PROPERTIES"
		print "------------------------"
		counter = 0
		for seg in H.Segments:
			print " ",counter,":",seg.label
			counter += 1
		printIn = raw_input("Enter a segment index to view the properties of (q to quit): ")
		if printIn == 'q':
			printdone = 1
		else:
			print ''
			H.Segments[int(printIn)].printProperties()
			print ''
		# error check the input

def printSolidProperties():
	'''EDIT.
	'''
	printdone = 0
	while printdone != 1:
		print "\nPRINT SOLID PROPERTIES"
		print "----------------------"
		counter = 0
		for seg in H.Segments:
			print " ",counter,":",seg.label
			counter += 1
		printIn = raw_input("Enter the segment index to view the solid properties of (q to quit): ")
		if printIn == 'q':
			printdone = 1
		else:
			Seg = H.Segments[int(printIn)]
			soldone = 0
			while soldone != 1:
				print "Solids in segment",Seg.label
				counter = 0
				for sol in Seg.solids:
					print " ",counter,":",sol.label
					counter += 1
				printIn = raw_input("Enter the solid index to view parameters of (q to quit): ")
				if printIn == 'q':
					soldone = 1
				else:
					print ''
					Seg.solids[int(printIn)].printProperties()
					print ''

print "Creating human object."

H = hum.human(meas,DOF)

#>>> print 'We are the {} who say "{}!"'.format('knights', 'Ni')
#We are the knights who say "Ni!"

done = 0
frames = ('Yeadon','bike')
frame = 0
nonfr = 1
while done != 1:
	print "\nYEADON MAIN MENU"
	print "----------------"
	print "  m: print/modify solid dimensions\n  j: print/modify joint angles\n  a: save current joint angles to file\n  d: draw human\n  h: print human properties\n  g: print segment properties\n  l: print solid properties\n  f: use",frames[nonfr],"coordinates\n  b: bike mode\n  o: options\n  q: quit"

	userIn = raw_input("What would you like to do next? ")
	print ""
	
	# MODIFY SOLID DIMENSIONS
	if userIn == 'm':
		print "Main menu option m is not implemented yet."
		
	# MODIFY JOINT ANGLES
	elif userIn == 'j':
		modifyJointAngles()
		
	# SAVE CURRENT JOINT ANGLES
	elif userIn == 'a':
		print "Not implemented yet"
		
	# DRAW HUMAN
	elif userIn == 'd':
		print "To continue using the YEADON after drawing, close the plot window."
		H.draw()
		
	# PRINT HUMAN PROPERTIES
	elif userIn == 'h':
		print "\nHuman properties using",frames[frame],"coordinate system:\n"
		H.printProperties()
		
	# PRINT SEGMENT PROPERTIES
	elif userIn == 'g':
		printSegmentProperties()	
		
	# PRINT SOLID PROPERTIES	
	elif userIn == 'l':
		printSolidProperties()
		
	# USE COORDINATES
	elif userIn == 'f':
		if frame == 0:
			frame = 1
			nonfr = 0
		elif frame == 1:
			frame = 0
			nonfr = 1

	# BIKE MODE
	elif userIn == 'b':
		print "Bike mode is not implemented yet."

	# OPTIONS
	elif userIn == 'o':
		optionsdone = 0
		sym = ['off','on']
		while optionsdone != 1:
			print "\nOPTIONS"
			print "-------"
			print "  1: toggle symmetric inertia parameters (symmetry is",sym[ H.isSymmetric ],"now)\n  q: back to main menu"
			optionIn = raw_input("What would you like to do? ")
			if optionIn == '1':
				if H.isSymmetric == 1:
					H.isSymmetrc = 0
				elif H.isSymmetric == 0:
					H.isSymmetric = 1
				print "Symmetric inertia parameters are now turned",sym,"."
			elif optionIn == 'q':
				print "Going back to main menu."
				optionsdone = 1
			else:
				print "Invalid input"
	elif userIn == 'q':
		print "Quitting YEADON"
		done = 1
	else:
		print "Invalid input"

# other sets of joint angles
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

