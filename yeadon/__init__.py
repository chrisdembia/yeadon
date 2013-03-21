from yeadon.human import Human
from yeadon.ui import start_ui

try:
    import mayavi
except ImportError:
    pass
else:
    del mayavi
    from yeadon.gui import start_gui
