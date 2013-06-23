.. yeadon documentation master file, created by
   sphinx-quickstart on Thu Jun 30 16:11:26 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ``yeadon``'s documentation!
======================================

This package calculates the masses, center of mass positions, and inertia
tensors that correspond to the human inertia model developed by Yeadon [1]. The
package allows for the input of both measurements from
human subjects and configuration variables (joint angles) with which one can
orient the model. Additionally, the package allows for 3D visualization of the
model using the package.

One possible use of the package is to incorporate the inertial properties of an
actual human into a rigid body dynamics model that contains a human. Then, the
model containing the human can be compared to experiments performed with the
same human.

This package was developed during the Summer of 2011 at the University of
California, Davis, to aid with the bicycle research of Jason Moore and Dale
Luke Peterson in the Sports Biomechanics Lab of Professor Mont Hubbard. Jason
Moore had a multibody dynamics model of a human riding a bicycle, and performed
experiments with humans riding a bicycle. To compare his model to his
experiments, he needed the inertial properties of the human riding the bicycle.
That's what this package was able to provide him [2]. Learn more about the
Sports Biomechanics Lab at `biosport.ucdavis.edu
<http://biosport.ucdavis.edu>`_.

Here is a video that introduces the basics of this package:
`<http://youtu.be/o-5Ss6YLY0I>`_.

Contents
========

.. toctree::
   :maxdepth: 1

   overview.rst
   usage.rst
   measurements.rst
   configuration.rst
   releasenotes.rst
   apidoc.rst

Installation
============

The README.rst file in the source distribution of this packge contains
installation instructions.

Website navigation
==================

* :ref:`genindex`
* :ref:`modindex`

References
==========

[1] M. R. Yeadon, 1990. The Simulation of Aerial Movement-ii. Mathematical
Inertia Model of the Human Body. Journal of Biomechanics, 23:67-74.

[2] `J. Moore, 2012. Human Control of a Bicycle. University of California,
Davis.
<http://moorepants.github.io/dissertation/physicalparameters.html#human-parameters>`_
