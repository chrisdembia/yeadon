import unittest
import nose
import numpy as np
from numpy import testing, pi

import yeadon.solid as sol
import yeadon.segment as seg
from yeadon import inertia

class TestSegments(unittest.TestCase):

    def setUp(self):
        # Make a few surfaces.
        surfA = sol.Stadium('surfA', 'perimwidth', 3, 1)
        surfB = sol.Stadium('surfB', 'depthwidth', 3, 4)
        surfC = sol.Stadium('surfC', 'thickradius', 5, 6)
        surfD = sol.Stadium('surfD', 'perimwidth', 9, 4)
        # Make solids for use with segments.
        self.solidAB = sol.StadiumSolid('stadsolAB', 2, surfA, surfB, 5)
        self.solidBC = sol.StadiumSolid('stadsolBC', 3, surfB, surfC, 6)
        self.solidCD = sol.StadiumSolid('stadsolCD', 4, surfC, surfD, 7)

    def test_init_real_input(self):
        # Create parameters.
        label = 'seg1'
        pos = np.array([[1], [2], [3]])
        rot = inertia.rotate3([pi / 2, pi / 2, pi / 2])
        solids = [self.solidAB, self.solidBC, self.solidCD]
        color = (1, 0, 0)

        # Create the segment.
        seg1 = seg.Segment(label, pos, rot, solids, color)

        # Check that parameters were set.
        assert seg1.label == label
        assert (seg1.pos == pos).all()
        assert (seg1.RotMat == rot).all()
        assert seg1.solids == solids
        assert seg1.nSolids == len(solids)
        assert seg1.color == color

        # -- Check the other constructor actions.
        # Setting orientations of all constituent solids.
        assert (seg1.solids[0].pos == pos).all()
        assert (seg1.solids[0].RotMat == rot).all()
        print seg1.solids[0].endpos
        assert (seg1.solids[0].endpos == np.array([[6], [2], [3]])).all()

    def test_init_bad_input(self):
        # Ensures only proper input gets through.
        # pos = np.array([1, 2, 3]) <-- NOT OKAY, but internal.
        pass


