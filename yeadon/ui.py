'''This module contains a user interface for using and manipulating a Human object.
 '''

import human as hum
import numpy as np

def start_ui():
    print "Starting YEADON user interface."
    
    measnames = ('Ls1L','Ls2L','Ls3L','Ls4L','Ls5L','Ls6L','Ls7L',
                 'Ls8L','Ls0p','Ls1p','Ls2p','Ls3p','Ls5p','Ls6p',
                 'Ls7p','Ls0w','Ls1w','Ls2w','Ls3w','Ls4w','Ls4d',                               'La2L','La3L','La4L','La5L','La6L','La7L','La0p',
                 'La1p','La2p','La3p','La4p','La5p','La6p','La7p',
                 'La4w','La5w','La6w','La7w',
                 'Lb2L','Lb3L','Lb4L','Lb5L','Lb6L','Lb7L','Lb0p',
                 'Lb1p','Lb2p','Lb3p','Lb4p','Lb5p','Lb6p','Lb7p',
                 'Lb4w','Lb5w','Lb6w','Lb7w',
                 'Lj1L','Lj3L','Lj4L','Lj5L','Lj6L','Lj8L','Lj9L',
                 'Lj1p','Lj2p','Lj3p','Lj4p','Lj5p','Lj6p','Lj7p',
                 'Lj8p','Lj9p','Lj8w','Lj9w','Lj6d', 
                 'Lk1L','Lk3L','Lk4L','Lk5L','Lk6L','Lk8L','Lk9L',
                 'Lk1p','Lk2p','Lk3p','Lk4p','Lk5p','Lk6p','Lk7p',
                 'Lk8p','Lk9p','Lk8w','Lk9w','Lk6d')
   # measvals =  (   2.0,   2.8,   5.8,   8.8,   9.4,   1.0,   2.0,
    #                3.6,   5.3,   4.8,   5.6,   ,    3.,    3.,
                     
    # initialize the joint angle data
    # USER SUPPLIES MEASUREMENT FILE NAME
    print "PROVIDE DATA INPUTS: measurements and configuration (joint angles)."
    print "MEASUREMENTS: can be provided as a 95-field dict (units must be " \
          "meters), or a .TXT file"
    temp = raw_input("Type the name of the dict variable "\
                     "or the .TXT filename (to use preloaded measurements," \
                     " just hit enter): ")
    if temp == '':
        meas = measPreload
    else:
        meas = temp
    print "CONFIGURATION (joint angles): can be provided as a 21-field dict,"\
          " or a .TXT file"
    CFG = raw_input("Type the name of the dict variable "\
                    "or the .TXT filename (for all joint angles as zero," \
                    " just hit enter): ") 
    # create the human object. only one is needed for this commandline program
    print "Creating human object."
    if CFG == '':
        H = hum.human(meas)
    else:
        H = hum.human(meas,CFG)
    
    #>>> print 'We are the {} who say "{}!"'.format('knights', 'Ni')
    #We are the knights who say "Ni!"
    
    done = 0 # loop end flag
    
    # used for changing the reference frame of...everything.
    frames = ('Yeadon','bike')
    frame = 0
    nonfr = 1
    while done != 1:
        print "\nYEADON MAIN MENU"
        print "----------------"
        print "  j: print/modify joint angles\n\n",\
              "  a: save current joint angles to file\n",\
              "  p: load joint angles from file\n",\
              "  s: format input measurements for ISEG Fortran code\n\n",\
              "  d: draw human\n\n",\
              "  h: print human properties\n",\
              "  g: print segment properties\n",\
              "  l: print solid properties\n\n",\
              "  c: combine solids/segments for inertia\n\n",\
              "  f: use",frames[nonfr],"coordinates\n",\
              "  o: options\n",\
              "  q: quit"
    
        userIn = raw_input("What would you like to do next? ")
        print ""
        
        # MODIFY JOINT ANGLES
        if userIn == 'j':
            # this function is defined above
            H = modify_joint_angles(H)
            
        # SAVE CURRENT JOINT ANGLES
        elif userIn == 'a':
            fname = raw_input("The joint angle dictionary CFG will be pickled" \
                              " into a file saved in the current directory." \
                              " Specify a file name (without quotes or spaces," \
                              " q to quit): ")
            if fname != 'q':
                H.write_CFG(fname)
                print "The joint angles have been saved in",fname,".pickle."
    
        # LOAD JOINT ANGLES
        elif userIn == 'p':
            print "Be careful with this, because there is no error checking"\
                  " yet. Make sure that the pickle file is in the same format"\
                  " as a pickle output file from this program."
            fname = raw_input("Enter the name of a CFG .TXT file" \
                              " including its extension" \
                              " (q to quit):")
            if fname != 'q':
                H.read_CFG(fname)
                print "The joint angles in",fname,".pickle have been loaded."
    
        # FORMAT INPUT MEASUREMENTS FOR ISEG FORTRAN CODE
        elif userIn == 's':
            fname = raw_input("Enter the file name to which you would like" \
                              " to write the ISEG input: ")
            if H.write_meas_for_ISEG(fname) == 0:
                print "Success!"
            else:
                print "Uh oh, there was an error when trying to write",\
                       "the ISEG input."
            
        # DRAW HUMAN
        elif userIn == 'd':
            print "To continue using the YEADON UI after drawing,",\
                   "close the plot window."
            H.draw()
            
        # PRINT HUMAN PROPERTIES
        elif userIn == 'h':
            print "\nHuman properties using",frames[frame],\
                  "coordinate system:\n"
            H.print_properties()
            
        # PRINT SEGMENT PROPERTIES
        elif userIn == 'g':
            print_segment_properties(H)    
            
        # PRINT SOLID PROPERTIES    
        elif userIn == 'l':
            print_solid_properties(H)
            
        # USE COORDINATES. see initialized variables above while-loop
        # for more info.
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
                print "  1: toggle symmetric inertia parameters (symmetry is",\
                       sym[ H.isSymmetric ],"now)\n  q: back to main menu"
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
    
    
# 3 methods to manage user actions in the main menu (below)
def modify_joint_angles(H):
    '''Called by command-line interaction to modify joint angles. Allows the 
       user to first select a joint angle (from the dictionary CFG) to modify.
       Then, the user inputs a new value for that joint angle in units of
       pi-radians. The user continues to modify joint angles until the user
       quits. The user can quit at any time by entering q.

    '''
    # MUST UPDATE THE DRAW, etc.
    done = 0
    counter = 0
    while done != 1:
        counter += 1
        CFG = H.CFG
        print "MODIFY JOINT ANGLES"
        print "-------------------"
        for i in np.arange(len(H.CFGnames)):
            print " ",i,":",H.CFGnames[i],"=",CFG[H.CFGnames[i]]/np.pi,"pi-rad"
        if counter == 1:
            idxIn = raw_input("Enter the number next to the joint angle" \
                              " to modify (q to quit): ")
        else:
            idxIn = raw_input("Modify another joint angle (q to quit):")
        if idxIn == 'q':
            done = 1
        else:
            valueIn = raw_input("Enter the new value for the joint angle" \
                                " in units of pi-rad (q to quit): ")
            if valueIn == 'q':
                done = 1
            else:
                CFG[H.CFGnames[int(idxIn)]] = float(valueIn) * np.pi
                while H.validate_CFG() == -1:
                    valueIn = raw_input("Re-enter a value for this joint: ")
                    CFG[H.CFGnames[int(idxIn)]] = float(valueIn) * np.pi

    H.CFG = CFG
    H.update_segments()
    return H

