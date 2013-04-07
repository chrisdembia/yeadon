Overview
========

This package calculates the masses, center of mass positions, and inertia
tensors that correspond to the human inertia model developed by Yeadon in
(Yeadon, 1990). The package allows for the input of both measurements and
configuration variables (joint angles), and provides 3D visualization using the
MayaVi package. See the online documentation at
`<http://pythonhosted.org/yeadon>`_.

References
==========

M. R. Yeadon, 1990. The Simulation of Aerial Movement-ii. Mathematical Inertia
Model of the Human Body. Journal of Biomechanics, 23:67-74.

Directories
===========

- ``yeadon/`` contains the python source files for the yeadon package.
- ``doc/`` contains source documents for building sphinx documentation.
- ``misc/`` contains figures and template input files.
- ``misc/samplemeasurements/`` contains sample measurement input files.

Installing
==========

This package was developed in Python 2.7. It depends on the following
widely-used packages:

- setuptools_ or distribute_ for installation, distribute is preferred
- NumPy_ basic array manipulations and computations
- PyYAML_ used for the input files

.. _setuptools: http://pythonhosted.org/setuptools
.. _distribute: http://pytonhosted.org/distribute
.. _NumPy: http://numpy.scipy.org
.. _PyYAML: http://pyyaml.org

The following packages are optional:

- MayaVi_ used for pretty visualization and GUI interaction
- nose_ used for unit tests
- Sphinx_  needed to create documentation
- numpydoc_ sphinx extension for NumPy-style documentation formatting

.. _MayaVi: http://mayavi.sourceforge.net
.. _nose: https://nose.readthedocs.org
.. _Sphinx: http://sphinx.pocoo.org
.. _numpydoc: http://pythonhosted.org/numpydoc

Most `scientific python distributions
<http://numfocus.org/projects-2/software-distributions/>`_ provide all of these
dependencies and it is often easiest to install one of them to get started. Once
you have a distribution, you simply have to install the yeadon package. This is
the best solution for Windows users.

The dependencies can also be obtained easily from your operating system's
package manager. For example, in Debian systems, you should be able to obtain
all of these packages by opening a terminal window (CTRL-ALT-T) and typing::

   $ # use sudo if system install is desired
   $ apt-get install python-distribute python-numpy python-yaml # required
   $ apt-get install python-nose python-sphinx mayavi2 # optional packages
   $ easy_install numpydoc # only on PyPi

For other operating systems (e.g. Windows or Mac), visit the websites for the
packages for installation instructions.

The easiest way to download and install the yeadon package is by using a tool
like `pip` to get the package from PyPi::

   $ easy_install pip
   $ pip install yeadon # sudo if system install

An alternative for downloading and installing on a Unix system that does not
rely on a tool like `pip` is as follows::

   $ # change X.X.X to the desired version
   $ wget https://pypi.python.org/packages/source/y/yeadon/yeadon-X.X.X.tar.gz
   $ tar -zxfv yeadon-X.X.X.tar.gz
   $ cd yeadon-X.X.X.tar.gz
   $ python setup.py install # sudo if system install

Both of these options assume that your default Python interpreter is version
2.7.

Run the tests with::

   $ python setup.py nosetests

Building the documentation
==========================

You can build the yeadon HTML documentation if you have Sphinx by typing the
following from the root directory of the yeadon source files::

   $ cd doc/
   $ make html

You can open the documentation in your favorite web browser::

   $ firefox _build/html/index.html

If you have a LaTeX distribution installed you can build the LaTeX docs with::

   $ cd doc/
   $ make latexpdf

and view the document with your preferred PDF viewer::

   $ evince _build/latex/yeadon.pdf

Note that to generate documentation, one also needs the `numpydoc` package.
Alternatively, one can just access the documentation through the `PyPi` site.

Usage
=====

Once the package is installed you can start the program with::

   $ yeadon

If you have MayaVi installed, the GUI will launch. If you don't, the text based
UI will launch. You can explicitly specify whether you want to load the GUI or
the UI with these flags::

   $ yeadon --gui
   $ yeadon --ui

You can also interact with yeadon in a Python interpreter session or Python
script/module via the API by importing the package. For example::

   $ python
   >>> import yeadon

Now you can create a human object with::

   >>> human = yeadon.Human(<measfilename>, <CFGfilename>)

where `<measfilename>` and `<CFGfilename>` are replaced by strings that contain
a relative or absolute path to the appropriate input `.txt` files. For more
basics on how to use a human object, you can go into a python command prompt and
type::

   >>> help(yeadon.Human)

or see the documentation.

You can also start the UI or the GUI by executing::

   >>> yeadon.start_ui()

or::

   >>> yeadon.start_gui()

within a Python interpreter. See the HTML or PDF documentation for more
information.

Contact
=======

Feel free to contact Chris Dembia (chris530d, gmail) with any questions or
comments.

All development is handled at `<http://github.com/fitze/yeadon>`_, including issue
tracking.
