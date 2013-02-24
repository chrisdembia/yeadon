# For redirecting stdout.
from cStringIO import StringIO
import copy
import sys
import os

import unittest
import nose
import numpy as np
from numpy import testing, pi

import yeadon.inertia as inertia
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

        # Regression test.
        testing.assert_almost_equal(h.mass, 58.200488588422544)
        inertiaDes = np.zeros((3, 3))
        inertiaDes[0, 0] = 9.63093850
        inertiaDes[1, 1] = 9.99497872
        inertiaDes[2, 2] = 5.45117742e-01
        testing.assert_allclose(h.inertia, inertiaDes, atol=1e-15)
        testing.assert_allclose(h.center_of_mass,
                np.array([[0], [0], [1.19967938e-02]]), atol=1e-15)

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

    def test_density_set(self):
        """Tests the Chandler and Clauser density sets."""

        # Ensure the densities themselves have not regressed.
        segment_names = ['head-neck', 'shoulders', 'thorax', 'abdomen-pelvis',
                'upper-arm', 'forearm', 'hand', 'thigh', 'lower-leg', 'foot']
        segmental_densities_des = {
            'Chandler': dict(zip(segment_names,
            [1056,  853,  853,  853, 1005, 1052, 1080, 1020, 1078, 1091])),
            'Dempster': dict(zip(segment_names,
            [1110, 1040,  920, 1010, 1070, 1130, 1160, 1050, 1090, 1100])),
            'Clauser': dict(zip(segment_names,
            [1070, 1019, 1019, 1019, 1056, 1089, 1109, 1044, 1085, 1084])),
            }

        # Input error.
        self.assertRaises(Exception,
                hum.Human, self.male1meas, density_set='badname')
        try:
            hum.Human(self.male1meas, density_set='badname')
        except Exception as e:
            self.assertEquals(e.message, "Density set 'badname' is not one "
                    "of 'Chandler', 'Clauser', or 'Dempster'.")

        h = hum.Human(self.male1meas, density_set='Chandler')

        # Ensure the densities themselves have not regressed.
        segmental_densities_des = {
            'Chandler': dict(zip(segment_names,
            [1056,  853,  853,  853, 1005, 1052, 1080, 1020, 1078, 1091])),
            'Dempster': dict(zip(segment_names,
            [1110, 1040,  920, 1010, 1070, 1130, 1160, 1050, 1090, 1100])),
            'Clauser': dict(zip(segment_names,
            [1070, 1019, 1019, 1019, 1056, 1089, 1109, 1044, 1085, 1084])),
            }
        segmental_densities = h.segmental_densities
        for key, val in segmental_densities.items():
            for seg, dens in val.items():
                self.assertEquals(dens, segmental_densities_des[key][seg])

        # Regression test.
        testing.assert_almost_equal(h.mass, 54.639701113740323)
        inertiaDes = np.zeros((3, 3))
        inertiaDes[0, 0] = 9.26910316
        inertiaDes[1, 1] = 9.61346162
        inertiaDes[2, 2] = 0.512454528
        testing.assert_allclose(h.inertia, inertiaDes, atol=1e-15)
        testing.assert_allclose(h.center_of_mass,
                np.array([[0], [0], [2.08057425e-03]]), atol=1e-15)

        # Regression for the remaining density set.
        h = hum.Human(self.male1meas, density_set='Clauser')

        testing.assert_almost_equal(h.mass, 59.061501074879487)
        inertiaDes = np.zeros((3, 3))
        inertiaDes[0, 0] = 9.6382444
        inertiaDes[1, 1] = 10.002298
        inertiaDes[2, 2] = 0.550455953
        testing.assert_allclose(h.inertia, inertiaDes, atol=1e-15)
        testing.assert_allclose(h.center_of_mass,
                np.array([[0], [0], [0.0176605046]]), atol=1e-15)

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
        """Setting an individual CFG variable works. Also, error checks."""

        h = hum.Human(self.male1meas)
        h.set_CFG('K1K2flexion', np.pi * 0.2)

        testing.assert_almost_equal(h.CFG['K1K2flexion'], np.pi * 0.2)

        self.assertRaises(Exception, h.set_CFG, 'testing', 0.1)
        try:
            h.set_CFG('testing', 0.1)
        except Exception as e:
            self.assertEqual(e.message, "'testing' is not a valid name of a "
                    "configuration variable.")

        # Reset CFG.
        h = hum.Human(self.male1meas)
        # Inertia, etc, is affected correctly.
        h2 = hum.Human(self.male1meas)
        h2.set_CFG('somersalt', np.pi / 2)
        # Relative inertia unchanged.
        testing.assert_allclose(h2.P.rel_inertia, h.P.rel_inertia)
        # Absolute inertia is changed.
        testing.assert_almost_equal(h2.inertia[0, 0], h.inertia[0, 0])
        testing.assert_almost_equal(h2.inertia[1, 1], h.inertia[2, 2])
        testing.assert_almost_equal(h2.inertia[2, 2], h.inertia[1, 1])

        h2.set_CFG('somersalt', 0)
        h2.set_CFG('CA1elevation', np.pi / 2)
        testing.assert_almost_equal(h2.A1.rel_inertia, h.A1.rel_inertia)
        testing.assert_almost_equal(h2.A2.rel_inertia, h.A2.rel_inertia)
        # y and z components are swapped.
        testing.assert_almost_equal(h2.A1.inertia[0, 0], h.A1.inertia[0, 0])
        testing.assert_almost_equal(h2.A1.inertia[1, 1], h.A1.inertia[2, 2])
        testing.assert_almost_equal(h2.A1.inertia[2, 2], h.A1.inertia[1, 1])
        testing.assert_almost_equal(h2.A2.inertia[0, 0], h.A2.inertia[0, 0])
        testing.assert_almost_equal(h2.A2.inertia[1, 1], h.A2.inertia[2, 2])
        testing.assert_almost_equal(h2.A2.inertia[2, 2], h.A2.inertia[1, 1])

        # Subtract out the arm, and see if the remaining inertia is good.
        # That is, the only part of the human's inertia tensor that changed
        # should be that which comes from the arm A.
        # Obtain inertia tensors about origin; the other option would be
        # h.center_of_mass, but this changes depending on A1A2flexion.
        a1inertia_before = np.mat(inertia.parallel_axis( h.A1.inertia, h.A1.mass,
            h.A1.center_of_mass.T.tolist()[0]))
        a1inertia_after = np.mat(inertia.parallel_axis( h2.A1.inertia, h2.A1.mass,
            h2.A1.center_of_mass.T.tolist()[0]))
        a2inertia_before = np.mat(inertia.parallel_axis( h.A2.inertia, h.A2.mass,
            h.A2.center_of_mass.T.tolist()[0]))
        a2inertia_after = np.mat(inertia.parallel_axis( h2.A2.inertia, h2.A2.mass,
            h2.A2.center_of_mass.T.tolist()[0]))
        whole_inertia_before = np.mat(inertia.parallel_axis(h.inertia, h.mass,
            h.center_of_mass.T.tolist()[0]))
        whole_inertia_after = np.mat(inertia.parallel_axis(h2.inertia, h2.mass,
            h2.center_of_mass.T.tolist()[0]))
        testing.assert_allclose(
                whole_inertia_after - a1inertia_after - a2inertia_after,
                whole_inertia_before - a1inertia_before - a2inertia_before,
                atol=1e-15)

    def test_set_CFG_dict(self):
        """Checks input errors and that the assignment occurs."""

        h = hum.Human(self.male1meas)

        h2 = hum.Human(self.male1meas)
        h2.set_CFG_dict(h.CFG)
        self.assertEqual(h2.CFG, h.CFG)

        CFG = copy.copy(h.CFG)
        CFG.pop('twist')
        self.assertRaises(Exception, h2.set_CFG_dict, CFG)
        try:
            h2.set_CFG_dict(CFG)
        except Exception as e:
            self.assertEqual(e.message,
                    "Number of CFG variables, 20, is incorrect.")

        CFG['testing'] = 0.5
        self.assertRaises(Exception, h2.set_CFG_dict, CFG)
        try:
            h2.set_CFG_dict(CFG)
        except Exception as e:
            self.assertEqual(e.message,
                    "'testing' is not a correct variable name.")

    def test_print_properties(self):
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        h = hum.Human(self.male1meas)
        h.print_properties()
        sys.stdout = old_stdout

        fname = os.path.join(os.path.split(__file__)[0],
                'human_print_des.txt')
        fid = open(fname, 'r')
        desStr = fid.read()
        fid.close()

        self.assertEquals(mystdout.getvalue(), desStr)

    def test_scale_human_by_mass(self):
        """User can scale human's mass, via meas input or API."""

        segment_names = ['head-neck', 'shoulders', 'thorax', 'abdomen-pelvis',
                'upper-arm', 'forearm', 'hand', 'thigh', 'lower-leg', 'foot']
        segmental_densities_des = {
            'Chandler': dict(zip(segment_names,
            [1056,  853,  853,  853, 1005, 1052, 1080, 1020, 1078, 1091])),
            'Dempster': dict(zip(segment_names,
            [1110, 1040,  920, 1010, 1070, 1130, 1160, 1050, 1090, 1100])),
            'Clauser': dict(zip(segment_names,
            [1070, 1019, 1019, 1019, 1056, 1089, 1109, 1044, 1085, 1084])),
            }

        # For comparison, unscaled densities.
        h = hum.Human(self.male1meas)

        # From measurement file, scaling mass though.
        measPath = os.path.join(os.path.split(__file__)[0],
                'male1_scale.txt')
        h2 = hum.Human(measPath)

        # Make sure the mass is 100.
        self.assertEqual(h2.mass, 100)

        # Make sure all density values are scaled appropriately.
        factor = h2.mass / h.mass

        # Make sure densities are scaled correctly.
        for key, val in h.segmental_densities.items():
            for seg, dens in val.items():
                self.assertEquals(dens,
                        segmental_densities_des[key][seg] * factor)

        # Check a few individual segments and solids.
        testing.assert_almost_equal(h2.K1.mass, h.K1.mass * factor)
        testing.assert_almost_equal(h2.A2.solids[0].mass, h.A2.solids[0].mass * factor)

        # Check center of mass is not modified.
        testing.assert_almost_equal(h2.center_of_mass[2], h.center_of_mass[2])
        # Check that inertia is modified.
        testing.assert_allclose(h2.inertia, h.inertia * factor, atol=1e-15)
        testing.assert_allclose(h2.B1.solids[0].inertia, h.B1.solids[0].inertia
                * factor)

        # Scale again.
        h2.scale_human_by_mass(30)
        testing.assert_almost_equal(h2.mass, 30)

        factor2 = h2.mass / 100
        # Make sure densities are scaled correctly.
        for key, val in h2.segmental_densities.items():
            for seg, dens in val.items():
                self.assertEquals(dens,
                        segmental_densities_des[key][seg] * factor * factor2)

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

    def test_translate_coord_sys(self):
        """Just translates once and makes sure only COM changes."""
        h = hum.Human(self.male1meas)
        h2 = hum.Human(self.male1meas)
        h2.translate_coord_sys([1, 2, 3])

        testing.assert_almost_equal(h2.mass, h.mass)
        testing.assert_allclose(h2.center_of_mass,
                h.center_of_mass + np.array([[1], [2], [3]]))
        testing.assert_allclose(h2.inertia, h.inertia, atol=1e-15)

    def test_rotate_coord_sys(self):
        # TODO Check out properties again.
        h = hum.Human(self.male1meas)
        pass

    def test_transform_coord_sys(self):
        # TODO this can be simple.
        pass

    def test_combine_inertia(self):
        # TODO Try a few different cases
        # TODO test input errors.
        pass

# TODO translating the entire human: check resulting inertia properties.

# TODO compare ISEG output to our output.

    # TODO really make sure we're calculating total inertia correctly.
    # TODO make sure we're doing rotations correctly.3
    # TODO make sure relative vs absolute inertia etc is correct.

    # TODO test combineinerita by manual calculations.

    # TODO try out a program flow: make sure we do all necessary updates after
    # construction, say when we change a joint angle, etc. CANNOT just change
    # measurements on the fly.
    # TODO make sure we're averaging the correct limbs
    # TODO it's possible that by averaging the measurements, we're coming up
    # with more false stadia than we would otherwise, but if we don't average
    # the measurements, how do we draw?
