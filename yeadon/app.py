#!/usr/bin/env python

"""Runs the GUI or the UI. The UI is a fallback if MayaVi is not installed."""

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Yeadon command line options.')

    parser.add_argument('-g', '--gui', action="store_true",
        help='Runs the graphical user interface.')

    parser.add_argument('-u', '--ui', action="store_true",
        help='Runs the text based user interface.')

    args = parser.parse_args()

    try:
        import mayavi
    except ImportError:
        print("MayaVi is not installed, resorting to text based user interface.")
        has_mayavi = False
    else:
        del mayavi
        has_mayavi = True

    if args.ui == True or has_mayavi == False:
        from yeadon.ui import start_ui
        start_ui()
    else:
        from yeadon.gui import start_gui
        start_gui()
