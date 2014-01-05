'''This module contains a user interface for using and manipulating a Human
object.
 '''
import os

import numpy as np

import inertia

import human as hum

def start_ui():
    print "Starting YEADON user interface."

    measPreload = { 'Ls5L' : 0.545, 'Lb2p' : 0.278, 'La5p' : 0.24, 'Ls4L' :
    0.493, 'La5w' : 0.0975, 'Ls4w' : 0.343, 'La5L' : 0.049, 'Lb2L' : 0.2995,
    'Ls4d' : 0.215, 'Lj2p' : 0.581, 'Lb5p' : 0.24, 'Lb5w' : 0.0975, 'Lk8p' :
    0.245, 'Lk8w' : 0.1015, 'Lj5L' : 0.878, 'La6w' : 0.0975, 'Lk1L' : 0.062,
    'La6p' : 0.2025, 'Lk1p' : 0.617, 'La6L' : 0.0805, 'Ls5p' : 0.375, 'Lj5p' :
    0.2475, 'Lk8L' : 0.1535, 'Lb5L' : 0.049, 'La3p' : 0.283, 'Lj9w' : 0.0965,
    'La4w' : 0.055, 'Ls6L' : 0.152, 'Lb0p' : 0.337, 'Lj8w' : 0.1015, 'Lk2p' :
    0.581, 'Ls6p' : 0.53, 'Lj9L' : 0.218, 'La3L' : 0.35, 'Lj8p' : 0.245, 'Lj3L'
    : 0.449, 'La4p' : 0.1685, 'Lk3L' : 0.449, 'Lb3p' : 0.283, 'Ls7L' : 0.208,
    'Ls7p' : 0.6, 'Lb3L' : 0.35, 'Lk3p' : 0.3915, 'La4L' : 0.564, 'Lj8L' :
    0.1535, 'Lj3p' : 0.3915, 'Lk4L' : 0.559, 'La1p' : 0.2915, 'Lb6p' : 0.2025,
    'Lj6L' : 0.05, 'Lb6w' : 0.0975, 'Lj6p' : 0.345, 'Lb6L' : 0.0805, 'Ls0p' :
    0.97, 'Ls0w' : 0.347, 'Lj6d' : 0.122, 'Ls8L' : 0.308, 'Lk5L' : 0.878,
    'La2p' : 0.278, 'Lj9p' : 0.215, 'Ls1L' : 0.176, 'Lj1L' : 0.062, 'Lb1p' :
    0.2915, 'Lj1p' : 0.617, 'Ls1p' : 0.865, 'Ls1w' : 0.317, 'Lk4p' : 0.34,
    'Lk5p' : 0.2475, 'La2L' : 0.2995, 'Lb4w' : 0.055, 'Lb4p' : 0.1685, 'Lk9p' :
    0.215, 'Lk9w' : 0.0965, 'Ls2p' : 0.845, 'Lj4L' : 0.559, 'Ls2w' : 0.285,
    'Lk6L' : 0.05, 'La7w' : 0.047, 'La7p' : 0.1205, 'La7L' : 0.1545, 'Lk6p' :
    0.345, 'Ls2L' : 0.277, 'Lj4p' : 0.34, 'Lk6d' : 0.122, 'Lk9L' : 0.218,
    'Lb4L' : 0.564, 'La0p' : 0.337, 'Ls3w' : 0.296, 'Ls3p' : 0.905, 'Lb7p' :
    0.1205, 'Lb7w' : 0.047, 'Lj7p' : 0.252, 'Lb7L' : 0.1545, 'Ls3L' : 0.388,
    'Lk7p' : 0.252 }

    # initialize the joint angle data
    # user supplies names/paths of input text files
    print "PROVIDE DATA INPUTS: measurements and configuration (joint angles)."
    print "\nMEASUREMENTS: can be provided as a 95-field dict (units must be " \
          "meters), or a .TXT file"
    temp = raw_input("Type the name of the .TXT filename (to use preloaded "
                    "measurements just hit enter): ")
    if temp == '':
        meas = measPreload
    else:
        file_exist_meas = os.path.exists(temp)
        meas = temp
        while not file_exist_meas:
            temp = raw_input("Please type the correct name of the .TXT filename "
                            "(or just use preloaded measurements just hit enter): ")
            file_exist_meas = os.path.exists(temp)

            if temp == '':
                meas = measPreload
                break
            elif file_exist_meas:
                meas = temp

    print "\nCONFIGURATION (joint angles): can be provided as a 21-field dict,"\
          " or a .TXT file"
    CFG = raw_input("Type the name of the .TXT filename (for all joint angles "
                    "as zero, just hit enter): ")
    # create the human object. only one is needed for this commandline program
    print "Creating human object."

    if CFG == '':
        H = hum.Human(meas)
    else:
        file_exist_CFG = os.path.exists(CFG)
        while not file_exist_CFG:
            CFG = raw_input("Please type the correct name of the .TXT filename "
                            "(for all joint angles as zero, just hit enter): ")
            file_exist_CFG = os.path.exists(CFG)

            if CFG == '':
                H = hum.Human(meas)
                break
            elif file_exist_CFG:
                H = hum.Human(meas, CFG)

    done = 0 # loop end flag

    while done != 1:
        print "\nYEADON MAIN MENU"
        print "----------------"
        print "  j: print/modify joint angles\n\n",\
              "  a: save current joint angles to file\n",\
              "  p: load joint angles from file\n",\
              "  s: format input measurements for ISEG Fortran code\n\n",\
              "  t: transform absolute/base/fixed coordinate system\n\n",\
              "  d: draw 3D human\n\n",\
              "  h: print human properties\n",\
              "  g: print segment properties\n",\
              "  l: print solid properties\n\n",\
              "  c: combine solids/segments for inertia parameters\n\n",\
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

        # TRANSFORM COORDINATE SYSTEM
        elif userIn == 't':
            print "Transforming absolute/base/fixed coordinate system."
            print "First we will rotate the yeadon coordinate system " \
                  "with respect to your new, desired coordinate system. " \
                  "We will first rotate about your x-axis, then your " \
                  "y-axis, then your z-axis."
            thetx = raw_input("Angle (rad) about your x-axis: ")
            thety = raw_input("Angle (rad) about your y-axis: ")
            thetz = raw_input("Angle (rad) about your z-axis: ")
            H.rotate_coord_sys(inertia.rotate_space_123(thetx,thety,thetz))
            print "Now we'll specify the position of yeadon with respect to " \
                  "your coordinate system. You will provide the three " \
                  "components, x y and z, in YOUR coordinates."
            posx = raw_input("X-position (m): ")
            posy = raw_input("Y-position (m): ")
            posz = raw_input("Z-position (m): ")
            H.translate_coord_sys( (posx,posy,posz) )
            print "All done!"

        # DRAW HUMAN WITH MAYAVI
        elif userIn == 'd':
            H.draw()

        # PRINT HUMAN PROPERTIES
        elif userIn == 'h':
            print "\nHuman properties."
            H.print_properties()

        # PRINT SEGMENT PROPERTIES
        elif userIn == 'g':
            print_segment_properties(H)

        # PRINT SOLID PROPERTIES
        elif userIn == 'l':
            print_solid_properties(H)

        # COMBINE INERTIA PARAMETERS
        elif userIn == 'c':
            print "Use the following variables/keywords to select which" \
                  " solids/segments to combine: "
            print "     s0 - s7, a0 - a6, b0 - b6, j0 - j8, k0 - k8"
            print "     P, T, C, A1, A2, B1, B2, J1, J2, K1, K2\n"
            print "Enter in the keywords one at a time. When you are " \
                  "done, enter q."
            combinedone = False
            combinectr = 1
            objlist = []
            while combinedone == False:
                objtemp = raw_input('Solid/segment #' + str(combinectr) + ': ')
                if objtemp == 'q':
                    combinedone = True
                else:
                    objlist.append(objtemp)
                    combinectr += 1
            print "Okay, get ready for your results (mass, COM, Inertia)!"
            combineMass,combineCOM,combineInertia = H.combine_inertia(objlist)
            print "These values are with respect to your fixed frame."
            print "Mass (kg):", combineMass
            print "COM (m):\n", combineCOM
            print "Inertia (kg-m^2):\n", combineInertia

        # OPTIONS
        elif userIn == 'o':
            optionsdone = 0
            sym = ('off','on')
            while optionsdone != 1:
                print "\nOPTIONS"
                print "-------"
                print "  1: toggle symmetry (symmetry is",\
                       sym[ int(H.is_symmetric) ],"now)\n", \
                      "  2: scale human by mass\n", \
                      "  q: back to main menu"
                optionIn = raw_input("What would you like to do? ")
                if optionIn == '1':
                    if H.is_symmetric == True:
                        H.is_symmetric = False
                        H.meas = meas
                    elif H.is_symmetric == False:
                        H.is_symmetric = True
                        H._average_limbs()
                    H.update()
                    print "Symmetry is now turned", sym[int(H.is_symmetric)], "."
                elif optionIn == '2':
                    measmass = raw_input("Provide a measured mass with which "\
                               "to scale the human (kg): ")
                    H.scale_human_by_mass(float(measmass))
                elif optionIn == 'q':
                    print "Going back to main menu."
                    optionsdone = 1
                else:
                    print "Invalid input."
        elif userIn == 'q':
            print "Quitting YEADON"
            done = 1
        else:
            print "Invalid input."


