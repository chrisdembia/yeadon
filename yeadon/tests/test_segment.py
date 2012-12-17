from numpy import testing, pi

import solid as sol
import segment as seg
import inertia

def setup_func():
    # Make a few surfaces.
    surfA = sol.Stadium('surfA', 'perimwidth', 2, 1)
    surfB = sol.Stadium('surfB', 'depthwidth', 3, 4)
    surfC = sol.Stadium('surfC', 'thickradius', 5, 6)
    surfD = sol.Stadium('surfD', 'perimwidth', 8, 4)
    # Make solids for use with segments.
    solidAB = sol.StadiumSolid('stadsolAB', 2, surfA, surfB, 5)
    solidBC = sol.StadiumSolid('stadsolBC', 3, surfB, surfC, 6)
    solidCD = sol.StadiumSolid('stadsolCD', 4, surfC, surfD, 7)

def test_init_real_input():
    # Create parameters.
    label = 'seg1'
    pos = np.array([1, 2, 3])
    rot = inertia.rotate3([pi / 2, pi / 2, pi / 2])
    solids = [solidAB, solidBC, solidCD]
    color = (1, 0, 0)

    seg1 = seg.Segment(label, pos, rot, solids, color)

    # Check that parameters were set.
    assert seg1.label == label
    assert seg1.pos == pos
    assert seg1.RotMat == rot
    assert seg1.solids == solids
    assert seg1.nSolids == len(solids)
    assert seg1.color == color

    # -- Check the other constructor actions.
    # Setting orientations of all constituent solids.
    assert seg1.solids[0].pos == pos
    assert seg1.solids[0].RotMat == rot
    assert seg1.solids[0].endpos == np.array([6, 2, 3])

def test_init_bad_input():
    # Ensures only proper input gets through.
    pass


