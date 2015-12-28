#!/usr/bin/env python

from numpy import deg2rad, rad2deg

from traits.api import HasTraits, Range, Instance, \
        on_trait_change, Float, Property, File, Bool, Button
from traitsui.api import \
        View, Item, VSplit, VGroup, HSplit, HGroup, Group, Label

from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor

from .human import Human

sliders = Human.CFGnames

def format_func(value):
    return '{:1.3}'.format(value)

class YeadonGUI(HasTraits):
    """A GUI for the yeadon module, implemented using the traits package."""

    # Input.
    measurement_file_name = File()

    # Drawing options.
    show_mass_center = Bool(False)
    show_inertia_ellipsoid = Bool(False)

    # Configuration variables.
    opts = {'enter_set': True, 'auto_set': True, 'mode': 'slider'}
    for name, bounds in zip(Human.CFGnames, Human.CFGbounds):
        # TODO : Find a better way than using locals here, it may not be a good
        # idea, but I don't know the consequences.
        locals()[name] =  Range(float(rad2deg(bounds[0])),
            float(rad2deg(bounds[1])), 0.0, **opts)

    reset_configuration = Button()

    # Display of Human object properties.
    Ixx = Property(Float, depends_on=sliders)
    Ixy = Property(Float, depends_on=sliders)
    Ixz = Property(Float, depends_on=sliders)
    Iyx = Property(Float, depends_on=sliders)
    Iyy = Property(Float, depends_on=sliders)
    Iyz = Property(Float, depends_on=sliders)
    Izx = Property(Float, depends_on=sliders)
    Izy = Property(Float, depends_on=sliders)
    Izz = Property(Float, depends_on=sliders)
    x = Property(Float, depends_on=sliders)
    y = Property(Float, depends_on=sliders)
    z = Property(Float, depends_on=sliders)

    scene = Instance(MlabSceneModel, args=())

    input_group = Group(Item('measurement_file_name'))

    vis_group = Group(Item('scene',
        editor=SceneEditor(scene_class=MayaviScene), height=580, width=430,
        show_label=False))

    config_first_group = Group(
            Item('somersault'),
            Item('tilt'),
            Item('twist'),
            Item('PTsagittalFlexion', label='PT sagittal flexion'),
            Item('PTbending', label='PT bending'),
            Item('TCspinalTorsion', label='TC spinal torsion'),
            Item('TCsagittalSpinalFlexion',
                label='TC sagittal spinal flexion'),
            label='Whole-body, pelvis, torso',
            dock='tab',
            )
    config_upper_group = Group(
            Item('CA1extension', label='CA1 extension'),
            Item('CA1adduction', label='CA1 adduction'),
            Item('CA1rotation', label='CA1 rotation'),
            Item('CB1extension', label='CB1 extension'),
            Item('CB1abduction', label='CB1 abduction'),
            Item('CB1rotation', label='CB1 rotation'),
            Item('A1A2extension', label='A1A2 extension'),
            Item('B1B2extension', label='B1B2 extension'),
            label='Upper limbs',
            dock='tab',
            )
    config_lower_group = Group(
            Item('PJ1extension', label='PJ1 extension'),
            Item('PJ1adduction', label='PJ1 adduction'),
            Item('PK1extension', label='PK1 extension'),
            Item('PK1abduction', label='PK1 abduction'),
            Item('J1J2flexion', label='J1J2 flexion'),
            Item('K1K2flexion', label='K1K2 flexion'),
            label='Lower limbs',
            dock='tab',
            )
    config_group = VGroup(
            Label('Configuration'),
            Group(config_first_group, config_upper_group, config_lower_group,
                layout='tabbed',
                ),
            Item('reset_configuration', show_label=False),
            Label('P: pelvis (red); T: thorax (orange); C: chest-head (yellow)'),
            Label('A1/A2: left upper arm/forearm-hand; B1/B2: right arm'),
            Label('J1/J2: left thigh/shank-foot; K1/K2: right leg'),
            show_border=True,
            )

    inertia_prop = VGroup(
            Label('Mass center (from origin of coord. sys.) (m):'),
            HGroup(
                Item('x', style='readonly', format_func=format_func),
                Item('y', style='readonly', format_func=format_func),
                Item('z', style='readonly', format_func=format_func)
                ),
            Label('Inertia tensor (about origin, in basis shown) (kg-m^2):'),
            HSplit( # HSplit 2
                Group(
                    Item('Ixx', style='readonly', format_func=format_func),
                    Item('Iyx', style='readonly', format_func=format_func),
                    Item('Izx', style='readonly', format_func=format_func),
                    ),
                Group(
                    Item('Ixy', style='readonly', format_func=format_func),
                    Item('Iyy', style='readonly', format_func=format_func),
                    Item('Izy', style='readonly', format_func=format_func),
                    ),
                Group(
                    Item('Ixz', style='readonly', format_func=format_func),
                    Item('Iyz', style='readonly', format_func=format_func),
                    Item('Izz', style='readonly', format_func=format_func)
                    ),
                ), # end HSplit 2
            Label('X, Y, Z axes drawn as red, green, blue arrows, respectively.'),
                show_border=True,
            ) # end VGroup

    view = View(
            VSplit(
                input_group,
                HSplit(vis_group,
                    VSplit(
                        config_group,
                        Item('show_mass_center'),
                        Item('show_inertia_ellipsoid'),
                        inertia_prop
                        )
                    ),
                ),
            resizable=True,
            title='Yeadon human inertia model'
            ) # end View

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

    def __init__(self, meas_in=None):
        HasTraits.__init__(self, trait_value=True)
        if meas_in:
            measurement_file_name = meas_in
        else:
            measurement_file_name = 'Path to measurement input text file.'
        self.H = Human(meas_in if meas_in else self.measPreload)
        self._init_draw_human()

    def _init_draw_human(self):
        self.H.draw(self.scene.mlab, True)

        if self.show_mass_center:
            self.H._draw_mayavi_mass_center_sphere(self.scene.mlab)

        if self.show_inertia_ellipsoid:
            self.H._draw_mayavi_inertia_ellipsoid(self.scene.mlab)

    @on_trait_change('scene.activated')
    def set_view(self):
        """Sets a reasonable camera angle for the intial view."""
        self.scene.mlab.view(azimuth=90.0, elevation=-90.0)

    def _get_Ixx(self):
        return self.H.inertia[0, 0]

    def _get_Ixy(self):
        return self.H.inertia[0, 1]

    def _get_Ixz(self):
        return self.H.inertia[0, 2]

    def _get_Iyx(self):
        return self.H.inertia[1, 0]

    def _get_Iyy(self):
        return self.H.inertia[1, 1]

    def _get_Iyz(self):
        return self.H.inertia[1, 2]

    def _get_Izx(self):
        return self.H.inertia[2, 0]

    def _get_Izy(self):
        return self.H.inertia[2, 1]

    def _get_Izz(self):
        return self.H.inertia[2, 2]

    def _get_x(self):
        return self.H.center_of_mass[0, 0]

    def _get_y(self):
        return self.H.center_of_mass[1, 0]

    def _get_z(self):
        return self.H.center_of_mass[2, 0]

    @on_trait_change('measurement_file_name')
    def _update_measurement_file_name(self):
        # Must convert to str (from unicode), because Human parses it
        # differently depending on its type, and there's no consideration for
        # it being unicode.
        self.H = Human(str(self.measurement_file_name))
        self.scene.mlab.clf()
        self._init_draw_human()

    @on_trait_change('show_inertia_ellipsoid')
    def _update_show_inertia_ellipsoid(self):
        if self.show_inertia_ellipsoid:
            self.H._draw_mayavi_inertia_ellipsoid(self.scene.mlab)
        else:
            self.H._ellipsoid_mesh.remove()

    def _maybe_update_inertia_ellipsoid(self):
        if self.show_inertia_ellipsoid:
            self.H._update_mayavi_inertia_ellipsoid()

    @on_trait_change('show_mass_center')
    def _update_show_mass_center(self):
        if self.show_mass_center:
            self.H._draw_mayavi_mass_center_sphere(self.scene.mlab)
        else:
            self.H._mass_center_sphere.remove()

    def _maybe_update_mass_center(self):
        if self.show_mass_center:
            self.H._update_mayavi_mass_center_sphere()

    @on_trait_change('reset_configuration')
    def _update_reset_configuration(self):
        # TODO: This is really slow because it sets every trait one by one. It
        # would be nice to set them all to zero and only call the redraw once.
        for cfg in sliders:
            setattr(self, cfg, self.trait(cfg).default_value()[1])

    @on_trait_change('somersault')
    def _update_somersault(self):
        self.H.set_CFG('somersault', deg2rad(self.somersault))
        self._update_mayavi(['P', 'T', 'C', 'A1', 'A2', 'B1', 'B2', 'J1', 'J2',
            'K1', 'K2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('tilt')
    def _update_tilt(self):
        self.H.set_CFG('tilt', deg2rad(self.tilt))
        self._update_mayavi(['P', 'T', 'C', 'A1', 'A2', 'B1', 'B2', 'J1', 'J2',
            'K1', 'K2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('twist')
    def _update_twist(self):
        self.H.set_CFG('twist', deg2rad(self.twist))
        self._update_mayavi(['P', 'T', 'C', 'A1', 'A2', 'B1', 'B2', 'J1', 'J2',
            'K1', 'K2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('PTsagittalFlexion')
    def _update_PTsagittalFlexion(self):
        self.H.set_CFG('PTsagittalFlexion', deg2rad(self.PTsagittalFlexion))
        self._update_mayavi(['T', 'C', 'A1', 'A2', 'B1', 'B2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('PTbending')
    def _update_PTFrontalFlexion(self):
        self.H.set_CFG('PTbending', deg2rad(self.PTbending))
        self._update_mayavi(['T', 'C', 'A1', 'A2', 'B1', 'B2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('TCspinalTorsion')
    def _update_TCSpinalTorsion(self):
        self.H.set_CFG('TCspinalTorsion', deg2rad(self.TCspinalTorsion))
        self._update_mayavi(['C', 'A1', 'A2', 'B1', 'B2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('TCsagittalSpinalFlexion')
    def _update_TCLateralSpinalFlexion(self):
        self.H.set_CFG('TCsagittalSpinalFlexion',
                deg2rad(self.TCsagittalSpinalFlexion))
        self._update_mayavi(['C', 'A1', 'A2', 'B1', 'B2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('CA1extension')
    def _update_CA1extension(self):
        self.H.set_CFG('CA1extension', deg2rad(self.CA1extension))
        self._update_mayavi(['A1', 'A2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('CA1adduction')
    def _update_CA1adduction(self):
        self.H.set_CFG('CA1adduction', deg2rad(self.CA1adduction))
        self._update_mayavi(['A1', 'A2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('CA1rotation')
    def _update_CA1rotation(self):
        self.H.set_CFG('CA1rotation', deg2rad(self.CA1rotation))
        self._update_mayavi(['A1', 'A2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('CB1extension')
    def _update_CB1extension(self):
        self.H.set_CFG('CB1extension', deg2rad(self.CB1extension))
        self._update_mayavi(['B1', 'B2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('CB1abduction')
    def _update_CB1abduction(self):
        self.H.set_CFG('CB1abduction', deg2rad(self.CB1abduction))
        self._update_mayavi(['B1', 'B2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('CB1rotation')
    def _update_CB1rotation(self):
        self.H.set_CFG('CB1rotation', deg2rad(self.CB1rotation))
        self._update_mayavi(['B1', 'B2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('A1A2extension')
    def _update_A1A2extension(self):
        self.H.set_CFG('A1A2extension', deg2rad(self.A1A2extension))
        self._update_mayavi(['A2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('B1B2extension')
    def _update_B1B2extension(self):
        self.H.set_CFG('B1B2extension', deg2rad(self.B1B2extension))
        self._update_mayavi(['B2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('PJ1extension')
    def _update_PJ1extension(self):
        self.H.set_CFG('PJ1extension', deg2rad(self.PJ1extension))
        self._update_mayavi(['J1', 'J2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('PJ1adduction')
    def _update_PJ1adduction(self):
        self.H.set_CFG('PJ1adduction', deg2rad(self.PJ1adduction))
        self._update_mayavi(['J1', 'J2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('PK1extension')
    def _update_PK1extension(self):
        self.H.set_CFG('PK1extension', deg2rad(self.PK1extension))
        self._update_mayavi(['K1', 'K2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('PK1abduction')
    def _update_PK1abduction(self):
        self.H.set_CFG('PK1abduction', deg2rad(self.PK1abduction))
        self._update_mayavi(['K1', 'K2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('J1J2flexion')
    def _update_J1J2flexion(self):
        self.H.set_CFG('J1J2flexion', deg2rad(self.J1J2flexion))
        self._update_mayavi(['J2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    @on_trait_change('K1K2flexion')
    def _update_K1K2flexion(self):
        self.H.set_CFG('K1K2flexion', deg2rad(self.K1K2flexion))
        self._update_mayavi(['K2'])
        self._maybe_update_mass_center()
        self._maybe_update_inertia_ellipsoid()

    def _update_mayavi(self, segments):
        """Updates all of the segments and solids."""
        for affected in segments:
            seg = self.H.get_segment_by_name(affected)
            for solid in seg.solids:
                solid._mesh.scene.disable_render = True
        for affected in segments:
            self.H.get_segment_by_name(affected)._update_mayavi()
        for affected in segments:
            seg = self.H.get_segment_by_name(affected)
            for solid in seg.solids:
                solid._mesh.scene.disable_render = False

def start_gui(*args, **kwargs):
    '''Start the GUI. The GUI automatically creates a Human, and lets the user
    modify its configuration and observe the resulting change in the human's
    inertia properties.

    Parameters
    ----------
    meas_in : str, optional
        The filename of a measurements file to use for the human.
    '''
    gui = YeadonGUI(*args, **kwargs)
    gui.configure_traits()

if __name__ == '__main__':
    start_gui()
