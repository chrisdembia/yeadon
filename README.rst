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

``yeadon/`` is the root directory of this packages
``/`` contains two template input .txt files
``build/`` is filled up when creating documentation or installing the package
``dist/`` is filled when running "python setup.p sdist" in bash.
``doc/`` contains source documents for building sphinx documentation.
``yeadon/`` contains the python source files


Installing
==========

This package was developed in Python 2.7. It depends on the following
widely-used packages:

-numpy (python-numpy) numpy.scipy.orgzo
-matplotlib (python-matplotlib) matplotlib.sourceforge.net
-vpython (python-visual) www.vpython.org
-sphinx sphinx.pocoo.org (optional, needed to create documentation)

In Linux systems, you may be able to obtain those four packages by opening a
terminal window (CTRL-ALT-T) and typing the following line::
    sudo apt-get install python-numpy python-matplotlib python-visual

For other systems (Windows or Mac), visit the websites for the packages,
given above.

The code also depends on a package called DynamicistToolKit. This is
available from a GIT repository hosted by www.github.com at

    https://github.com/moorepants/DynamicistToolKit

You can download that python package from the URL above. If you are using a
Linux system, you can also open up a terminal window and execute the
lines below to install the package, assuming you have Python 2.7 installed.

::

    $cd ~/    #(or choose any dir. to download the files to)
    $sudo apt-get install git
    $git clone https://github.com/moorepants/DynamicistToolKit
    $cd DynamicistToolKit
    $python setup.py install

The procedure for installing this yeadon package is similar. It is available
on www.github.com as a GIT repository at

    https://github.com/fitze/yeadon

You can install the python package in Linux with the commands along the lines
of::
    $cd ~/
    $sudo apt-get install git
    $git clone https://github.com/fitze/yeadon
    $cd yeadon
    $python setup.py install

Again, this assumes that you have installed Python 2.7. You can build (create)
the yeadon documentation if you have the python sphinx package (see above) by
typing, in the same yeadon/ directory

::
    $cd doc/
    $make html

to make HTML documentation in the yeadon/doc/_build/html folder, or

::
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

    >>>H = y.human(<measfilename>,<CFGfilename>)

where <measfilename> and <CFGfilename> are replaced by strings that contain
a relative or absolute path to the appropriate input .txt files. For more
basics on how to use a human object, you can go into a python command prompt
(IDLE) and type

::

    >>>import yeadon as y
    >>>help(y.human)

See the HTML or PDF documentation for more information.

Feel free to contact Chris Dembia (fitzeq@gmail.com) with any questions or
comments.
