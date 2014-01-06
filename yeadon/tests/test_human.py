# For redirecting stdout.
from cStringIO import StringIO
import copy
import sys
import os
import warnings

import unittest
import nose
import numpy as np
from numpy import testing, pi

import yeadon.inertia as inertia
import yeadon.human as hum

warnings.filterwarnings('ignore', category=DeprecationWarning)

class TestHuman(unittest.TestCase):
    """Tests the :py:class:`Human` class."""

    male1meas = os.path.join(os.path.split(__file__)[0], '..', '..',
            'misc', 'samplemeasurements', 'male1.txt')

    def runTest(self):
        # NOTE : This allows one to run this test at the interpreter.
        pass

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

        # averaging limbs.
        testing.assert_almost_equal(meas['La2L'], meas['Lb2L'])
        testing.assert_almost_equal(meas['La3L'], meas['Lb3L'])
        testing.assert_almost_equal(meas['La4L'], meas['Lb4L'])
        testing.assert_almost_equal(meas['La5L'], meas['Lb5L'])
        testing.assert_almost_equal(meas['La6L'], meas['Lb6L'])
        testing.assert_almost_equal(meas['La7L'], meas['Lb7L'])
        testing.assert_almost_equal(meas['La0p'], meas['Lb0p'])
        testing.assert_almost_equal(meas['La1p'], meas['Lb1p'])
        testing.assert_almost_equal(meas['La2p'], meas['Lb2p'])
        testing.assert_almost_equal(meas['La3p'], meas['Lb3p'])
        testing.assert_almost_equal(meas['La4p'], meas['Lb4p'])
        testing.assert_almost_equal(meas['La5p'], meas['Lb5p'])
        testing.assert_almost_equal(meas['La6p'], meas['Lb6p'])
        testing.assert_almost_equal(meas['La7p'], meas['Lb7p'])
        testing.assert_almost_equal(meas['La4w'], meas['Lb4w'])
        testing.assert_almost_equal(meas['La5w'], meas['Lb5w'])
        testing.assert_almost_equal(meas['La6w'], meas['Lb6w'])
        testing.assert_almost_equal(meas['La7w'], meas['Lb7w'])

        testing.assert_almost_equal(meas['Lj1L'], meas['Lk1L'])
        testing.assert_almost_equal(meas['Lj3L'], meas['Lk3L'])
        testing.assert_almost_equal(meas['Lj4L'], meas['Lk4L'])
        testing.assert_almost_equal(meas['Lj5L'], meas['Lk5L'])
        testing.assert_almost_equal(meas['Lj6L'], meas['Lk6L'])
        testing.assert_almost_equal(meas['Lj8L'], meas['Lk8L'])
        testing.assert_almost_equal(meas['Lj9L'], meas['Lk9L'])
        testing.assert_almost_equal(meas['Lj1p'], meas['Lk1p'])
        testing.assert_almost_equal(meas['Lj2p'], meas['Lk2p'])
        testing.assert_almost_equal(meas['Lj3p'], meas['Lk3p'])
        testing.assert_almost_equal(meas['Lj4p'], meas['Lk4p'])
        testing.assert_almost_equal(meas['Lj5p'], meas['Lk5p'])
        testing.assert_almost_equal(meas['Lj6p'], meas['Lk6p'])
        testing.assert_almost_equal(meas['Lj7p'], meas['Lk7p'])
        testing.assert_almost_equal(meas['Lj8p'], meas['Lk8p'])
        testing.assert_almost_equal(meas['Lj9p'], meas['Lk9p'])
        testing.assert_almost_equal(meas['Lj8w'], meas['Lk8w'])
        testing.assert_almost_equal(meas['Lj9w'], meas['Lk9w'])
        testing.assert_almost_equal(meas['Lj6d'], meas['Lk6d'])

        # configuration.
        assert len(h.CFG) == 21
        CFGnames = ('somersault',
                    'tilt',
                    'twist',
                    'PTsagittalFlexion',
                    'PTbending',
                    'TCspinalTorsion',
                    'TCsagittalSpinalFlexion',
                    'CA1extension',
                    'CA1adduction',
                    'CA1rotation',
                    'CB1extension',
                    'CB1abduction',
                    'CB1rotation',
                    'A1A2extension',
                    'B1B2extension',
                    'PJ1extension',
                    'PJ1adduction',
                    'PK1extension',
                    'PK1abduction',
                    'J1J2flexion',
                    'K1K2flexion')
        for key in CFGnames:
            assert h.CFG[key] == 0.0

        # Check initialized global position and orientation.
        testing.assert_allclose(h._coord_sys_pos, np.array([[0, 0, 0]]).T)
        testing.assert_allclose(h._coord_sys_orient, np.eye(3))


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
        testing.assert_almost_equal(h.K2.mass, h.J2.mass)
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
        meas = h.meas

        self.assertFalse(h.is_symmetric)
        self.assertNotEqual(h.K1.mass, h.J1.mass)
        self.assertNotEqual(h.K2.mass, h.J2.mass)
        self.assertNotEqual(h.A1.mass, h.B1.mass)
        self.assertNotEqual(h.A2.mass, h.B2.mass)

        # Check level and solid definitions.
        # segment s
        self.assertEquals(len(h._Ls), 9)
        self.assertEquals(h._Ls[0].label, 'Ls0: hip joint centre')
        testing.assert_almost_equal(h._Ls[0].perimeter, meas['Ls0p'])
        testing.assert_almost_equal(h._Ls[0].width, meas['Ls0w'])

        self.assertEquals(h._Ls[1].label, 'Ls1: umbilicus')
        testing.assert_almost_equal(h._Ls[1].perimeter, meas['Ls1p'])
        testing.assert_almost_equal(h._Ls[1].width, meas['Ls1w'])

        self.assertEquals(h._Ls[2].label, 'Ls2: lowest front rib')
        testing.assert_almost_equal(h._Ls[2].perimeter, meas['Ls2p'])
        testing.assert_almost_equal(h._Ls[2].width, meas['Ls2w'])

        self.assertEquals(h._Ls[3].label, 'Ls3: nipple')
        testing.assert_almost_equal(h._Ls[3].perimeter, meas['Ls3p'])
        testing.assert_almost_equal(h._Ls[3].width, meas['Ls3w'])

        self.assertEquals(h._Ls[4].label, 'Ls4: shoulder joint centre')
        testing.assert_almost_equal(h._Ls[4].radius, meas['Ls4d'] / 2)
        testing.assert_almost_equal(h._Ls[4].width, meas['Ls4w'])

        # TODO Hard-coded parameters for the acromion from Yeadon's ISEG.
        self.assertEquals(h._Ls[5].label, 'Ls5: acromion')
        testing.assert_almost_equal(
                h._Ls[5].thickness, h._Ls[4].width / 2 - h._Ls[5].radius)
        testing.assert_almost_equal(h._Ls[5].radius, 0.57 * h._Ls[4].radius)

        self.assertEquals(h._Ls[6].label, 'Ls5: acromion/bottom of neck')
        testing.assert_almost_equal(h._Ls[6].perimeter, meas['Ls5p'])
        self.assertEquals(h._Ls[6].thickness, 0)

        self.assertEquals(h._Ls[7].label, 'Ls6: beneath nose')
        testing.assert_almost_equal(h._Ls[7].perimeter, meas['Ls6p'])
        self.assertEquals(h._Ls[7].thickness, 0)

        self.assertEquals(h._Ls[8].label, 'Ls7: above ear')
        testing.assert_almost_equal(h._Ls[8].perimeter, meas['Ls7p'])
        self.assertEquals(h._Ls[8].thickness, 0)

        self.assertEquals(len(h._s), 8)
        self.assertEquals(h._s[0].label, 's0: hip joint centre')
        testing.assert_almost_equal(h._s[0].density,
                h.segmental_densities['Dempster']['abdomen-pelvis'])
        self.assertEquals(h._s[1].label, 's1: umbilicus')
        testing.assert_almost_equal(h._s[1].density,
                h.segmental_densities['Dempster']['abdomen-pelvis'])
        self.assertEquals(h._s[2].label, 's2: lowest front rib')
        testing.assert_almost_equal(h._s[2].density,
                h.segmental_densities['Dempster']['thorax'])
        self.assertEquals(h._s[3].label, 's3: nipple')
        testing.assert_almost_equal(h._s[3].density,
                h.segmental_densities['Dempster']['thorax'])
        self.assertEquals(h._s[4].label, 's4: shoulder joint centre')
        testing.assert_almost_equal(h._s[4].density,
                h.segmental_densities['Dempster']['shoulders'])
        self.assertEquals(h._s[5].label, 's5: acromion')
        testing.assert_almost_equal(h._s[5].density,
                h.segmental_densities['Dempster']['head-neck'])
        self.assertEquals(h._s[6].label, 's6: beneath nose')
        testing.assert_almost_equal(h._s[6].density,
                h.segmental_densities['Dempster']['head-neck'])
        self.assertEquals(h._s[7].label, 's7: above ear')
        testing.assert_almost_equal(h._s[7].density,
                h.segmental_densities['Dempster']['head-neck'])

        # arms
        # 'a'
        self.assertEquals(len(h._La), 8)
        self.assertEquals(h._La[0].label, 'La0: shoulder joint centre')
        testing.assert_almost_equal(h._La[0].perimeter, meas['La0p'])
        self.assertEquals(h._La[0].thickness, 0)

        self.assertEquals(h._La[1].label, 'La1: mid-arm')
        testing.assert_almost_equal(h._La[1].perimeter, meas['La1p'])
        self.assertEquals(h._La[1].thickness, 0)

        self.assertEquals(h._La[2].label, 'La2: elbow joint centre')
        testing.assert_almost_equal(h._La[2].perimeter, meas['La2p'])
        self.assertEquals(h._La[2].thickness, 0)

        self.assertEquals(h._La[3].label, 'La3: maximum forearm perimeter')
        testing.assert_almost_equal(h._La[3].perimeter, meas['La3p'])
        self.assertEquals(h._La[3].thickness, 0)

        self.assertEquals(h._La[4].label, 'La4: wrist joint centre')
        testing.assert_almost_equal(h._La[4].perimeter, meas['La4p'])
        testing.assert_almost_equal(h._La[4].width, meas['La4w'])

        self.assertEquals(h._La[5].label, 'La5: base of thumb')
        testing.assert_almost_equal(h._La[5].perimeter, meas['La5p'])
        testing.assert_almost_equal(h._La[5].width, meas['La5w'])

        self.assertEquals(h._La[6].label, 'La6: knuckles')
        testing.assert_almost_equal(h._La[6].perimeter, meas['La6p'])
        testing.assert_almost_equal(h._La[6].width, meas['La6w'])

        self.assertEquals(h._La[7].label, 'La7: fingernails')
        testing.assert_almost_equal(h._La[7].perimeter, meas['La7p'])
        testing.assert_almost_equal(h._La[7].width, meas['La7w'])

        self.assertEquals(len(h._a_solids), 7)
        self.assertEquals(h._a_solids[0].label, 'a0: shoulder joint centre')
        testing.assert_almost_equal(h._a_solids[0].density,
                h.segmental_densities['Dempster']['upper-arm'])

        self.assertEquals(h._a_solids[1].label, 'a1: mid-arm')
        testing.assert_almost_equal(h._a_solids[1].density,
                h.segmental_densities['Dempster']['upper-arm'])

        self.assertEquals(h._a_solids[2].label, 'a2: elbow joint centre')
        testing.assert_almost_equal(h._a_solids[2].density,
                h.segmental_densities['Dempster']['forearm'])

        self.assertEquals(h._a_solids[3].label, 'a3: maximum forearm perimeter')
        testing.assert_almost_equal(h._a_solids[3].density,
                h.segmental_densities['Dempster']['forearm'])

        self.assertEquals(h._a_solids[4].label, 'a4: wrist joint centre')
        testing.assert_almost_equal(h._a_solids[4].density,
                h.segmental_densities['Dempster']['hand'])

        self.assertEquals(h._a_solids[5].label, 'a5: base of thumb')
        testing.assert_almost_equal(h._a_solids[5].density,
                h.segmental_densities['Dempster']['hand'])

        self.assertEquals(h._a_solids[6].label, 'a6: knuckles')
        testing.assert_almost_equal(h._a_solids[6].density,
                h.segmental_densities['Dempster']['hand'])

        # 'b'
        self.assertEquals(len(h._Lb), 8)
        self.assertEquals(h._Lb[0].label, 'Lb0: shoulder joint centre')
        testing.assert_almost_equal(h._Lb[0].perimeter, meas['Lb0p'])
        self.assertEquals(h._Lb[0].thickness, 0)

        self.assertEquals(h._Lb[1].label, 'Lb1: mid-arm')
        testing.assert_almost_equal(h._Lb[1].perimeter, meas['Lb1p'])
        self.assertEquals(h._Lb[1].thickness, 0)

        self.assertEquals(h._Lb[2].label, 'Lb2: elbow joint centre')
        testing.assert_almost_equal(h._Lb[2].perimeter, meas['Lb2p'])
        self.assertEquals(h._Lb[2].thickness, 0)

        self.assertEquals(h._Lb[3].label, 'Lb3: maximum forearm perimeter')
        testing.assert_almost_equal(h._Lb[3].perimeter, meas['Lb3p'])
        self.assertEquals(h._Lb[3].thickness, 0)

        self.assertEquals(h._Lb[4].label, 'Lb4: wrist joint centre')
        testing.assert_almost_equal(h._Lb[4].perimeter, meas['Lb4p'])
        testing.assert_almost_equal(h._Lb[4].width, meas['Lb4w'])

        self.assertEquals(h._Lb[5].label, 'Lb5: base of thumb')
        testing.assert_almost_equal(h._Lb[5].perimeter, meas['Lb5p'])
        testing.assert_almost_equal(h._Lb[5].width, meas['Lb5w'])

        self.assertEquals(h._Lb[6].label, 'Lb6: knuckles')
        testing.assert_almost_equal(h._Lb[6].perimeter, meas['Lb6p'])
        testing.assert_almost_equal(h._Lb[6].width, meas['Lb6w'])

        self.assertEquals(h._Lb[7].label, 'Lb7: fingernails')
        testing.assert_almost_equal(h._Lb[7].perimeter, meas['Lb7p'])
        testing.assert_almost_equal(h._Lb[7].width, meas['Lb7w'])

        self.assertEquals(len(h._b_solids), 7)
        self.assertEquals(h._b_solids[0].label, 'b0: shoulder joint centre')
        testing.assert_almost_equal(h._b_solids[0].density,
                h.segmental_densities['Dempster']['upper-arm'])

        self.assertEquals(h._b_solids[1].label, 'b1: mid-arm')
        testing.assert_almost_equal(h._b_solids[1].density,
                h.segmental_densities['Dempster']['upper-arm'])

        self.assertEquals(h._b_solids[2].label, 'b2: elbow joint centre')
        testing.assert_almost_equal(h._b_solids[2].density,
                h.segmental_densities['Dempster']['forearm'])

        self.assertEquals(h._b_solids[3].label, 'b3: maximum forearm perimeter')
        testing.assert_almost_equal(h._b_solids[3].density,
                h.segmental_densities['Dempster']['forearm'])

        self.assertEquals(h._b_solids[4].label, 'b4: wrist joint centre')
        testing.assert_almost_equal(h._b_solids[4].density,
                h.segmental_densities['Dempster']['hand'])

        self.assertEquals(h._b_solids[5].label, 'b5: base of thumb')
        testing.assert_almost_equal(h._b_solids[5].density,
                h.segmental_densities['Dempster']['hand'])

        self.assertEquals(h._b_solids[6].label, 'b6: knuckles')
        testing.assert_almost_equal(h._b_solids[6].density,
                h.segmental_densities['Dempster']['hand'])

        # legs
        # 'j'
        self.assertEquals(len(h._Lj), 10)
        Lj0p = np.pi * np.sqrt(h._Ls[0].radius * h._Ls[0].width)
        self.assertEquals(h._Lj[0].label, 'Lj0: hip joint centre')
        testing.assert_almost_equal(h._Lj[0].perimeter, Lj0p)
        self.assertEquals(h._Lj[0].thickness, 0)

        self.assertEquals(h._Lj[1].label, 'Lj1: crotch')
        testing.assert_almost_equal(h._Lj[1].perimeter, meas['Lj1p'])
        self.assertEquals(h._Lj[1].thickness, 0)

        self.assertEquals(h._Lj[2].label, 'Lj2: mid-thigh')
        testing.assert_almost_equal(h._Lj[2].perimeter, meas['Lj2p'])
        self.assertEquals(h._Lj[2].thickness, 0)

        self.assertEquals(h._Lj[3].label, 'Lj3: knee joint centre')
        testing.assert_almost_equal(h._Lj[3].perimeter, meas['Lj3p'])
        self.assertEquals(h._Lj[3].thickness, 0)

        self.assertEquals(h._Lj[4].label, 'Lj4: maximum calf perimeter')
        testing.assert_almost_equal(h._Lj[4].perimeter, meas['Lj4p'])
        self.assertEquals(h._Lj[4].thickness, 0)

        self.assertEquals(h._Lj[5].label, 'Lj5: ankle joint centre')
        testing.assert_almost_equal(h._Lj[5].perimeter, meas['Lj5p'])
        self.assertEquals(h._Lj[5].thickness, 0)

        self.assertEquals(h._Lj[6].label, 'Lj6: heel')
        testing.assert_almost_equal(h._Lj[6].perimeter, meas['Lj6p'])
        testing.assert_almost_equal(h._Lj[6].width, meas['Lj6d'])

        self.assertEquals(h._Lj[7].label, 'Lj7: arch')
        testing.assert_almost_equal(h._Lj[7].perimeter, meas['Lj7p'])

        self.assertEquals(h._Lj[8].label, 'Lj8: ball')
        testing.assert_almost_equal(h._Lj[8].perimeter, meas['Lj8p'])
        testing.assert_almost_equal(h._Lj[8].width, meas['Lj8w'])

        self.assertEquals(h._Lj[9].label, 'Lj9: toe nails')
        testing.assert_almost_equal(h._Lj[9].perimeter, meas['Lj9p'])
        testing.assert_almost_equal(h._Lj[9].width, meas['Lj9w'])

        self.assertEquals(len(h._j_solids), 9)
        self.assertEquals(h._j_solids[0].label, 'j0: hip joint centre')
        testing.assert_almost_equal(h._j_solids[0].density,
                h.segmental_densities['Dempster']['thigh'])

        self.assertEquals(h._j_solids[1].label, 'j1: crotch')
        testing.assert_almost_equal(h._j_solids[1].density,
                h.segmental_densities['Dempster']['thigh'])

        self.assertEquals(h._j_solids[2].label, 'j2: mid-thigh')
        testing.assert_almost_equal(h._j_solids[2].density,
                h.segmental_densities['Dempster']['thigh'])

        self.assertEquals(h._j_solids[3].label, 'j3: knee joint centre')
        testing.assert_almost_equal(h._j_solids[3].density,
                h.segmental_densities['Dempster']['lower-leg'])

        self.assertEquals(h._j_solids[4].label, 'j4: maximum calf perimeter')
        testing.assert_almost_equal(h._j_solids[4].density,
                h.segmental_densities['Dempster']['lower-leg'])

        self.assertEquals(h._j_solids[5].label, 'j5: ankle joint centre')
        testing.assert_almost_equal(h._j_solids[5].density,
                h.segmental_densities['Dempster']['foot'])

        self.assertEquals(h._j_solids[6].label, 'j6: heel')
        testing.assert_almost_equal(h._j_solids[6].density,
                h.segmental_densities['Dempster']['foot'])

        self.assertEquals(h._j_solids[7].label, 'j7: arch')
        testing.assert_almost_equal(h._j_solids[7].density,
                h.segmental_densities['Dempster']['foot'])

        self.assertEquals(h._j_solids[8].label, 'j8: ball')
        testing.assert_almost_equal(h._j_solids[8].density,
                h.segmental_densities['Dempster']['foot'])

        # 'k'
        self.assertEquals(len(h._Lk), 10)
        Lk0p = np.pi * np.sqrt(h._Ls[0].radius * h._Ls[0].width)
        self.assertEquals(h._Lk[0].label, 'Lk0: hip joint centre')
        testing.assert_almost_equal(h._Lk[0].perimeter, Lk0p)
        self.assertEquals(h._Lk[0].thickness, 0)

        self.assertEquals(h._Lk[1].label, 'Lk1: crotch')
        testing.assert_almost_equal(h._Lk[1].perimeter, meas['Lk1p'])
        self.assertEquals(h._Lk[1].thickness, 0)

        self.assertEquals(h._Lk[2].label, 'Lk2: mid-thigh')
        testing.assert_almost_equal(h._Lk[2].perimeter, meas['Lk2p'])
        self.assertEquals(h._Lk[2].thickness, 0)

        self.assertEquals(h._Lk[3].label, 'Lk3: knee joint centre')
        testing.assert_almost_equal(h._Lk[3].perimeter, meas['Lk3p'])
        self.assertEquals(h._Lk[3].thickness, 0)

        self.assertEquals(h._Lk[4].label, 'Lk4: maximum calf perimeter')
        testing.assert_almost_equal(h._Lk[4].perimeter, meas['Lk4p'])
        self.assertEquals(h._Lk[4].thickness, 0)

        self.assertEquals(h._Lk[5].label, 'Lk5: ankle joint centre')
        testing.assert_almost_equal(h._Lk[5].perimeter, meas['Lk5p'])
        self.assertEquals(h._Lk[5].thickness, 0)

        self.assertEquals(h._Lk[6].label, 'Lk6: heel')
        testing.assert_almost_equal(h._Lk[6].perimeter, meas['Lk6p'])
        testing.assert_almost_equal(h._Lk[6].width, meas['Lk6d'])

        self.assertEquals(h._Lk[7].label, 'Lk7: arch')
        testing.assert_almost_equal(h._Lk[7].perimeter, meas['Lk7p'])

        self.assertEquals(h._Lk[8].label, 'Lk8: ball')
        testing.assert_almost_equal(h._Lk[8].perimeter, meas['Lk8p'])
        testing.assert_almost_equal(h._Lk[8].width, meas['Lk8w'])

        self.assertEquals(h._Lk[9].label, 'Lk9: toe nails')
        testing.assert_almost_equal(h._Lk[9].perimeter, meas['Lk9p'])
        testing.assert_almost_equal(h._Lk[9].width, meas['Lk9w'])

        self.assertEquals(len(h._k_solids), 9)
        self.assertEquals(h._k_solids[0].label, 'k0: hip joint centre')
        testing.assert_almost_equal(h._k_solids[0].density,
                h.segmental_densities['Dempster']['thigh'])

        self.assertEquals(h._k_solids[1].label, 'k1: crotch')
        testing.assert_almost_equal(h._k_solids[1].density,
                h.segmental_densities['Dempster']['thigh'])

        self.assertEquals(h._k_solids[2].label, 'k2: mid-thigh')
        testing.assert_almost_equal(h._k_solids[2].density,
                h.segmental_densities['Dempster']['thigh'])

        self.assertEquals(h._k_solids[3].label, 'k3: knee joint centre')
        testing.assert_almost_equal(h._k_solids[3].density,
                h.segmental_densities['Dempster']['lower-leg'])

        self.assertEquals(h._k_solids[4].label, 'k4: maximum calf perimeter')
        testing.assert_almost_equal(h._k_solids[4].density,
                h.segmental_densities['Dempster']['lower-leg'])

        self.assertEquals(h._k_solids[5].label, 'k5: ankle joint centre')
        testing.assert_almost_equal(h._k_solids[5].density,
                h.segmental_densities['Dempster']['foot'])

        self.assertEquals(h._k_solids[6].label, 'k6: heel')
        testing.assert_almost_equal(h._k_solids[6].density,
                h.segmental_densities['Dempster']['foot'])

        self.assertEquals(h._k_solids[7].label, 'k7: arch')
        testing.assert_almost_equal(h._k_solids[7].density,
                h.segmental_densities['Dempster']['foot'])

        self.assertEquals(h._k_solids[8].label, 'k8: ball')
        testing.assert_almost_equal(h._k_solids[8].density,
                h.segmental_densities['Dempster']['foot'])

    def test_init_interesting_cfg(self):
        """Providing a dict for CFG, input errors, and out of bounds errors."""

        # Normal behavior.
        CFG = {'somersault': 0.0,
                'tilt': 0.0,
                'twist': np.pi/2,
                'PTsagittalFlexion': 0.0,
                'PTbending': 0.0,
                'TCspinalTorsion': 0.0,
                'TCsagittalSpinalFlexion': 0.0,
                'CA1extension': 0.0,
                'CA1adduction': 0.0,
                'CA1rotation': 0.0,
                'CB1extension': 0.0,
                'CB1abduction': np.pi/4,
                'CB1rotation': 0.0,
                'A1A2extension': 0.0,
                'B1B2extension': 0.0,
                'PJ1extension': 0.0,
                'PJ1adduction': 0.0,
                'PK1extension': 0.0,
                'PK1abduction': 0.0,
                'J1J2flexion': 0.0,
                'K1K2flexion': 0.0,
                }
        h = hum.Human(self.male1meas, CFG)
        self.assertEqual(h.CFG, CFG)

        # Missing a value.
        CFG = {'somersault': 0.0,
                'tilt': 0.0,
                'twist': np.pi/2,
                'PTsagittalFlexion': 0.0,
                'PTbending': 0.0,
                'TCspinalTorsion': 0.0,
                'TCsagittalSpinalFlexion': 0.0,
                'CA1extension': 0.0,
                'CA1adduction': 0.0,
                'CA1rotation': 0.0,
                'CB1extension': 0.0,
                'CB1abduction': np.pi/4,
                'CB1rotation': 0.0,
                'A1A2extension': 0.0,
                'PJ1extension': 0.0,
                'PJ1adduction': 0.0,
                'PK1extension': 0.0,
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
        CFG = {'somersault': 0.0,
                'tilt': 0.0,
                'twist': np.pi/2,
                'PTsagittalFlexion': 0.0,
                'PTbending': 0.0,
                'TCspinalTorsion': 0.0,
                'TCsagittalSpinalFlexion': 0.0,
                'CA1extension': 0.0,
                'CA1adduction': 0.0,
                'CA1rotation': 0.0,
                'wrong': 0.01,
                'CB1extension': 0.0,
                'CB1abduction': np.pi/4,
                'CB1rotation': 0.0,
                'A1A2extension': 0.0,
                'PJ1extension': 0.0,
                'PJ1adduction': 0.0,
                'PK1extension': 0.0,
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
        CFG = {'somersault': 0.0,
               'tilt': 0.0,
               'twist': 3.0 * np.pi,
               'PTsagittalFlexion': 0.0,
               'PTbending': 0.0,
               'TCspinalTorsion': 0.0,
               'TCsagittalSpinalFlexion': 0.0,
               'CA1extension': 0.0,
               'CA1adduction': 0.0,
               'CA1rotation': 0.0,
               'CB1extension': 0.0,
               'CB1abduction': np.pi / 4.0,
               'CB1rotation': 0.0,
               'A1A2extension': 0.0,
               'B1B2extension': 0.0,
               'PJ1extension': 0.0,
               'PJ1adduction': 0.0,
               'PK1extension': -10.0 * np.pi,
               'PK1abduction': 0.0,
               'J1J2flexion': 0.0,
               'K1K2flexion': 0.0,
               }
        desStr = ("Joint angle twist = 3.0 pi-rad is out of range. "
                "Must be between -1.0 and 1.0 pi-rad.\n"
                "Joint angle PK1extension = -10.0 pi-rad is out of range. "
                "Must be between -1.0 and 0.5 pi-rad.\n")

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
        h2.set_CFG('somersault', np.pi / 2)
        # Relative inertia unchanged.
        testing.assert_allclose(h2.P.rel_inertia, h.P.rel_inertia)
        # Absolute inertia is changed.
        testing.assert_almost_equal(h2.inertia[0, 0], h.inertia[0, 0])
        testing.assert_almost_equal(h2.inertia[1, 1], h.inertia[2, 2])
        testing.assert_almost_equal(h2.inertia[2, 2], h.inertia[1, 1])

        h2.set_CFG('somersault', 0)
        h2.set_CFG('CA1extension', np.pi / 2)
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
        # h.center_of_mass, but this changes depending on A1A2extension.
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

    def test_deprecated_CFG_names(self):
        """For v1.1.0, we changed a number of the configuration variable names.
        We still want to accept incorrect spellings for backwards
        compatibility. It should issue a deprecation warning
        # if you use the incorrect spelling but the code should run anyways.

        """
        deprecated_CFG_names = {'somersalt': 'somersault',
                'CA1elevation': 'CA1extension',
                'CB1elevation': 'CB1extension',
                'CA1abduction': 'CA1adduction',
                'A1A2flexion': 'A1A2extension',
                'B1B2flexion': 'B1B2extension',
                'TClateralSpinalFlexion': 'TCsagittalSpinalFlexion',
                'PJ1flexion': 'PJ1extension',
                'PK1flexion': 'PK1extension',
                'PJ1abduction': 'PJ1adduction',
                'PTfrontalFlexion': 'PTbending',
                }

        for old_name, new_name in deprecated_CFG_names.items():

            # set_CFG.
            h = hum.Human(self.male1meas)
            CFG_value = h.CFGbounds[h.CFGnames.index(new_name)][0]
            h.set_CFG(old_name, CFG_value)
            assert old_name not in h.CFG.keys()
            testing.assert_allclose(h.CFG[new_name], CFG_value)

            # set_CFG_dict.
            h = hum.Human(self.male1meas)
            CFG = copy.copy(h.CFG)
            CFG.pop(new_name)
            CFG[old_name] = CFG_value
            h.set_CFG_dict(CFG)
            assert old_name not in h.CFG.keys()
            assert new_name in h.CFG.keys()
            testing.assert_allclose(h.CFG[new_name], CFG_value)

        # Reading from file.
        cfg_path = os.path.join(os.path.split(__file__)[0],
                               'CFG_deprecated_names.txt')
        h = hum.Human(self.male1meas, cfg_path)
        for old_name, new_name in deprecated_CFG_names.items():
            assert old_name not in h.CFG.keys()
            assert new_name in h.CFG.keys()

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

    def test_crazy_CFG_regression(self):
        """Puts the human in a crazy configuration (all angles are non-zero)
        and compares all 3 inertial properties.

        This is a regression test, not a physical verification.

        """
        CFG = {'somersault': 0.20 * np.pi,
               'tilt': 0.10 * np.pi,
               'twist': 0.30 * np.pi,
               'PTsagittalFlexion': 0.35 * np.pi,
               'PTbending': -0.18 * np.pi,
               'TCspinalTorsion': -0.08 * np.pi,
               'TCsagittalSpinalFlexion': 0.13 * np.pi,
               'CA1extension': -0.42 * np.pi,
               'CA1adduction': 0.19 * np.pi,
               'CA1rotation': 0.38 * np.pi,
               'CB1extension': -0.13 * np.pi,
               'CB1abduction': 0.32 * np.pi,
               'CB1rotation': 0.48 * np.pi,
               'A1A2extension': -0.45 * np.pi,
               'B1B2extension': -0.31 * np.pi,
               'PJ1extension': 0.26 * np.pi,
               'PJ1adduction': 0.37 * np.pi,
               'PK1extension': -0.21 * np.pi,
               'PK1abduction': 0.29 * np.pi,
               'J1J2flexion': 0.23 * np.pi,
               'K1K2flexion': 0.41 * np.pi,
               }
        h = hum.Human(self.male1meas, CFG)

        testing.assert_almost_equal(h.mass, 58.2004885884)

        expected_center_of_mass = np.matrix([[-0.04602766],
                                             [-0.17716871],
                                             [-0.05332974]])
        testing.assert_allclose(h.center_of_mass, expected_center_of_mass)

        expected_inertia = \
           np.matrix([[ 2.89276755,  0.43049026, -0.80508996],
                      [ 0.43049026,  4.37335248,  0.17229662],
                      [-0.80508996,  0.17229662,  4.13153827]])
        testing.assert_allclose(h.inertia, expected_inertia, atol=1e-6)

    def test_segment_pos(self):
        """Ensures that Segment.pos and Segment.end_pos return the correct
        quantities, for arms and legs. Regression test."""
        h = hum.Human(self.male1meas)
        testing.assert_almost_equal(h.A1.pos[2, 0], 0.472)
        testing.assert_almost_equal(h.A1.end_pos[2, 0], 0.2085)
        testing.assert_almost_equal(h.B1.pos[2, 0], 0.472)
        testing.assert_almost_equal(h.B1.end_pos[2, 0], 0.2085)

        testing.assert_almost_equal(h.J2.pos[2, 0], -0.424)
        testing.assert_almost_equal(h.J2.end_pos[2, 0], -1.02)

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

        # Use the __str__method.
        # It's just a fluke that we need to append an additional newline char.
        self.assertEquals(h.__str__() + '\n', desStr)

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

        CFG = {'somersault': 0.0,
                'tilt': 0.0,
                'twist': np.pi/2,
                'PTsagittalFlexion': 0.0,
                'PTbending': 0.0,
                'TCspinalTorsion': 0.0,
                'TCsagittalSpinalFlexion': 0.0,
                'CA1extension': 0.0,
                'CA1adduction': 0.0,
                'CA1rotation': 0.0,
                'CB1extension': 0.0,
                'CB1abduction': np.pi/4,
                'CB1rotation': 0.0,
                'A1A2extension': 0.0,
                'B1B2extension': 0.0,
                'PJ1extension': 0.0,
                'PJ1adduction': 0.0,
                'PK1extension': 0.0,
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
        # TODO this method has been hidden for v1.0 release.
        h = hum.Human(self.male1meas)
        h2 = hum.Human(self.male1meas)
        h2._translate_coord_sys([1, 2, 3])

        testing.assert_almost_equal(h2.mass, h.mass)
        testing.assert_allclose(h2.center_of_mass,
                h.center_of_mass + np.array([[1], [2], [3]]))
        testing.assert_allclose(h2.inertia, h.inertia, atol=1e-15)

    def test_rotate_coord_sys(self):
        # TODO Check out properties again.
        h = hum.Human(self.male1meas)
        # TODO this method has been hidden for v1.0 release.
        pass

    def test_transform_coord_sys(self):
        # TODO this can be simple.
        # TODO this method has been hidden for v1.0 release.
        pass

    def test_combine_inertia(self):
        """Tries input errors and checks output against some hand
        calculations."""
        # Input errors.
        h = hum.Human(self.male1meas, symmetric=True)

        # Nonsensical input.
        with self.assertRaises(Exception) as e:
            h.combine_inertia([''])
        self.assertEquals(e.exception.message, "The string '' does not "
                "identify a segment or solid of the human.")

        with self.assertRaises(Exception) as e:
            h.combine_inertia()

        with self.assertRaises(Exception) as e:
            h.combine_inertia([])
        self.assertEquals(e.exception.message, "Empty input.")

        # List a string that doesn't identify a segment or solid.
        with self.assertRaises(Exception) as e:
            h.combine_inertia(['abracadabra'])
        self.assertEquals(e.exception.message, "The string 'abracadabra' does "
                "not identify a segment or solid of the human.")

        # List a solid more than once.
        with self.assertRaises(Exception) as e:
            h.combine_inertia(['j4', 'a0', 's0', 'a0', 'A2'])
        self.assertEquals(e.exception.message, "An object is listed more than "
                "once. A solid/segment can only be listed once.")

        # List solid and its parent segment.
        with self.assertRaises(Exception) as e:
            h.combine_inertia(['k2', 'K1'])
        self.assertEquals(e.exception.message, "A solid k2 and its parent "
                "segment K1 have both been given as inputs. This duplicates "
                "that solid's contribution.")

        with self.assertRaises(Exception) as e:
            h.combine_inertia(['B2', 'b6'])

        # The following depends on the fact that we've imposed symmetry.
        # 'c' for combined.
        c_mass, c_com, c_inertia = h.combine_inertia(['a0', 'b0'])
        # Using _a_solids instead of A1.solids because we've reversed the order
        # of the solids in the segments.
        c_mass_des = h._a_solids[0].mass + h._b_solids[0].mass
        self.assertEquals(c_mass, c_mass_des)
        testing.assert_allclose(c_com,
                (h._a_solids[0].mass * h._a_solids[0].center_of_mass +
                    h._b_solids[0].mass * h._b_solids[0].center_of_mass) /
                c_mass_des)
        # Given symmetry, com's x-component should be zero.
        self.assertEquals(c_com[0, 0], 0.0)
        # ... z-component is the same as for individual solids.
        self.assertEquals(c_com[2, 0], h._a_solids[0].center_of_mass[2, 0])
        # The 2 comes from symmetry; then we have parallel axis theorem.
        self.assertEquals(c_inertia[0, 0], 2 * h._a_solids[0].inertia[0, 0])
        parallel_term = \
                h._a_solids[0].mass * h._a_solids[0].center_of_mass[0, 0]**2
        Iyy_des = 2.0 * (h._a_solids[0].inertia[1, 1] + parallel_term)
        self.assertEquals(c_inertia[1, 1], Iyy_des)
        Izz_des = 2.0 * (h._a_solids[0].inertia[2, 2] + parallel_term)
        self.assertEquals(c_inertia[2, 2], Izz_des)
        self.assertEquals(c_inertia[0, 1], 0.0)
        self.assertEquals(c_inertia[0, 2], 0.0)
        self.assertEquals(c_inertia[1, 2], 0.0)

        c_mass = None
        c_com = None
        c_inertia = None

        # Try segments.
        c_mass, c_com, c_inertia = h.combine_inertia(['A2', 'B2'])
        c_mass_des = h.A2.mass + h.B2.mass
        self.assertEquals(c_mass, c_mass_des)
        self.assertEquals(c_com[0, 0], 0.0)
        testing.assert_almost_equal(c_com[2, 0], h.B2.center_of_mass[2, 0])
        self.assertEquals(c_inertia[0, 0], 2 * h.A2.inertia[0, 0])
        parallel_term = h.A2.mass * h.A2.center_of_mass[0, 0]**2
        Iyy_des = 2.0 * (h.A2.inertia[1, 1] + parallel_term)
        self.assertEquals(c_inertia[1, 1], Iyy_des)
        Izz_des = 2.0 * (h.A2.inertia[2, 2] + parallel_term)
        self.assertEquals(c_inertia[2, 2], Izz_des)

        self.assertEquals(c_inertia[0, 1], 0.0)
        testing.assert_almost_equal(c_inertia[0, 2], 0.0)
        self.assertEquals(c_inertia[1, 2], 0.0)

    def test_inertia_transformed(self):
        """Tests the functionality of getting an inertia tensor about a
        different point and in a different frame.

        """
        h = hum.Human(self.male1meas)
        h.set_CFG('somersault', np.pi * 0.25)
        inertia_pre = h.inertia
        m = h.mass

        # A simple change in position.
        d = 15  # meters
        inertia_post = h.inertia_transformed(
                pos=[d + h.center_of_mass[0, 0],
                    h.center_of_mass[1, 0],
                    h.center_of_mass[2, 0]])
        offset = m * d**2
        # Moments of inertia.
        testing.assert_almost_equal(inertia_post[0, 0], inertia_pre[0, 0])
        testing.assert_almost_equal(
                inertia_post[1, 1], inertia_pre[1, 1] + offset)
        testing.assert_almost_equal(
                inertia_post[2, 2], inertia_pre[2, 2] + offset)
        # Products of inertia.
        testing.assert_almost_equal(inertia_post[0, 1], inertia_pre[0, 1])
        testing.assert_almost_equal(inertia_post[0, 2], inertia_pre[0, 2])
        testing.assert_almost_equal(inertia_post[1, 2], inertia_pre[1, 2])
        # Symmetry is preserved.
        testing.assert_almost_equal(inertia_post[1, 0], inertia_post[0, 1])
        testing.assert_almost_equal(inertia_post[2, 0], inertia_post[0, 2])
        testing.assert_almost_equal(inertia_post[2, 1], inertia_post[1, 2])
        inertia_post = None

        # A more complicated change in position.
        inertia_post = h.inertia_transformed(
                pos=[d + h.center_of_mass[0, 0],
                     h.center_of_mass[1, 0],
                     2 * d + h.center_of_mass[2, 0]])
        offset2 = m * 4 * d**2
        # Moments of inertia.
        testing.assert_almost_equal(
                inertia_post[0, 0], inertia_pre[0, 0] + offset2)
        testing.assert_almost_equal(
                inertia_post[1, 1], inertia_pre[1, 1] + offset + offset2)
        testing.assert_almost_equal(
                inertia_post[2, 2], inertia_pre[2, 2] + offset)
        # Products of inertia.
        testing.assert_almost_equal(inertia_post[0, 1], inertia_pre[0, 1])
        testing.assert_almost_equal(
                inertia_post[0, 2], inertia_pre[0, 2] - m * 2 * d * d)
        testing.assert_almost_equal(inertia_post[1, 2], inertia_pre[1, 2])
        # Symmetry is preserved.
        testing.assert_almost_equal(inertia_post[1, 0], inertia_post[0, 1])
        testing.assert_almost_equal(inertia_post[2, 0], inertia_post[0, 2])
        testing.assert_almost_equal(inertia_post[2, 1], inertia_post[1, 2])
        inertia_post = None

        # A combined change in position and basis. Shift in x and rotation
        # about X.
        inertia_post = h.inertia_transformed(
                pos=[d + h.center_of_mass[0, 0],
                         h.center_of_mass[1, 0],
                         h.center_of_mass[2, 0]],
                rotmat=inertia.rotate_space_123((0.5 * np.pi, 0.0, 0.0)))
        # Moments of inertia.
        testing.assert_almost_equal(inertia_post[0, 0], inertia_pre[0, 0])
        testing.assert_almost_equal(
                inertia_post[1, 1], inertia_pre[2, 2] + offset)
        testing.assert_almost_equal(
                inertia_post[2, 2], inertia_pre[1, 1] + offset)
        # Products of inertia.
        testing.assert_almost_equal(inertia_post[0, 1], inertia_pre[0, 2])
        testing.assert_almost_equal(inertia_post[0, 2], -inertia_pre[0, 1])
        testing.assert_almost_equal(inertia_post[1, 2], -inertia_pre[1, 2])
        # Symmetry is preserved.
        testing.assert_almost_equal(inertia_post[1, 0], inertia_post[0, 1])
        testing.assert_almost_equal(inertia_post[2, 0], inertia_post[0, 2])
        testing.assert_almost_equal(inertia_post[2, 1], inertia_post[1, 2])
        inertia_post = None

        # Make sure the direction of the rotation matrix is correct.
        # Inertia tensor of 2 point mass in the y-z plane; at (2, 1) and (-2,
        # -1), both with mass 1.
        # Rotating a positive atan(1/2) should give a zero xy product of
        # inertia if the rotation matrix is what we think it is.
        inertia_ptmass = np.mat(np.zeros((3, 3)))
        inertia_ptmass[0, 0] = 2 * 1 * (2**2 + 1**1)
        inertia_ptmass[1, 1] = 2 * 1 * (1**1)
        inertia_ptmass[2, 2] = 2 * 1 * (2**2)
        Iyz = 2 * 1 * (2 * 1)
        inertia_ptmass[1, 2] = -Iyz
        inertia_ptmass[2, 1] = -Iyz # symmetry
        angle = np.arctan(1.0 / 2.0)
        # This returns R from va = R * vb:
        rotmat = inertia.rotate_space_123((angle, 0.0, 0.0))
        # Here is a little cheating to test out the method itself with our own
        # center of mass and inertia:
        h._mass = 1
        h._center_of_mass = np.array([[0], [0], [0]])
        h._inertia = inertia_ptmass
        # This expects R from va = R * vb:
        inertia_post = h.inertia_transformed(rotmat=rotmat)
        # Moments of inertia.
        testing.assert_almost_equal(inertia_post[0, 0], inertia_ptmass[0, 0])
        testing.assert_almost_equal(inertia_post[1, 1], 0.0)
        testing.assert_almost_equal(inertia_post[2, 2], inertia_ptmass[0, 0])
        # Products of inertia.
        testing.assert_almost_equal(inertia_post[0, 1], 0.0)
        testing.assert_almost_equal(inertia_post[0, 2], 0.0)
        testing.assert_almost_equal(inertia_post[1, 2], 0.0)
        # Symmetry is preserved.
        testing.assert_almost_equal(inertia_post[1, 0], inertia_post[0, 1])
        testing.assert_almost_equal(inertia_post[2, 0], inertia_post[0, 2])
        testing.assert_almost_equal(inertia_post[2, 1], inertia_post[1, 2])
        inertia_post = None

    def test_lower_torso_rotations(self):
        """Yeadon specifies Euler 1-2-3 rotations (body fixed 1-2-3). For the
        lower torso, this is somersault-tilt-twist relative to the inertial
        reference frame."""

        h = hum.Human(self.male1meas)

        # specify some arbitrary angles
        somersault = pi / 5.0
        tilt = pi / 10.0
        twist = pi / 14.0

        h.set_CFG('somersault', somersault)
        h.set_CFG('tilt', tilt)
        h.set_CFG('twist', twist)

        # Now manually calculate the rotation matrix for Euler 1-2-3 using the
        # inerita.euler_rotation function. Yeadon starts with the I frame
        # (inertial) and rotates the F frame (attached to P) through the body
        # fixed 123 angles.
        # NOTE inertia.euler_rotation has been removed.

        R = inertia.euler_123((somersault, tilt, twist))

        testing.assert_almost_equal(h.P.rot_mat, R)

        # Yeadon presents this rotation matrix on page 3 of his first paper,
        # but it has two errors. The entry Sfi[1, 0] should be `+ sin(phi)`
        # instead of `+ sin(theta)` and the entry Sfi[1, 1] should be
        # `cos(phi)cos(psi) -` instead of `cos(theta)cos(psi) -`. The following
        # is the matrix with the error corrected. His definition of the
        # rotation matrix is:

        # v_i = Sfi * v_f

        # which is the same as the definition in euler_123

        phi = somersault
        theta = tilt
        psi = twist

        cph = np.cos(phi)
        sph = np.sin(phi)
        cth = np.cos(theta)
        sth = np.sin(theta)
        cps = np.cos(psi)
        sps = np.sin(psi)

        Sfi = np.mat(
            [[cth * cps, -cth * sps, sth],
             [cph * sps + sph * sth * cps,
              cph * cps - sph * sth * sps,
              -sph * cth],
             [sph * sps - cph * sth * cps,
              sph * cps + cph * sth * sps,
              cph * cth]])

        testing.assert_almost_equal(h.P.rot_mat, Sfi)

    def test_leg_rotations(self):

        h = hum.Human(self.male1meas)

        elevation = pi / 10.05
        abduction = pi / 68.4

        h.set_CFG('PJ1extension', elevation)
        h.set_CFG('PJ1adduction', -abduction) # should be neg

        RJ = inertia.euler_123((elevation, -abduction, 0.0))

        testing.assert_allclose(h.J1.rot_mat, RJ)

        h.set_CFG('PK1extension', elevation)
        h.set_CFG('PK1abduction', abduction)

        RK = inertia.euler_123((elevation, abduction, 0.0))

        testing.assert_allclose(h.K1.rot_mat, RK)

        flexion = pi / 9.6

        R2 = inertia.euler_123((flexion, 0.0, 0.0))

        h.set_CFG('J1J2flexion', flexion)
        h.set_CFG('K1K2flexion', flexion)

        testing.assert_allclose(h.J2.rot_mat, RJ * R2)
        testing.assert_allclose(h.K2.rot_mat, RK * R2)

        somersault = pi / 5.0
        tilt = pi / 10.0
        twist = pi / 14.0

        h.set_CFG('somersault', somersault)
        h.set_CFG('tilt', tilt)
        h.set_CFG('twist', twist)

        R3 = inertia.euler_123((somersault, tilt, twist))

        # v_p = R3 * v_i
        # v_j1 = R * v_p
        # v_j2 = R2 * v_j1
        # v_j2 = R2 * R * R3 * v_i
        # v_i = R3^T * R^T * R2^T * v_j2

        testing.assert_allclose(h.J2.rot_mat, R3 * RJ * R2)
        testing.assert_allclose(h.K2.rot_mat, R3 * RK * R2)

    def test_arm_rotations(self):
        """Yeadon specifies Euler 1-2-3 rotations (body fixed 1-2-3). For the
        left arm, A, this is elevation-abduction-rotation relative to the C
        body (shoulders/head)."""

        h = hum.Human(self.male1meas)

        elevation = pi / 5.0
        abduction = pi - pi / 10.0
        rotation = pi / 14.0

        h.set_CFG('CA1extension', elevation)
        h.set_CFG('CA1adduction', abduction)
        h.set_CFG('CA1rotation', rotation)

        # now we should manually calculate the rotation matrix for Euler 1-2-3
        # Yeadon starts with the C frame and rotates the F frame
        # (attached to P) through the body fixed 123 angles.

        R = inertia.euler_123((elevation, abduction, rotation))

        testing.assert_allclose(h.A1.rot_mat, R)

        # now rotate the elbow

        flexion = - pi / 4.3

        R2 = inertia.euler_123((flexion, 0.0, 0.0))

        h.set_CFG('A1A2extension', flexion)

        testing.assert_allclose(h.A2.rot_mat, R * R2)

        # right arm

        elevation = pi / 5.0
        abduction = pi - pi / 10.0
        rotation = pi / 14.0

        h.set_CFG('CB1extension', elevation)
        h.set_CFG('CB1abduction', abduction)
        h.set_CFG('CB1rotation', rotation)

        # now we should manually calculate the rotation matrix for Euler 1-2-3
        # Yeadon starts with the C frame and rotates the F frame
        # (attached to P) through the body fixed 123 angles.

        R = inertia.euler_123((elevation, abduction, rotation))

        testing.assert_allclose(h.B1.rot_mat, R)

        # now rotate the elbow
        # v_a1 = R * v_c and v_a2 = R2 * v_a1
        # v_a2 = R2 * R * v_c
        # v_c =  R^T * R2^T * v_a2

        flexion = -pi / 6.98

        R2 = inertia.euler_123((flexion, 0.0, 0.0))

        h.set_CFG('B1B2extension', flexion)

        testing.assert_allclose(h.B2.rot_mat, R * R2)

    def test_rotation_chain(self):
        """This tests all of the rotations in the whole body."""

        h = hum.Human(self.male1meas)

        def angle():
            """Returns a random angle between -2*pi and 2*pi."""
            return 2 * pi * np.random.uniform(-1, 1)

        # rotate the pelvis (P) relative to the inertial frame (I)

        somersault = angle()
        tilt = angle()
        twist = angle()

        h.set_CFG('somersault', somersault)
        h.set_CFG('tilt', tilt)
        h.set_CFG('twist', twist)

        P_R_I = inertia.euler_123((somersault, tilt, twist))

        testing.assert_allclose(h.P.rot_mat, P_R_I)

        # rotate the thorax (T) relative to the pelvis (P)

        sagflexion = angle()
        bending = angle()

        h.set_CFG('PTsagittalFlexion', sagflexion)
        h.set_CFG('PTbending', bending)

        T_R_P = inertia.euler_123((sagflexion, bending, 0.0))

        T_R_I = P_R_I * T_R_P

        testing.assert_allclose(h.T.rot_mat, T_R_I)

        # rotate the chest relative to the thorax

        spinalflexion = angle()
        torsion = angle()

        h.set_CFG('TCsagittalSpinalFlexion', spinalflexion)
        h.set_CFG('TCspinalTorsion', torsion)

        C_R_T = inertia.euler_123((spinalflexion, 0.0, torsion))

        C_R_I = T_R_I * C_R_T

        testing.assert_allclose(h.C.rot_mat, C_R_I)

        # rotate the left upper arm relative to the chest

        extension = angle()
        abduction = angle() # neg
        rotation = angle()

        h.set_CFG('CA1extension', extension)
        h.set_CFG('CA1adduction', abduction)
        h.set_CFG('CA1rotation', rotation)

        A1_R_C = inertia.euler_123((extension, abduction, rotation))

        A1_R_I = C_R_I * A1_R_C

        testing.assert_allclose(h.A1.rot_mat, A1_R_I)

        # rotate the left lower arm relative to the left upper arm

        extension = angle() #neg

        h.set_CFG('A1A2extension', extension)

        A2_R_A1 = inertia.euler_123((extension, 0.0, 0.0))

        A2_R_I = A1_R_I * A2_R_A1

        testing.assert_allclose(h.A2.rot_mat, A2_R_I)

        # rotate the right upper arm relative to the chest

        extension = angle()
        abduction = angle()
        rotation = angle()

        h.set_CFG('CB1extension', extension)
        h.set_CFG('CB1abduction', abduction)
        h.set_CFG('CB1rotation', rotation)

        B1_R_C = inertia.euler_123((extension, abduction, rotation))

        B1_R_I = C_R_I * B1_R_C

        testing.assert_allclose(h.B1.rot_mat, B1_R_I)

        # rotate the left lower arm relative to the left upper arm

        extension = angle() # neg

        h.set_CFG('B1B2extension', extension)

        B2_R_B1 = inertia.euler_123((extension, 0.0, 0.0))

        B2_R_I = B1_R_I * B2_R_B1

        testing.assert_allclose(h.B2.rot_mat, B2_R_I)

        # legs

        # left leg

        elevation = angle()
        abduction = angle() # neg

        h.set_CFG('PJ1extension', elevation)
        h.set_CFG('PJ1adduction', abduction) # should be neg

        J1_R_P = inertia.euler_123((elevation, abduction, 0.0))

        J1_R_I = P_R_I * J1_R_P

        testing.assert_allclose(h.J1.rot_mat, J1_R_I)

        flexion = angle()

        h.set_CFG('J1J2flexion', flexion)

        J2_R_J1 = inertia.euler_123((flexion, 0.0, 0.0))

        J2_R_I = J1_R_I * J2_R_J1

        testing.assert_allclose(h.J2.rot_mat, J2_R_I)

        # right leg

        elevation = angle()
        abduction = angle()

        h.set_CFG('PK1extension', elevation)
        h.set_CFG('PK1abduction', abduction) # should be neg

        K1_R_P = inertia.euler_123((elevation, abduction, 0.0))

        K1_R_I = P_R_I * K1_R_P

        testing.assert_allclose(h.K1.rot_mat, K1_R_I)

        flexion = angle()

        h.set_CFG('K1K2flexion', flexion)

        K2_R_K1 = inertia.euler_123((flexion, 0.0, 0.0))

        K2_R_I = K1_R_I * K2_R_K1

        testing.assert_allclose(h.K2.rot_mat, K2_R_I)

# TODO compare ISEG output to our output.

# TODO try out a program flow: make sure we do all necessary updates after
# construction, say when we change a joint angle, etc. CANNOT just change
# measurements on the fly.
# TODO it's possible that by averaging the measurements, we're coming up
# with more false stadia than we would otherwise, but if we don't average
# the measurements, how do we draw?