# 3 methods to manage user actions in the main menu (below)
def modify_joint_angles(H):
    '''Called by command-line interaction to modify joint angles. Allows the
    user to first select a joint angle (from the dictionary CFG) to modify.
    Then, the user inputs a new value for that joint angle in units of
    pi-radians. The user continues to modify joint angles until the user quits.
    The user can quit at any time by entering q.

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
    H._update_segments()
    return H

def print_segment_properties(H):
    '''Called by commandline interaction to choose a segment to print the
    properties (mass, center of mass, inertia), and to print those properties.
    See the documentation for the segment class for more information. The user
    can print properties of segments endlessly until entering q.

    '''
    printdone = 0
    while printdone != 1:
        print "\nPRINT SEGMENT PROPERTIES"
        print "------------------------"
        counter = 0
        for seg in H.segments:
            print " ",counter,":",seg.label
            counter += 1
        printIn = raw_input("Enter a segment index to view the properties" \
                            " of (q to quit): ")
        if printIn == 'q':
            printdone = 1
        else:
            print ''
            H.segments[int(printIn)].print_properties()
            print ''
        # error check the input

def print_solid_properties(H):
    '''Called by commandline interaction to print the properties (mass, center
    of mass, inertia) of a solid chosen by user inputs.  The user first selects
    a segment, and then chooses a solid within that segment. Then, the
    properties of that solid are shown. See the documentation for the solid
    class for more information.
    '''
    printdone = 0
    while printdone != 1:
        print "\nPRINT SOLID PROPERTIES"
        print "----------------------"
        counter = 0
        for seg in H.segments:
            print " ",counter,":",seg.label
            counter += 1
        printIn = raw_input("Enter the segment index to view the solid" \
                            " properties of (q to quit): ")
        if printIn == 'q':
            printdone = 1
        else:
            Seg = H.segments[int(printIn)]
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
CFGskydiver = {
             'somersault' : 0.0,
                   'tilt' : 0.0,
                  'twist' : 0.0,
      'PTsagittalFlexion' : 0.0,
              'PTbending' : 0.0,
        'TCspinalTorsion' : 0.0,
'TCsagittalSpinalFlexion' : 0.0,
           'CA1extension' : np.pi/2,
           'CA1adduction' : np.pi/2,
            'CA1rotation' : 0.0,
           'CB1extension' : np.pi/2,
           'CB1abduction' : np.pi/2,
            'CB1rotation' : 0.0,
          'A1A2extension' : np.pi/2,
          'B1B2extension' : np.pi/2,
           'PJ1extension' : np.pi/2,
           'PJ1adduction' : np.pi/2,
           'PK1extension' : np.pi/2,
           'PK1abduction' : np.pi/2,
            'J1J2flexion' : np.pi/2,
            'K1K2flexion' : np.pi/2}

# almost in a bike-riding position
CFGbiker = {
             'somersault' : np.pi/2 * 0.2,
                   'tilt' : 0.0,
                  'twist' : 0.0,
      'PTsagittalFlexion' : np.pi/2 * 0.1,
              'PTbending' : 0.0,
        'TCspinalTorsion' : 0.0,
'TCsagittalSpinalFlexion' : 0.0,
           'CA1extension' : np.pi/4,
           'CA1adduction' : 0.0,
            'CA1rotation' : 0.0,
           'CB1extension' : np.pi/4,
           'CB1abduction' : 0.0,
            'CB1rotation' : 0.0,
          'A1A2extension' : np.pi/4,
          'B1B2extension' : np.pi/4,
           'PJ1extension' : np.pi/2 * 1.2,
           'PJ1adduction' : 0.0,
           'PK1extension' : np.pi/2 * 1.2,
           'PK1abduction' : 0.0,
            'J1J2flexion' : np.pi/2 * 1.2,
            'K1K2flexion' : np.pi/2 * 1.2}

