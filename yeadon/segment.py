'''Segment objects are used by the human module. A segment has a position, and
an orientation. All constituent solids of a segment have the same orientation.
That is to say that the base of the segment is at a joint in the human. The
user does not interact with this module.

'''
import numpy as np

import inertia # jason moore's

class segment:
    def __init__(self, label, pos, RotMat, solids, color):
        '''Initializes a segment object. Stores inputs as instance variables,
        calculates the orientation of the segment's child solids, and
        calculates the "relative" inertia parameters (mass, center of mass
        and inertia) of the segment.

        Parameters
        ----------
        label : str
            The ID and name of the segment.
        pos : numpy.array, shape(3,1)
            The vector position of the segment's base,
            with respect to the fixed human frame.
        Rotmat : numpy.matrix, shape(3,3)
            The orientation of the segment is given by a rotation matrix that
            specifies the orientation of the segment with respect to the fixed
            human frame.
        solids : list of solid objects
            The solid objects that compose the segment
        color : tuple (3,)
            Color with which to plot this segment in the plotting functions.
            RGB tuple with float values between 0 and 1.

        '''
        self.label = label
        self.pos = pos
        self.RotMat = RotMat
        self.solids = solids
        self.nSolids = len(self.solids)
        self.color = color
        # must set the position of constituent solids before being able to
        # calculate relative/local properties.
        self.set_orientations()
        self.endpos = self.solids[-1].endpos
        self.length = np.linalg.norm(self.endpos-self.pos)
        self.calc_rel_properties()


    def set_orientations(self):
        '''Sets the position (self.pos) and rotation matrix (self.RotMat)
        for all solids in the segment by calling each constituent
        solid's set_orientation method. The position of the i-th solid,
        expressed in the fixed human reference frame, is given by the sum
        of the segment's base position and the directed height of all the
        solids of the segment up to the i-th solid.

        '''
        # pos and RotMat for first solid
        self.solids[0].set_orientation(self.pos, self.RotMat)
        # pos and RotMat for remaining solids
        for i in np.arange(self.nSolids):
            if i != 0:
                pos = self.solids[i-1].endpos
                self.solids[i].set_orientation(pos, self.RotMat)

    def calc_rel_properties(self):
        '''Calculates the mass, relative/local center of mass, and
        relative/local inertia tensor (about the segment's center of mass).
        Also computes the center of mass of each constituent solid with
        respect to the segment's base in the segment's reference frame.

        '''
        # mass
        self.Mass = 0.0
        for s in self.solids:
            self.Mass += s.Mass
        # relative position of each solid w.r.t. segment orientation and
        # segment's origin
        self.solidpos = []
        self.solidpos.append(np.zeros((3, 1)))
        for i in np.arange(self.nSolids):
            if i != 0:
                self.solidpos.append( self.solidpos[i-1] +
                                      self.solids[i-1].height *
                                      np.array([[0, 0, 1]]).T)
        # center of mass of each solid w.r.t. segment orientation and
        # segment's origin
        self.solidCOM = []
        self.solidCOM.append(self.solids[0].relCOM)
        for i in np.arange(self.nSolids):
            if i != 0:
                self.solidCOM.append( self.solidpos[i] +
                                      self.solids[i].relCOM)
        # relative center of mass
        relmoment = np.zeros((3, 1))
        for i in np.arange(self.nSolids):
            relmoment += self.solids[i].Mass * self.solidCOM[i]
        self.relCOM = relmoment / self.Mass
        # relative Inertia
        self.relInertia = np.mat(np.zeros((3, 3)))
        for i in np.arange(self.nSolids):
            dist = self.solidCOM[i] - self.relCOM
            self.relInertia += np.mat(inertia.parallel_axis(
                                      self.solids[i].relInertia,
                                      self.solids[i].Mass,
                                      [dist[0, 0], dist[1, 0], dist[2, 0]]))

    def calc_properties(self):
        '''Calculates the segment's center of mass with respect to the
        fixed human frame origin (in the fixed human reference frame) and the
        segment's inertia in the fixed human frame but about the segment's
        center of mass.

        '''
        # center of mass
        self.COM = self.pos + self.RotMat * self.relCOM
        # inertia in frame f w.r.t. segment's COM
        self.Inertia = inertia.rotate3_inertia(self.RotMat, self.relInertia)
        # an alternative way of calculating absolute inertia tensor,
        # implemented for validation purposes.
        # inertia in frame f w.r.t. segment's COM
        self.Inertia2 = np.mat(np.zeros((3, 3)))
        for s in self.solids:
            dist = s.COM - self.COM
            self.Inertia2 += np.mat(inertia.parallel_axis(
                                    s.Inertia, s.Mass,
                                    [dist[0, 0], dist[1, 0], dist[2, 0]]))

    def print_properties(self):
        '''Prints mass, center of mass (in segment's and fixed human frames),
        and inertia (in segment's and fixed human frames).

        '''
        print self.label, "properties:\n"
        print "Mass (kg):", self.Mass, "\n"
        print "COM in local segment frame (m):\n", self.relCOM, "\n"
        print "COM in fixed human frame (m):\n", self.COM, "\n"
        print "Inertia tensor in segment frame about local segment",\
               "COM (kg-m^2):\n", self.relInertia, "\n"
        print "Inertia tensor in fixed human frame about local segment",\
               "COM (kg-m^2):\n", self.Inertia, "\n"

    def print_solid_properties(self):
        '''Calls the print_properties() member method of each of this
        segment's solids. See the solid class's definition of
        print_properties(self) for more detail.

        '''
        for s in self.solids:
            s.print_properties()

    def draw(self, ax):
        '''Draws all the solids within a segment using matplotlib.

        '''
        for idx in np.arange(self.nSolids):
            print "Drawing solid", self.solids[idx].label, "."
            self.solids[idx].draw(ax, self.color)
        u = np.linspace( 0, 2*np.pi, 30)
        v = np.linspace( 0, np.pi, 30)
        R = 0.03
        x = R * np.outer(np.cos(u), np.sin(v)) + self.COM[0, 0]
        y = R * np.outer(np.sin(u), np.sin(v)) + self.COM[1, 0]
        z = R * np.outer(np.ones(np.size(u)), np.cos(v)) + self.COM[2, 0]
        ax.plot_surface(x, y, z,  rstride=4, cstride=4, edgecolor='',
                        color='r')

    def draw2D(self, ax, ax2):
        '''Draws in two dimensions all the solids within this segment using
        matplotlib. Does not perform well.

        '''
        for idx in np.arange(self.nSolids):
            print "Drawing solid", self.solids[idx].label, "."
            self.solids[idx].draw2D(ax, ax2, self.color)

    def draw_visual(self):
        '''Draws in a 3D VPython window all the solids within this segment.

        '''
        for s in self.solids:
            s.draw_visual(self.color)
