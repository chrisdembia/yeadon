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

    male1meas = os.path.join(os.path.split(__file__)[0], '..', '..',
            'misc', 'samplemeasurements', 'male1.txt')

    def test_init_default_cfg(self):
        """Uses misc/samplemeasurements/male1.txt."""

        h = hum.Human(self.male1meas)
        meas = h.meas

        assert h.is_symmetric == True
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

        # TODO Hard-coded parameters for the acromion from Yeadon's ISEG.
        self.assertEquals(h._Ls[5].label, 'Ls5: acromion')
        self.assertEquals(
                h._Ls[5].thickness, h._Ls[4].width / 2 - h._Ls[5].radius)
        self.assertEquals(h._Ls[5].radius, 0.57 * h._Ls[4].radius)

        self.assertEquals(h._Ls[6].label, 'Ls5: acromion/bottom of neck')
        self.assertEquals(h._Ls[6].perimeter, meas['Ls5p'])
        self.assertEquals(h._Ls[6].thickness, 0)

        self.assertEquals(h._Ls[7].label, 'Ls6: beneath nose')
        self.assertEquals(h._Ls[7].perimeter, meas['Ls6p'])
        self.assertEquals(h._Ls[7].thickness, 0)

        self.assertEquals(h._Ls[8].label, 'Ls7: above ear')
        self.assertEquals(h._Ls[8].perimeter, meas['Ls7p'])
        self.assertEquals(h._Ls[8].thickness, 0)

        self.assertEquals(len(h._s), 8)
        self.assertEquals(h._s[0].label, 's0: hip joint centre')
        self.assertEquals(h._s[0].density, dens.Ds[0])
        self.assertEquals(h._s[1].label, 's1: umbilicus')
        self.assertEquals(h._s[1].density, dens.Ds[1])
        self.assertEquals(h._s[2].label, 's2: lowest front rib')
        self.assertEquals(h._s[2].density, dens.Ds[2])
        self.assertEquals(h._s[3].label, 's3: nipple')
        self.assertEquals(h._s[3].density, dens.Ds[3])
        self.assertEquals(h._s[4].label, 's4: shoulder joint centre')
        self.assertEquals(h._s[4].density, dens.Ds[4])
        self.assertEquals(h._s[5].label, 's5: acromion')
        self.assertEquals(h._s[5].density, dens.Ds[5])
        self.assertEquals(h._s[6].label, 's6: beneath nose')
        self.assertEquals(h._s[6].density, dens.Ds[6])
        self.assertEquals(h._s[7].label, 's7: above ear')
        self.assertEquals(h._s[7].density, dens.Ds[7])

        # Check that all segments exist.
        # TODO

        self.assertEquals(len(h.segments), 11)
        self.assertEquals(h.segments[0], h.P)
        self.assertEquals(h.segments[1], h.T)
        self.assertEquals(h.segments[2], h.C)
        self.assertEquals(h.segments[3], h.A1)
        self.assertEquals(h.segments[4], h.A2)
        self.assertEquals(h.segments[5], h.B1)
        self.assertEquals(h.segments[6], h.B2)
        self.assertEquals(h.segments[7], h.J1)
        self.assertEquals(h.segments[8], h.J2)
        self.assertEquals(h.segments[9], h.K1)
        self.assertEquals(h.segments[10], h.K2)

        # Ensure mass is unchanged from what it should be.
        testing.assert_almost_equal(h.mass, 
                h.P.mass + h.T.mass + h.C.mass + h.A1.mass + h.A2.mass +
                h.B1.mass + h.B2.mass + h.J1.mass + h.J2.mass +
                h.K1.mass + h.K2.mass)

        # Initialize measurements using the dict from the previous one.
        h2 = hum.Human(h.meas)
        # Crude test...
        testing.assert_almost_equal(h.mass, h2.mass)

        # - Inspect symmetry.
        # Symmetric by default.
        self.assertTrue(h.is_symmetric)
        self.assertEqual(h.K1.mass, h.J1.mass)
        self.assertEqual(h.K2.mass, h.J2.mass)
        self.assertEqual(h.A1.mass, h.B1.mass)
        self.assertEqual(h.A2.mass, h.B2.mass)

    def test_init_symmetry_off(self):
        """Uses misc/samplemeasurements/male1.txt."""

        h = hum.Human(self.male1meas, symmetric=False)

        self.assertFalse(h.is_symmetric)
        self.assertNotEqual(h.K1.mass, h.J1.mass)
        self.assertNotEqual(h.K2.mass, h.J2.mass)
        self.assertNotEqual(h.A1.mass, h.B1.mass)
        self.assertNotEqual(h.A2.mass, h.B2.mass)

    def test_init_interesting_cfg(self):
        """Providing a dict for CFG, input errors, and out of bounds errors."""

        # Normal behavior.
        CFG = {'somersalt': 0.0,
                'tilt': 0.0,
                'twist': np.pi/2,
                'PTsagittalFlexion': 0.0,
                'PTfrontalFlexion': 0.0,
                'TCspinalTorsion': 0.0,
                'TClateralSpinalFlexion': 0.0,
                'CA1elevation': 0.0,
                'CA1abduction': 0.0,
                'CA1rotation': 0.0,
                'CB1elevation': 0.0,
                'CB1abduction': np.pi/4,
                'CB1rotation': 0.0,
                'A1A2flexion': 0.0,
                'B1B2flexion': 0.0,
                'PJ1flexion': 0.0,
                'PJ1abduction': 0.0,
                'PK1flexion': 0.0,
                'PK1abduction': 0.0,
                'J1J2flexion': 0.0,
                'K1K2flexion': 0.0,
                }
        h = hum.Human(self.male1meas, CFG)
        self.assertEqual(h.CFG, CFG)

        # Missing a value.
        CFG = {'somersalt': 0.0,
                'tilt': 0.0,
                'twist': np.pi/2,
                'PTsagittalFlexion': 0.0,
                'PTfrontalFlexion': 0.0,
                'TCspinalTorsion': 0.0,
                'TClateralSpinalFlexion': 0.0,
                'CA1elevation': 0.0,
                'CA1abduction': 0.0,
                'CA1rotation': 0.0,
                'CB1elevation': 0.0,
                'CB1abduction': np.pi/4,
                'CB1rotation': 0.0,
                'A1A2flexion': 0.0,
                'PJ1flexion': 0.0,
                'PJ1abduction': 0.0,
                'PK1flexion': 0.0,
                'PK1abduction': 0.0,
                'J1J2flexion': 0.0,
                'K1K2flexion': 0.0,
                }
        self.assertRaises(Exception, hum.Human, self.male1meas, CFG)
        try:
            hum.Human(self.male1meas, CFG)
        except Exception as e:
            self.assertEqual(e.message,
                    "Number of CFG variables, 20, is incorrect.")

        # Invalid key.
        CFG = {'somersalt': 0.0,
                'tilt': 0.0,
                'twist': np.pi/2,
                'PTsagittalFlexion': 0.0,
                'PTfrontalFlexion': 0.0,
                'TCspinalTorsion': 0.0,
                'TClateralSpinalFlexion': 0.0,
                'CA1elevation': 0.0,
                'CA1abduction': 0.0,
                'CA1rotation': 0.0,
                'wrong': 0.01,
                'CB1elevation': 0.0,
                'CB1abduction': np.pi/4,
                'CB1rotation': 0.0,
                'A1A2flexion': 0.0,
                'PJ1flexion': 0.0,
                'PJ1abduction': 0.0,
                'PK1flexion': 0.0,
                'PK1abduction': 0.0,
                'J1J2flexion': 0.0,
                'K1K2flexion': 0.0,
                }
        self.assertRaises(Exception, hum.Human, self.male1meas, CFG)
        try:
            hum.Human(self.male1meas, CFG)
        except Exception as e:
            self.assertEqual(e.message,
                    "'wrong' is not a correct variable name.")

    def test_init_input_errors(self):
        """Especially measurement input file errors."""
        pass

    def test_update_solids(self):
        # TODO
        pass

    def test_update_segments(self):
        # TODO
        pass

    def test_validate_cfg(self):
        """Ensures that out-of-range values elicit a print, but no exception."""

        # Two values out of range.
        CFG = {'somersalt': 0.0,
                'tilt': 0.0,
                'twist': 3*np.pi,
                'PTsagittalFlexion': 0.0,
                'PTfrontalFlexion': 0.0,
                'TCspinalTorsion': 0.0,
                'TClateralSpinalFlexion': 0.0,
                'CA1elevation': 0.0,
                'CA1abduction': 0.0,
                'CA1rotation': 0.0,
                'CB1elevation': 0.0,
                'CB1abduction': np.pi/4,
                'CB1rotation': 0.0,
                'A1A2flexion': 0.0,
                'B1B2flexion': 0.0,
                'PJ1flexion': 0.0,
                'PJ1abduction': 0.0,
                'PK1flexion': -10*np.pi,
                'PK1abduction': 0.0,
                'J1J2flexion': 0.0,
                'K1K2flexion': 0.0,
                }
        desStr = ("Joint angle twist = 3.0 pi-rad is out of range. "
                "Must be between -1.0 and 1.0 pi-rad.\n"
                "Joint angle PK1flexion = -10.0 pi-rad is out of range. "
                "Must be between -0.5 and 1.0 pi-rad.\n")

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        hum.Human(self.male1meas, CFG)
        sys.stdout = old_stdout

        self.assertEquals(mystdout.getvalue(), desStr)

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

        # From measurement file.
        measPath = os.path.join(os.path.split(__file__)[0],
                'male1_scale.txt')
        h = hum.Human(measPath)
        # TODO

    def test_read_measurements(self):
        # TODO is it expected behavior for the user to update the measurements?
        # -- Measurement input file errors.
        measPath = os.path.join(os.path.split(__file__)[0],
                'male1_badkey.txt')
        self.assertRaises(ValueError, hum.Human, measPath)
        try:
            h = hum.Human(measPath)
        except ValueError as e:
            self.assertEqual(e.message, "Variable LsLL is not "
                    "valid name for a measurement.")

        measPath = os.path.join(os.path.split(__file__)[0],
                'male1_badval.txt')
        self.assertRaises(ValueError, hum.Human, measPath)
        try:
            h = hum.Human(measPath)
        except ValueError as e:
            self.assertEqual(e.message,
                    "Variable Ls1L has inappropriate value.")

        measPath = os.path.join(os.path.split(__file__)[0],
                'male1_mcf.txt')
        self.assertRaises(Exception, hum.Human, measPath)
        try:
            h = hum.Human(measPath)
        except Exception as e:
            self.assertEqual(e.message,
                    "Variable measurementconversionfactor not provided "
                    "or is 0. Set as 1 if measurements are given in meters.")

        measPath = os.path.join(os.path.split(__file__)[0],
                'male1_missingkey.txt')
        self.assertRaises(Exception, hum.Human, measPath)
        try:
            h = hum.Human(measPath)
        except Exception as e:
            self.assertEqual(e.message, "There should be 95 "
                    "measurements, but 94 were found.")

    def test_write_measurements(self):
        """Writes a valid YAML file that can be read back in."""

        path = os.path.join(os.path.split(__file__)[0],
                'meas_output.txt')
        pathDes = os.path.join(os.path.split(__file__)[0],
                'meas_output_des.txt')

        h = hum.Human(self.male1meas)
        h.write_measurements(path)

        # Output is correct.
        self.assertEqual(open(path, 'r').read(), open(pathDes, 'r').read())

        # Works as input.
        h2 = hum.Human(path)
        self.assertEqual(h2.meas, h.meas)

        os.remove(path)

    def test_write_meas_for_ISEG(self):
        """Ensures ISEG input is written correctly."""

        path = os.path.join(os.path.split(__file__)[0],
                'meas_iseg.txt')
        pathDes = os.path.join(os.path.split(__file__)[0],
                'meas_iseg_des.txt')

        h = hum.Human(self.male1meas)
        h.write_meas_for_ISEG(path)

        self.assertEqual(open(path, 'r').read(), open(pathDes, 'r').read())

        os.remove(path)

    def test_read_CFG(self):
        """Particularly checks input errors."""

        # Unrecognized variable.
        cfgPath = os.path.join(os.path.split(__file__)[0],
                'CFG_badkey.txt')
        self.assertRaises(StandardError, hum.Human, self.male1meas, cfgPath)
        try:
            hum.Human(self.male1meas, cfgPath)
        except StandardError as e:
            self.assertEqual(e.message,
                    "'invalid' is not a correct variable name.")

        # Too few inputs.
        cfgPath = os.path.join(os.path.split(__file__)[0],
                'CFG_missingkey.txt')
        self.assertRaises(StandardError, hum.Human, self.male1meas, cfgPath)
        try:
            hum.Human(self.male1meas, cfgPath)
        except StandardError as e:
            self.assertEqual(e.message, "Number of CFG variables, 20, is "
                    "incorrect.")

        # No value for a key.
        cfgPath = os.path.join(os.path.split(__file__)[0],
                'CFG_badval.txt')
        self.assertRaises(StandardError, hum.Human, self.male1meas, cfgPath)
        try:
            hum.Human(self.male1meas, cfgPath)
        except StandardError as e:
            self.assertEqual(e.message,
                    "Variable PTsagittalFlexion has no value.")

    def test_write_CFG(self):
        """Writes a valid YAML file that can be read back in."""

        CFG = {'somersalt': 0.0,
                'tilt': 0.0,
                'twist': np.pi/2,
                'PTsagittalFlexion': 0.0,
                'PTfrontalFlexion': 0.0,
                'TCspinalTorsion': 0.0,
                'TClateralSpinalFlexion': 0.0,
                'CA1elevation': 0.0,
                'CA1abduction': 0.0,
                'CA1rotation': 0.0,
                'CB1elevation': 0.0,
                'CB1abduction': np.pi/4,
                'CB1rotation': 0.0,
                'A1A2flexion': 0.0,
                'B1B2flexion': 0.0,
                'PJ1flexion': 0.0,
                'PJ1abduction': 0.0,
                'PK1flexion': 0.0,
                'PK1abduction': 0.0,
                'J1J2flexion': 0.0,
                'K1K2flexion': 0.0,
                }
        path = os.path.join(os.path.split(__file__)[0],
                'CFG_output.txt')
        h = hum.Human(self.male1meas, CFG)
        h.write_CFG(path)

        pathDes = os.path.join(os.path.split(__file__)[0],
                'CFG_output_des.txt')
        self.assertEqual(open(path, 'r').read(), open(pathDes, 'r').read())

        # Can use the cfg output as input.
        h = hum.Human(self.male1meas, path)
        self.assertEqual(h.CFG, CFG)

        os.remove(path)

# TODO translating the entire human: check resulting inertia properties.
# TODO make sure mass scaling works appropriately.

# TODO compare ISEG output to our output.
# TODO test CFGbounds functionality.
# TODO reading measurement input file: test bad input:
    # missing a measurement
    # value is zero
    # repeating a measurement/key

    # TODO really make sure we're calculating inertia correctly.
    # TODO make sure we're doing rotations correctly.3
    # TODO make sure the rotations rotate as expected.2
    # TODO file i/o 1
    # TODO zero-config inertia comparison with ISEG code. 2
    # TODO make sure relative vs absolute inertia etc is correct.

    # TODO test combineinerita by manual calculations.

    # TODO try out a program flow: make sure we do all necessary updates after
    # construction, say when we change a joint angle, etc. CANNOT just change
    # measurements on the fly.
