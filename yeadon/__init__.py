from yeadon.human import Human
from yeadon.ui import start_ui
from yeadon.version import __version__

try:
    import mayavi
except ImportError:
    pass
else:
    del mayavi
    try:
        from yeadon.gui import start_gui
    except AttributeError as e:
        if 'in1d' in str(e):
            print('Installed VTK not compatible with NumPy >= 2.4, '
                  'Mayavi ignored.')
            pass
        else:
            raise
