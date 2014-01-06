# For redirecting stdout.
from cStringIO import StringIO
import sys
import os
import warnings

import unittest
import numpy as np
from numpy import testing, pi, mat, arctan

import yeadon.solid as sol
import yeadon.segment as seg
from yeadon import inertia

warnings.filterwarnings('ignore', category=DeprecationWarning)


class TestSegments(unittest.TestCase):
    """Tests the :py:class:`Segment` class."""

    def setUp(self):
        """Creates the surfaces and solids needed to create a segment."""

        # Make a few surfaces.
        surfA = sol.Stadium('Ls0: hip joint centre', 'perimwidth', 3, 1)
        surfB = sol.Stadium('Ls1: umbilicus', 'depthwidth', 3, 4)
        surfC = sol.Stadium('Ls2: lowest front rib', 'thicknessradius', 5, 6)
        surfD = sol.Stadium('Ls3: nipple', 'perimwidth', 9, 4)
        # Make solids for use with segments.
        self.solidAB = sol.StadiumSolid('stadsolAB', 2, surfA, surfB, 5)
        self.solidBC = sol.StadiumSolid('stadsolBC', 3, surfB, surfC, 6)
        self.solidCD = sol.StadiumSolid('stadsolCD', 4, surfC, surfD, 7)

    def runTest(self):
        # NOTE : This just allows you to run this test from the interpreter.
        pass

    def test_init_real_input(self):
        """Ensures the constructor for valid input makes correct calculations.

        """
        # Create parameters.
        label = 'seg1'
        pos = np.array([[1], [2], [3]])
        rot = inertia.rotate_space_123([pi / 2, pi / 2, pi / 2])
        solids = [self.solidAB, self.solidBC, self.solidCD]
        color = (1, 0, 0)

        # Create the segment.
        seg1 = seg.Segment(label, pos, rot, solids, color)

        # Check that parameters were set.
        assert seg1.label == label
        assert (seg1.pos == pos).all()
        assert (seg1.rot_mat == rot).all()
        assert seg1.solids == solids
        assert seg1.nSolids == len(solids)
        assert seg1.color == color

        # -- Check the other constructor actions.
        # Setting orientations of all constituent solids.
        assert (seg1.solids[0].pos == pos).all()
        assert (seg1.solids[0]._rot_mat == rot).all()
        pos2 = np.array([[6], [2], [3]])
        assert (seg1.solids[0].end_pos == pos2).all()

        # 2nd solid in the segment.
        assert (seg1.solids[1].pos == pos2).all()
        assert (seg1.solids[1]._rot_mat == rot).all()
        # See definition of solids in setUp().
        pos3 = pos2 + np.array([[6],[0],[0]])
        assert (seg1.solids[1].end_pos == pos3).all()

        # 3rd solid in the segment.
        assert (seg1.solids[2].pos == pos3).all()
        assert (seg1.solids[2]._rot_mat == rot).all()
        # See definition of solids in setUp().
        pos4 = pos3 + np.array([[7],[0],[0]])
        assert (seg1.solids[2].end_pos == pos4).all()

        # Other segment-wide attributes we define.
        assert (seg1.end_pos == pos4).all()
        assert (seg1.length == (5 + 6 + 7)).all()

        # -- The constructor then calls calc_rel_properties().
        desMass = self.solidAB.mass + self.solidBC.mass + self.solidCD.mass
        testing.assert_almost_equal(seg1.mass, desMass)

        desRelCOM = (self.solidAB.mass * self.solidAB.rel_center_of_mass +
                self.solidBC.mass * (
                    self.solidBC.rel_center_of_mass + np.array([[0, 0, 5]]).T) +
                self.solidCD.mass * (
                    self.solidCD.rel_center_of_mass + np.array([[0, 0,
                        11]]).T)) / desMass
        testing.assert_allclose(seg1.rel_center_of_mass, desRelCOM);

        # Helper definitions
        relCOM_AB = self.solidAB.rel_center_of_mass
        relCOM_BC = (np.array([[0, 0, self.solidAB.height]]).T +
                self.solidBC.rel_center_of_mass)
        relCOM_CD = (
                np.array([[0, 0, self.solidAB.height+self.solidBC.height]]).T +
                self.solidCD.rel_center_of_mass)

        # Inertia for each direction.
        desXInertia = (self.solidAB.rel_inertia[0, 0] + self.solidAB.mass * (
                    relCOM_AB[2, 0] - seg1.rel_center_of_mass[2, 0])**2 +
                self.solidBC.rel_inertia[0, 0] + self.solidBC.mass * (
                        relCOM_BC[2, 0] - seg1.rel_center_of_mass[2, 0])**2 +
                self.solidCD.rel_inertia[0, 0] + self.solidCD.mass * (
                        relCOM_CD[2, 0] - seg1.rel_center_of_mass[2, 0])**2)
        desYInertia = (self.solidAB.rel_inertia[1, 1] + self.solidAB.mass * (
                    relCOM_AB[2, 0] - seg1.rel_center_of_mass[2, 0])**2 +
                self.solidBC.rel_inertia[1, 1] + self.solidBC.mass * (
                        relCOM_BC[2, 0] - seg1.rel_center_of_mass[2, 0])**2 +
                self.solidCD.rel_inertia[1, 1] + self.solidCD.mass * (
                        relCOM_CD[2, 0] - seg1.rel_center_of_mass[2, 0])**2)
        desZInertia = (self.solidAB.rel_inertia[2, 2] +
                self.solidBC.rel_inertia[2, 2] + self.solidCD.rel_inertia[2, 2])
        # Combine components into array.
        desRelInertia = np.diag(np.array(
                [desXInertia, desYInertia, desZInertia]))
        # Compare.
        testing.assert_allclose(seg1.rel_inertia, desRelInertia)

    def test_init_bad_input(self):
        """Ensures only proper constructor arguments get through. Exercises
        duck-typing.

        """
        # Create default parameters.
        label = 'seg1'
        pos = np.array([[1], [2], [3]])
        rot = inertia.rotate_space_123([pi / 2, pi / 2, pi / 2])
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
        # Wrong dimensions rot.
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
        """Ensures proper calculation of global-frame COM and Inertia."""

        # Create parameters.
        label = 'seg1'
        pos = np.array([[1], [2], [3]])
        rot = inertia.rotate_space_123([pi / 2, pi / 2, pi / 2])
        solids = [self.solidAB, self.solidBC, self.solidCD]
        color = (1, 0, 0)

        # Create the segment.
        seg1 = seg.Segment(label, pos, rot, solids, color)
        seg1.calc_properties()

        testing.assert_allclose(seg1.center_of_mass,
                np.array([[seg1.rel_center_of_mass[2, 0] + 1, 2, 3]]).T)
        desXInertia = seg1.rel_inertia[2, 2]
        desYInertia = seg1.rel_inertia[1, 1]
        desZInertia = seg1.rel_inertia[0, 0]
        desInertia = np.mat(np.diag(np.array(
                [desXInertia, desYInertia, desZInertia])))
        testing.assert_allclose(seg1.inertia, desInertia, atol=1e-10)

    def test_print_properties(self):
        """Ensures the proper printing of segment mass properties. """

        # Create parameters.
        label = 'seg1'
        pos = np.array([[1], [2], [3]])
        rot = inertia.rotate_space_123([pi / 2, pi / 2, pi / 2])
        solids = [self.solidAB, self.solidBC, self.solidCD]
        color = (1, 0, 0)

        # Create the segment.
        seg1 = seg.Segment(label, pos, rot, solids, color)

        # For capturing print.
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        # Calling print_properties before calc_properties should still work.
        seg1.print_properties()
        sys.stdout = old_stdout

        des_str = open(os.path.join(os.path.split(__file__)[0],
            'segment_print_des.txt'), 'r').read()

        self.assertEquals(mystdout.getvalue(), des_str)

        # Use the __str__method.
        # It's just a fluke that we need to append an additional newline char.
        self.assertEquals(seg1.__str__() + '\n', des_str)

    def test_print_solid_properties(self):

        # Create parameters.
        label = 'seg1'
        pos = np.array([[1], [2], [3]])
        rot = inertia.rotate_space_123([pi / 2, pi / 2, pi / 2])
        solids = [self.solidAB, self.solidBC, self.solidCD]
        color = (1, 0, 0)

        # Create the segment.
        seg1 = seg.Segment(label, pos, rot, solids, color)

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        seg1.print_solid_properties()
        sys.stdout = old_stdout
        desStr = open(os.path.join(os.path.split(__file__)[0],
            'segment_print_solid_des.txt'), 'r').read()
        self.assertEquals(mystdout.getvalue(), desStr)

    def test_rotate_inertia(self):
        """Are we obtaining the global inertia properly?"""

        # Create parameters.
        label = 'seg1'
        pos = np.array([[1], [2], [3]])
        rot = inertia.rotate_space_123([pi / 2, pi / 2, pi / 2])
        solids = [self.solidAB, self.solidBC, self.solidCD]
        color = (1, 0, 0)

        # Create the segment.
        seg1 = seg.Segment(label, pos, rot, solids, color)

        # This inertia matrix describes two 1kg point masses at (0, 2, 1) and
        # (0, -2, -1) in the global reference frame, A.
        seg1._rel_inertia = mat([[10.0, 0.0, 0.0],
                                 [0.0, 2.0, -4.0],
                                 [0.0, -4.0, 8.0]])

        # If we want the inertia about a new reference frame, B, such that the
        # two masses lie on the yb axis we can rotate about xa through the angle
        # arctan(1/2). Note that this function returns R from va = R * vb.
        seg1._rot_mat = inertia.rotate_space_123((arctan(1.0 / 2.0), 0.0, 0.0))

        seg1.calc_properties()

        I_b = seg1.inertia

        expected_I_b = mat([[10.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0],
                            [0.0, 0.0, 10.0]])

        testing.assert_allclose(I_b, expected_I_b)