def print_segment_properties(H):
    '''Called by commandline interaction to choose a segment to print the
       properties (mass, center of mass, inertia), and to print those
       properties. See the documentation for the segment class for more
       information. The user can print properties of segments endlessly until
       entering q. 
    '''
    printdone = 0
    while printdone != 1:
        print "\nPRINT SEGMENT PROPERTIES"
        print "------------------------"
        counter = 0
        for seg in H.Segments:
            print " ",counter,":",seg.label
            counter += 1
        printIn = raw_input("Enter a segment index to view the properties" \
                            " of (q to quit): ")
        if printIn == 'q':
            printdone = 1
        else:
            print ''
            H.Segments[int(printIn)].print_properties()
            print ''
        # error check the input

def print_solid_properties(H):
    '''Called by commandline interaction to print the properties 
       (mass, center of mass, inertia) of a solid chosen by user inputs.
       The user first selects a segment, and then chooses a solid within that
       segment. Then, the properties of that solid are shown. See the
       documentation for the solid class for more information.
    '''
    printdone = 0
    while printdone != 1:
        print "\nPRINT SOLID PROPERTIES"
        print "----------------------"
        counter = 0
        for seg in H.Segments:
            print " ",counter,":",seg.label
            counter += 1
        printIn = raw_input("Enter the segment index to view the solid" \
                            " properties of (q to quit): ")
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
                printIn = raw_input("Enter the solid index" \
                                    " to view parameters of (q to quit): ")
                if printIn == 'q':
                    soldone = 1
                else:
                    print ''
                    Seg.solids[int(printIn)].print_properties()
                    print ''

# other sets of joint angles

# this one was for fun; looks like a skydiver
CFGskydiver = {      'somersalt' : 0.0,
                  'tilt' : 0.0,
                  'twist' : 0.0,
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

# almost in a bike-riding position
CFGbiker = {      'somersalt' : np.pi/2 * 0.2,
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

