Overview
========

This package calculates the masses, center of mass positions, and inertia
tensors that correspond to the human inertia model developed by Yeadon
in (Yeadon, 1990). The package allows for the input of both measurements and
configuration variables (joint angles), and provides 3D graphical output
using the VPython package.

The package was developed on a Linux Ubuntu personal computer, and so this
README has that bent to it.

References
==========

M. R. Yeadon, 1990. The Simulation of Aerial Movement-ii. Mathematical Inertia
Model of the Human Body. Journal of Biomechanics, 23:67-74.

Directories
===========

- ``yeadon/`` is the root directory of this package
- ``/`` contains two template input .txt files
- ``doc/`` contains source documents for building sphinx documentation.
- ``yeadon/`` contains the python source files for the yeadon package

Installing
==========

This package was developed in Python 2.7. It depends on the following
widely-used packages:

- Numpy_ (debian: python-numpy)
- Matplotlib_ (debian: python-matplotlib)
- vPython_ optional, used for pretty visualization (debian: python-visual)
- Sphinx_  optional, needed to create documentation (debian: python-sphinx)
- numpydoc_ sphinx extension

.. _Numpy: http://numpy.scipy.org
.. _Matplotlib: http://matplotlib.sourceforge.net
.. _vPython: http://www.vpython.org
.. _Sphinx: http://sphinx.pocoo.org
.. _numpydoc: http://pypi.python.org/pypi/numpydoc

In Linux systems, you may be able to obtain those four packages by opening a
terminal window (CTRL-ALT-T) and typing the following line::

    $apt-get install python-numpy python-matplotlib # required
    $apt-get install python-sphinx python-visual # optional packages

For other systems (Windows or Mac), visit the websites for the packages,
given above for installation instructions.

Once you download the yeadon package and decompress it, you can install in
Linux with the commands along the lines of::

    $python setup.py install

or simply use a tool like `pip` ::

    $pip install yeadon

Again, this assumes that you have installed Python 2.7. You can build (create)
the yeadon documentation if you have the python sphinx package (see above) by
typing, in the same yeadon/ directory::

    $cd doc/
    $make html

to make HTML documentation in the yeadon/doc/_build/html folder, or::

    $cd doc/
    $make latex  #(or: make latexpdf)

to generate LaTeX source files in the yeadon/doc/_build/latex.

Usage
=====

In a python script or in the python command prompt (IDLE), import the library
with a line like

::

    >>>import yeadon as y

You can begin the command line interface by executing

::

    >>>y.start_ui()

Then you can follow the instructions provided in the command line interface.
The other way to interact with the package is by creating a human object
with a line (perhaps in your own code) like

::

    >>>H = y.human(<measfilename>, <CFGfilename>)

where `<measfilename>` and `<CFGfilename>` are replaced by strings that contain
a relative or absolute path to the appropriate input `.txt` files. For more
basics on how to use a human object, you can go into a python command prompt and type

::

    >>>import yeadon as y
    >>>help(y.human)

See the HTML or PDF documentation for more information.

Contact
=======

Feel free to contact Chris Dembia (fitzeq@gmail.com) with any questions or
comments.

Post issues to http://github.com/fitze/yeadon/issues.
