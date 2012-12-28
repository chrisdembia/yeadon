import unittest
import nose
import numpy as np
from numpy import testing, pi
# For redirecting stdout.
from cStringIO import StringIO
import sys
import os

import yeadon.human as hum
import yeadon.densities as dens

# TODO Jason: maybe the better test is to just check against the output of
# ISEG.

class TestHuman(unittest.TestCase):
    """Tests the :py:class:`Human` class."""

    def test_init_default_cfg(self):
        """Uses misc/samplemeasurements/male1.txt."""

        measPath = os.path.join(os.path.split(__file__)[0], '..', '..',
                'misc', 'samplemeasurements', 'male1.txt')
        h = hum.Human(measPath)
        meas = h.meas

        assert h.isSymmetric == True
        assert h.meas_mass == -1
        # reading measurements.
        assert len(h.meas) == 95
        # TODO

        # averaging limbs.
        # TODO

        # configuration.
        assert len(h.CFG) == 21
        CFGnames = ('somersalt',
                    'tilt',
                    'twist',
                    'PTsagittalFlexion',
                    'PTfrontalFlexion',
                    'TCspinalTorsion',
                    'TClateralSpinalFlexion',
                    'CA1elevation',
                    'CA1abduction',
                    'CA1rotation',
                    'CB1elevation',
                    'CB1abduction',
                    'CB1rotation',
                    'A1A2flexion',
                    'B1B2flexion',
                    'PJ1flexion',
                    'PJ1abduction',
                    'PK1flexion',
                    'PK1abduction',
                    'J1J2flexion',
                    'K1K2flexion')
        for key in CFGnames:
            assert h.CFG[key] == 0.0

        # Check initialized global position and orientation.
        testing.assert_allclose(h.coord_sys_pos, np.array([[0, 0, 0]]).T)
        testing.assert_allclose(h.coord_sys_orient, np.eye(3))

        # Check that all solids exist.
        # TODO
        self.assertEquals(len(h._Ls), 9)
        self.assertEquals(h._Ls[0].label, 'Ls0: hip joint centre')
        self.assertEquals(h._Ls[0].perimeter, meas['Ls0p'])
        self.assertEquals(h._Ls[0].width, meas['Ls0w'])

        self.assertEquals(h._Ls[1].label, 'Ls1: umbilicus')
        self.assertEquals(h._Ls[1].perimeter, meas['Ls1p'])
        self.assertEquals(h._Ls[1].width, meas['Ls1w'])

        self.assertEquals(h._Ls[2].label, 'Ls2: lowest front rib')
        self.assertEquals(h._Ls[2].perimeter, meas['Ls2p'])
        self.assertEquals(h._Ls[2].width, meas['Ls2w'])

        self.assertEquals(h._Ls[3].label, 'Ls3: nipple')
        self.assertEquals(h._Ls[3].perimeter, meas['Ls3p'])
        self.assertEquals(h._Ls[3].width, meas['Ls3w'])

        self.assertEquals(h._Ls[4].label, 'Ls4: shoulder joint centre')
        self.assertEquals(h._Ls[4].radius, meas['Ls4d'] / 2)
        self.assertEquals(h._Ls[4].width, meas['Ls4w'])

        # TODO Hard-coded parameters for the acromion from yeadon.
        self.assertEquals(h._Ls[5].label, 'Ls5: acromion')
        self.assertEquals(h._Ls[5].thickness, meas['Ls5p'])
        self.assertEquals(h._Ls[5].radius, meas['Ls5w'])

        self.assertEquals(h._Ls[6].label, 'Ls5: acromion/bottom of neck')
        self.assertEquals(h._Ls[6].perimeter, meas['Ls5p'])
        self.assertEquals(h._Ls[6].thickness, 0)

        self.assertEquals(h._Ls[7].label, 'Ls6: beneath nose')
        self.assertEquals(h._Ls[7].perimeter, meas['Ls6p'])
        self.assertEquals(h._Ls[7].thickness, 0)

        self.assertEquals(h._Ls[8].label, 'Ls7: above ear')
        self.assertEquals(h._Ls[8].perimeter, meas['Ls7p'])
        self.assertEquals(h._Ls[8].thickness, 0)

        self.assertEquals(len(h.s), 8)
        self.assertEquals(h.s[0].label, 's0: hip joint centre')
        self.assertEquals(h.s[0].density, dens.Ds[0])
        self.assertEquals(h.s[1].label, 's1: umbilicus')
        self.assertEquals(h.s[1].density, dens.Ds[1])
        self.assertEquals(h.s[2].label, 's2: lowest front rib')
        self.assertEquals(h.s[2].density, dens.Ds[2])
        self.assertEquals(h.s[3].label, 's3: nipple')
        self.assertEquals(h.s[3].density, dens.Ds[3])
        self.assertEquals(h.s[4].label, 's4: shoulder joint centre')
        self.assertEquals(h.s[4].density, dens.Ds[4])
        self.assertEquals(h.s[5].label, 's5: acromion')
        self.assertEquals(h.s[5].density, dens.Ds[5])
        self.assertEquals(h.s[6].label, 's6: beneath nose')
        self.assertEquals(h.s[6].density, dens.Ds[6])
        self.assertEquals(h.s[7].label, 's7: above ear')
        self.assertEquals(h.s[7].density, dens.Ds[7])

        # Check that all segments exist.
        # TODO

        self.assertEquals(len(h.Segments), 11)
        self.assertEquals(h.Segments[0], h.P)
        self.assertEquals(h.Segments[1], h.T)
        self.assertEquals(h.Segments[2], h.C)
        self.assertEquals(h.Segments[3], h.A1)
        self.assertEquals(h.Segments[4], h.A2)
        self.assertEquals(h.Segments[5], h.B1)
        self.assertEquals(h.Segments[6], h.B2)
        self.assertEquals(h.Segments[7], h.J1)
        self.assertEquals(h.Segments[8], h.J2)
        self.assertEquals(h.Segments[9], h.K1)
        self.assertEquals(h.Segments[10], h.K2)

        # Ensure mass is unchanged from what it should be.
        testing.assert_almost_equal(h.Mass, 
                h.P.Mass + h.T.Mass + h.C.Mass + h.A1.Mass + h.A2.Mass +
                h.B1.Mass + h.B2.Mass + h.J1.Mass + h.J2.Mass +
                h.K1.Mass + h.K2.Mass)

        # Initialize measurements using the dict from the previous one.
        h2 = hum.Human(h.meas)

        # Inspect symmetry.
        # TODO

    def test_init_interesting_cfg(self):
        # TODO
        pass

    def test_init_symmetry_off(self):
        # TODO
        pass

    def test_init_input_errors(self):
        # TODO
        pass

    def test_update_solids(self):
        # TODO
        pass

    def test_update_segments(self):
        # TODO
        pass

    def test_validate_cfg(self):
        # TODO
        pass

    def test_set_CFG(self):
        # TODO
        pass

    def test_set_CFG_dict(self):
        # TODO
        pass

    def test_calc_properties(self):
        # TODO
        pass

    def test_print_properties(self):
        # TODO
        pass

    def test_translate_coord_sys(self):
        # TODO Check out properties again.
        pass

    def test_rotate_coord_sys(self):
        # TODO Check out properties again.
        pass

    def test_transform_coord_sys(self):
        # TODO this can be simple.
        pass

    def test_combine_inertia(self):
        # TODO Try a few different cases
        # TODO test input errors.
        pass

    def test_scale_by_mass(self):
        # TODO

        # TODO cannot scale twice, or make sure the scale is relative to the
        # old scale.
        pass

    def test_read_measurements(self):
        # TODO is it expected behavior for the user to update the measurements?
        pass

    def test_write_measurements(self):
        # TODO this will have to change if we change the file format.
        pass

    def test_write_meas_for_ISEG(self):
        # TODO
        pass

    def test_read_CFG(self):
        # TODO
        pass

    def test_write_CFG(self):
        # TODO
        pass






# TODO translating the entire human: check resulting inertia properties.

# TODO compare ISEG output to our output.
# TODO test CFGbounds functionality.
