.. yeadon documentation master file, created by
   sphinx-quickstart on Thu Jun 30 16:11:26 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ``yeadon``'s documentation!
==================================

This package calculates the masses, center of mass positions, and inertia
tensors that correspond to the human inertia model developed by Yeadon
in (Yeadon, 1990). The package allows for the input of both measurements from
human subjects and configuration variables (joint angles) with which one can
orient the model. Additionally, the package allows for 3D visualization of the
model using the MayaVi package.

The following is the contents of this documentation:

.. toctree::
   :maxdepth: 1

   overview.rst
   usage.rst
   measurements.rst
   configuration.rst
   releasenotes.rst
   apidoc.rst

The README.rst file contained in the source distribution contains installation
instructions.

This package was developed during the Summer of 2011 at the University of
California, Davis, to aid with the bicycle research of Jason Moore and Dale
Luke Peterson in the Sports Biomechanics Lab of Professor Mont Hubbard. Learn
more about the Sports Biomechanics Lab at `biosport.ucdavis.edu
<http://biosport.ucdavis.edu>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

References
==========

M. R. Yeadon, 1990. The Simulation of Aerial Movement-ii. Mathematical Inertia
Model of the Human Body. Journal of Biomechanics, 23:67-74.
