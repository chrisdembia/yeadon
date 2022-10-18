yeadon
======

.. image:: https://img.shields.io/pypi/v/yeadon.svg
   :target: https://pypi.python.org/pypi/yeadon/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/yeadon.svg
   :target: https://pypi.python.org/pypi/yeadon/
   :alt: Number of PyPI downloads

.. image:: https://anaconda.org/conda-forge/yeadon/badges/version.svg
   :target: https://anaconda.org/conda-forge/yeadon

.. image:: https://readthedocs.org/projects/yeadon/badge/?version=latest
   :alt: Documentation Status
   :scale: 100%
   :target: https://yeadon.readthedocs.org/en/latest/?badge=latest

.. image:: https://zenodo.org/badge/doi/10.5281/zenodo.15770.svg
   :target: http://dx.doi.org/10.5281/zenodo.15770

.. image:: https://github.com/chrisdembia/yeadon/actions/workflows/runtests.yml/badge.svg

This package calculates the masses, center of mass positions, and inertia
tensors that correspond to the human inertia model developed by Yeadon in
(Yeadon, 1990). The package allows for the input of both measurements and
configuration variables (joint angles), and provides 3D visualization using the
MayaVi package. See the online documentation at
`<http://yeadon.readthedocs.org/>`_.

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

This package was developed for Python 3.7+.

Dependencies
------------

`yeadon` depends on the following widely-used packages:

- setuptools_ for installation
- NumPy_ for computations
- PyYAML_ for parsing input files

.. _setuptools: http://pythonhosted.org/setuptools
.. _NumPy: http://numpy.scipy.org
.. _PyYAML: http://pyyaml.org

The following packages are optional:

- MayaVi_ for visualization and GUI interaction
- nose_ for tests
- Sphinx_ to create documentation
- numpydoc_ Sphinx extension for NumPy-style documentation formatting

.. _MayaVi: http://mayavi.sourceforge.net
.. _nose: https://nose.readthedocs.org
.. _Sphinx: http://sphinx.pocoo.org
.. _numpydoc: http://pythonhosted.org/numpydoc

Getting the dependencies
------------------------

Option 1: Scientific python distributions
`````````````````````````````````````````

Most `scientific python distributions
<http://www.scipy.org/install.html#scientific-python-distributions>`_ provide
all of these dependencies and it is often easiest to install one of them to get
started. Once you have a distribution, you can install the yeadon package. This
is the best solution for Windows users.

Option 2: Operating system package manager
``````````````````````````````````````````

In some operating systems, the dependencies can also be obtained from the
operating system's package manager. For example, in Debian systems, you should
be able to obtain all of these packages by opening a terminal window and
typing::

   $ # prepend sudo to each line below if you desire a system install
   $ apt-get install python3-setuptools python3-numpy python3-yaml # required
   $ apt-get install python3-nose python3-sphinx python3-numpydoc mayavi2 # optional packages

For other operating systems (e.g. Windows or Mac), visit the websites for the
packages for installation instructions.

Option 3: Building dependencies from source
```````````````````````````````````````````

This option is required if you want to use `yeadon` in a virtualenv. You can
build the dependencies from source and then install them by using a tool like
`pip`::

    $ python -m pip install numpy PyYAML
    $ python -m pip install nose sphinx mayavi
    $ python -m pip install numpydoc

or you can obtain the source code, perhaps from GitHub_, and install the
packages manually.

.. _GitHub: http://github.com

Getting yeadon
--------------

Once you've obtained the dependencies, you can install `yeadon`. The
easiest way to download and install the `yeadon` package is by using a tool
like `pip` to obtain the package from the Python Package Index (PyPi)::

   $ python -m pip install yeadon # sudo if system install

You can also obtain an archive of the package at the Python Package Index
(`<https://pypi.python.org/pypi/yeadon>`_), and then install the package on your
own by executing the following from the root directory of the package::

   $ python setup.py install # sudo if system install

On Unix, you can obtain the package source code and install it without leaving
your terminal::

   $ # change X.X.X to the desired version
   $ wget https://pypi.python.org/packages/source/y/yeadon/yeadon-X.X.X.tar.gz
   $ tar -zxfv yeadon-X.X.X.tar.gz
   $ cd yeadon-X.X.X.tar.gz
   $ python setup.py install # sudo if system install

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
the UI with command-line flags::

   $ yeadon --gui
   $ yeadon --ui

You can also interact with `yeadon` in a Python interpreter session or Python
script/module via the API by importing the package. For example::

   $ python
   >>> import yeadon

Now you can create a human object with::

   >>> human = yeadon.Human(<measfilename>, <CFGfilename>)

where `<measfilename>` and `<CFGfilename>` are replaced by strings that contain
a relative or absolute path to the appropriate input `.txt` files. For more
basics on how to use a `Human` object, you can go into a python command prompt
and type::

   >>> help(yeadon.Human)

or see the documentation.

You can also start the UI or the GUI from within a Python interpreter by
executing::

   >>> yeadon.start_ui()

or::

   >>> yeadon.start_gui()

See the documentation for more information.

Cite us!
========

If you make use of the yeadon software we would welcome a citation in your
publications. Please cite this software paper:

Dembia C, Moore JK and Hubbard M. An object oriented implementation of the
Yeadon human inertia model, F1000Research 2014, 3:223 (doi:
https://dx.doi.org/10.12688/f1000research.5292.1)

Contact
=======

Feel free to contact Chris Dembia (chris530d, gmail) with any questions or
comments.

All development is handled at `<http://github.com/chrisdembia/yeadon>`_, including
issue tracking.
