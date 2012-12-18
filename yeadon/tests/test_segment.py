import unittest
import nose
import numpy as np
from numpy import testing, pi

import yeadon.solid as sol
import yeadon.segment as seg
from yeadon import inertia

class TestSegments(unittest.TestCase):
    """Tests the :py:class:`Segment` class."""

    def setUp(self):
        """Creates the surfaces and solids needed to create a segment."""

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
        """Ensures the constructor for valid input makes correct calculations.

        """
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
        pos2 = np.array([[6], [2], [3]])
        assert (seg1.solids[0].endpos == pos2).all()

        # 2nd solid in the segment.
        assert (seg1.solids[1].pos == pos2).all()
        assert (seg1.solids[1].RotMat == rot).all()
        # See definition of solids in setUp().
        pos3 = pos2 + np.array([[6],[0],[0]])
        assert (seg1.solids[1].endpos == pos3).all()

        # 3rd solid in the segment.
        assert (seg1.solids[2].pos == pos3).all()
        assert (seg1.solids[2].RotMat == rot).all()
        # See definition of solids in setUp().
        pos4 = pos3 + np.array([[7],[0],[0]])
        assert (seg1.solids[2].endpos == pos4).all()

        # Other segment-wide attributes we define.
        assert (seg1.endpos == pos4).all()
        assert (seg1.length == (5 + 6 + 7)).all()

        # -- The constructor then calls calc_rel_properties().
        desMass = self.solidAB.Mass + self.solidBC.Mass + self.solidCD.Mass
        testing.assert_almost_equal(seg1.Mass, desMass)

        desRelCOM = (self.solidAB.Mass * self.solidAB.relCOM +
                self.solidBC.Mass * (
                    self.solidBC.relCOM + np.array([[0, 0, 5]]).T) +
                self.solidCD.Mass * (
                    self.solidCD.relCOM + np.array([[0, 0, 11]]).T)) / desMass
        testing.assert_allclose(seg1.relCOM, desRelCOM);

        relCOM_AB = self.solidAB.relCOM
        relCOM_BC = (np.array([[0, 0, self.solidAB.height]]).T + 
                self.solidBC.relCOM)
        relCOM_CD = (
                np.array([[0, 0, self.solidAB.height+self.solidBC.height]]).T + 
                self.solidCD.relCOM)
        desXInertia = (self.solidAB.relInertia[0, 0] + self.solidAB.Mass * (
                    relCOM_AB[2, 0] - seg1.relCOM[2, 0])**2 +
                self.solidBC.relInertia[0, 0] + self.solidBC.Mass * (
                        relCOM_BC[2, 0] - seg1.relCOM[2, 0])**2 +
                self.solidCD.relInertia[0, 0] + self.solidCD.Mass * (
                        relCOM_CD[2, 0] - seg1.relCOM[2, 0])**2)
        desYInertia = (self.solidAB.relInertia[1, 1] + self.solidAB.Mass * (
                    relCOM_AB[2, 0] - seg1.relCOM[2, 0])**2 +
                self.solidBC.relInertia[1, 1] + self.solidBC.Mass * (
                        relCOM_BC[2, 0] - seg1.relCOM[2, 0])**2 +
                self.solidCD.relInertia[1, 1] + self.solidCD.Mass * (
                        relCOM_CD[2, 0] - seg1.relCOM[2, 0])**2)
        desZInertia = (self.solidAB.relInertia[2, 2] +
                self.solidBC.relInertia[2, 2] + self.solidCD.relInertia[2, 2])
        desRelInertia = np.diag(np.array(
                [desXInertia, desYInertia, desZInertia]))
        testing.assert_allclose(seg1.relInertia, desRelInertia)

    def test_init_bad_input(self):
        """Ensures only proper constructor arguments get through. Exercises
        duck-typing.

        """
        # Create default parameters.
        label = 'seg1'
        pos = np.array([[1], [2], [3]])
        rot = inertia.rotate3([pi / 2, pi / 2, pi / 2])
        solids = [self.solidAB, self.solidBC, self.solidCD]
        color = (1, 0, 0)

        # Empty position.
        self.assertRaises(AttributeError, seg.Segment, label, [], rot, solids,
                color)

        # Non-numpy position.
        self.assertRaises(AttributeError, seg.Segment, label, [0, 0, 0], rot,
                solids, color)

        # Wrong dimensions.
        self.assertRaises(ValueError, seg.Segment, label, pos[1:2,:], rot,
                solids, color)

        # Empty rotation.
        self.assertRaises(ValueError, seg.Segment, label, pos, [], solids,
                color)

        # Wrong type rot.
        self.assertRaises(ValueError, seg.Segment, label, pos, pos, solids,
                color)

        # Wrong dimension rot.
        self.assertRaises(ValueError, seg.Segment, label, pos, np.mat(pos),
                solids, color)

        # Empty solids.
        self.assertRaises(IndexError, seg.Segment, label, pos, rot, [], color)

        # Missing color.
        self.assertRaises(TypeError, seg.Segment, label, pos, rot, solids)

        # Test just having one solid; make sure we do not depend on a segment
        # having multiple solids.
        # Should not raise exception.
        seg1 = seg.Segment(label, pos, rot, [self.solidAB], color)

        # Objects in the solids list are not actually `Solid`'s.
        self.assertRaises(AttributeError, seg.Segment, label, pos, rot, ["1",
            "2"], color)

    def test_calc_properties(self):
        pass

    def test_print_properties(self):
        pass

    def test_print_solid_properties(self):
        pass

    def test_draw(self):
        pass

        # TODO take care of global COM/Inertia.


