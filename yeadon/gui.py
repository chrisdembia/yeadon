import numpy as np

from traits.api import HasTraits, Range, Instance, \
        on_trait_change, Array, Tuple, Str
from traitsui.api import View, Item, HSplit, Group

from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor

from human import Human

class GUI(HasTraits):
    ''' TODO '''

    myPi = 3.14
    opts = {'enter_set': True, 'auto_set': True}
    somersalt              = Range(-myPi, myPi, 0.0, **opts)
    tilt                   = Range(-myPi, myPi, 0.0, **opts)
    twist                  = Range(-myPi, myPi, 0.0, **opts)
    PTsagittalFlexion      = Range(-myPi/2, myPi, 0.0, **opts)
    PTfrontalFlexion       = Range(-myPi/2, myPi/2, 0.0, **opts)
    TCspinalTorsion        = Range(-myPi/2, myPi/2, 0.0, **opts)
    TClateralSpinalFlexion = Range(-myPi/2, myPi/2, 0.0, **opts)
    CA1elevation           = Range(-myPi/2, myPi*3/2, 0.0, **opts)
    CA1abduction           = Range(-myPi*3/2, myPi, 0.0, **opts)
    CA1rotation            = Range(-myPi, myPi, 0.0, **opts)
    CB1elevation           = Range(-myPi/2, myPi*3/2, 0.0, **opts)
    CB1abduction           = Range(-myPi*3/2, myPi, 0.0, **opts)
    CB1rotation            = Range(-myPi, myPi, 0.0, **opts)
    A1A2flexion            = Range(0, myPi, 0.0, **opts)
    B1B2flexion            = Range(0, myPi, 0.0, **opts)
    PJ1flexion             = Range(-myPi/2, myPi, 0.0, **opts)
    PJ1abduction           = Range(-myPi/2, myPi/2, 0.0, **opts)
    PK1flexion             = Range(-myPi/2, myPi, 0.0, **opts)
    PK1abduction           = Range(-myPi/2, myPi/2, 0.0, **opts)
    J1J2flexion            = Range(0, myPi, 0.0, **opts)
    K1K2flexion            = Range(0, myPi, 0.0, **opts)

    scene = Instance(MlabSceneModel, args=())

    view = View(HSplit(
        Group(
            Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                height=500, width=500, show_label=False)),
        Group(
            Item('somersalt'),
            Item('tilt'),
            Item('twist'),
            Item('PTsagittalFlexion'),
            Item('PTfrontalFlexion'),
            Item('TCspinalTorsion'),
            Item('TClateralSpinalFlexion'),
            Item('CA1elevation'),
            Item('CA1abduction'),
            Item('CA1rotation'),
            Item('CB1elevation'),
            Item('CB1abduction'),
            Item('CB1rotation'),
            Item('A1A2flexion'),
            Item('B1B2flexion'),
            Item('PJ1flexion'),
            Item('PJ1abduction'),
            Item('PK1flexion'),
            Item('PK1abduction'),
            Item('J1J2flexion'),
            Item('K1K2flexion'))
        ),
        resizable=True
        )

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

    def __init__(self):
        HasTraits.__init__(self)
        self.H = Human(self.measPreload)
        self.H.draw_mayavi(self.scene.mlab)

    @on_trait_change('somersalt')
    def update_somersalt(self):
        self.H.set_CFG('somersalt', self.somersalt)
        self._update_mayavi()

    @on_trait_change('tilt')
    def update_tilt(self):
        self.H.set_CFG('tilt', self.tilt)
        self._update_mayavi()

    @on_trait_change('twist')
    def update_twist(self):
        self.H.set_CFG('twist', self.twist)
        self._update_mayavi()

    @on_trait_change('PTsagittalFlexion')
    def update_PTsagittalFlexion(self):
        self.H.set_CFG('PTsagittalFlexion', self.PTsagittalFlexion)
        self._update_mayavi(['T', 'C', 'A1', 'A2', 'B1', 'B2'])

    @on_trait_change('PTfrontalFlexion')
    def update_PTfrontalFlexion(self):
        self.H.set_CFG('PTfrontalFlexion', self.PTfrontalFlexion)
        self._update_mayavi(['T', 'C', 'A1', 'A2', 'B1', 'B2'])

    @on_trait_change('TCspinalTorsion')
    def update_TCspinalTorsion(self):
        self.H.set_CFG('TCspinalTorsion', self.TCspinalTorsion)
        self._update_mayavi(['C', 'A1', 'A2', 'B1', 'B2'])

    @on_trait_change('TClateralSpinalFlexion')
    def update_TClateralSpinalFlexion(self):
        self.H.set_CFG('TClateralSpinalFlexion', self.TClateralSpinalFlexion)
        self._update_mayavi(['C', 'A1', 'A2', 'B1', 'B2'])

    @on_trait_change('CA1elevation')
    def update_CA1elevation(self):
        self.H.set_CFG('CA1elevation', self.CA1elevation)
        self._update_mayavi(['A1', 'A2'])

    @on_trait_change('CA1abduction')
    def update_CA1abduction(self):
        self.H.set_CFG('CA1abduction', self.CA1abduction)
        self._update_mayavi(['A1', 'A2'])

    @on_trait_change('CA1rotation')
    def update_CA1rotation(self):
        self.H.set_CFG('CA1rotation', self.CA1rotation)
        self._update_mayavi(['A1', 'A2'])

    @on_trait_change('CB1elevation')
    def update_CB1elevation(self):
        self.H.set_CFG('CB1elevation', self.CB1elevation)
        self._update_mayavi(['B1', 'B2'])

    @on_trait_change('CB1abduction')
    def update_CB1abduction(self):
        self.H.set_CFG('CB1abduction', self.CB1abduction)
        self._update_mayavi(['B1', 'B2'])

    @on_trait_change('CB1rotation')
    def update_CB1rotation(self):
        self.H.set_CFG('CB1rotation', self.CB1rotation)
        self._update_mayavi(['B1', 'B2'])

    @on_trait_change('A1A2flexion')
    def update_A1A2flexion(self):
        self.H.set_CFG('A1A2flexion', self.A1A2flexion)
        self._update_mayavi(['A2'])

    @on_trait_change('B1B2flexion')
    def update_B1B2flexion(self):
        self.H.set_CFG('B1B2flexion', self.B1B2flexion)
        self._update_mayavi(['B2'])

    @on_trait_change('PJ1flexion')
    def update_PJ1flexion(self):
        self.H.set_CFG('PJ1flexion', self.PJ1flexion)
        self._update_mayavi(['J1', 'J2'])

    @on_trait_change('PJ1abduction')
    def update_PJ1abduction(self):
        self.H.set_CFG('PJ1abduction', self.PJ1abduction)
        self._update_mayavi(['J1', 'J2'])

    @on_trait_change('PK1flexion')
    def update_PK1flexion(self):
        self.H.set_CFG('PK1flexion', self.PK1flexion)
        self._update_mayavi(['K1', 'K2'])

    @on_trait_change('PK1abduction')
    def update_PK1abduction(self):
        self.H.set_CFG('PK1abduction', self.PK1abduction)
        self._update_mayavi(['K1', 'K2'])

    @on_trait_change('J1J2flexion')
    def update_J1J2flexion(self):
        self.H.set_CFG('J1J2flexion', self.J1J2flexion)
        self._update_mayavi(['J2'])

    @on_trait_change('K1K2flexion')
    def update_K1K2flexion(self):
        self.H.set_CFG('K1K2flexion', self.K1K2flexion)
        self._update_mayavi(['K2'])

    def _update_mayavi(self, segments=None):
        """Updates all of the segments and solids."""
        if segments is None:
            self.H.update_mayavi()
        else:
            for affected in segments:
                self.H.get_segment_by_name(affected).update_mayavi()

if __name__ == '__main__':
    g = GUI()
    g.configure_traits()
