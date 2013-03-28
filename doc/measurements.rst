.. _measurements:

Measurements
============

This document describes the measurements that need to be taken, and provides
some guidance for taking those measurements and getting them into the code.

The stadium shape and the stadium solid
---------------------------------------

The human is composed of 11 rigid-body segments. Each segment is defined as a
loft across a number of stadium shapes, which are defined below. In one case, a
segment contains a semi-ellipsoid. The model is customized to an individual via
95 anthropomorphic measurements to define the stadia and the distances between
them.

A *stadium* shape, show in the figure below, can be defined via any of the 4
following sets of 2 parameters:

 - a radius :math:`r` and thickness :math:`t`,
 - a perimeter :math:`p` and width :math:`w` along the stadium's longitudinal
   axis
 - a perimeter :math:`p` and a depth :math:`d = 2r`.
 - a depth :math:`d` and a width :math:`w`.

.. image:: stadium.png
   :scale: 15 %

A circle can be defined by a stadium whose thickness is zero, :math:`t = 0`.

*Stadium solids* are defined by two stadia, as well as the height :math:`h` of
the solid between the two stadia (i.e., a loft between the two stadium cross
sections).

Specification of all measurements
---------------------------------

The figure below specifies all 95 measurements

To define the stadium solids that make up the human model, one can take the
measurements outlined here. The measurements consist of *lengths* :math:`L`
(not heights), perimeters :math:`p`, heights :math:`h`, widths :math:`w`, and
depths :math:`d`.

By measuring the parameters that define the stadia, or *levels*, and the
distance between these stadia, we define 39 stadium solids. Each stadium is
shared by two stadium solids, except for the stadia at the end of the hands and
feet. In general, the stadia are defined by measuring perimeter and width,
since these are easier to physically measure.  There are a few exceptions
though, and these are described further down the page.

.. image:: cld72_yeadon_meas_0716.png

It is lengths, not heights, that you measure off the subjects. That is to say
that the length inputs are cumulative length measurements, not the heights of
each individual stadium solid. For example, The "length" of the Ls5 acromion
level is measured from Ls0, the hip joint centre, not from Ls4. The figure
above lists the level from which the length to other levels are measured.

Scaling densities via a measured mass
-------------------------------------
The mass of the model is estimated from the measurements described above, along
with densities for the various segments taken from the literature. In the case
that you also measure the mass of the individual being modeled, it is possible
to scale the densities so that the total mass of the human is that which you
have measured. See :ref:`usage` for a brief explanation on how to do this.

Getting measurements into the model
-----------------------------------
There are two options for getting measurements into the model:

 - Use the `meastemplate.txt` input text file in the misc/ directory, or
   :download:`here <../misc/meastemplate.txt>` to define all measurements. The
   file uses the `YAML`_ syntax. This syntax allows you  to treat the input
   file as a Python script in which you simply define a number of variables.
   See comments within the file for further details.
 - Provide a python dictionary containing all the appropriate
   fields to the :py:class:`yeadon.human.Human` constructor. You can obtain a
   sample dictionary from the variable :py:attr:`yeadon.human.Human.meas`. The
   keys for the dictionary are the names of the variables in the
   `meastemplate.txt` file, as strings.

Internally, the package uses units of meters for the measurements. However, it
may be that you have worked with different units. In the case that you are using `meastemplate.txt`, you can define the measurements using the units you
desire, and the package will perform the unit conversion for you. This is done
by providing a value for the variable ``measurementconversionfactor`` in
`meastemplate.txt`. This is a number that converts the units of your
measurements into meters. For example, if you took measurements in millimeters,
you should give this variable the value 0.001. If you are inputting using a
dictionary, the measurements must be in units of meters.

Exceptions
----------
The exceptions to the general measurement practice (lengths, perimeters, and
widths) are explained here.

 - **Length exceptions**: Lengths to arm level 1 and leg levels 2 and 7 are not
   measured. The length from La0 to La1 (or Lb0 to Lb2) is set programmatically
   as half the length from La0 to La2 (or Lb0 to Lb2). The lengths to leg
   levels 2 and 7 are calculated as averages of the two lengths around leg
   levels 2 and 7.  Thus, perimeters, etc. at these levels should be measured
   halfway between the surrounding levels (i.e., perimeter of the La1 stadium
   is measured at the point in in the arm halfway between La0 and La2).
 - **Levels that are circles** (zero-thickness stadia): Arm levels 0-3 (the first
   four arm levels) and leg levels 0-5 and 7 (the first six and the arch). For
   these, only a perimeter measurement is required (no width or depth is
   measured).
 - **Depth measurements**: As far as measurements are concerned, the only
   difference between a depth and a width is that a depth is measured anterior
   to posterior (front to back), while widths are measured medio-laterally
   (side to side). Depths are measured at the Ls5 acromion, and the Lj6, Lk6
   heel.
 - **The neck**: The base of the neck, which is also located at level Ls5,
   acromion, is modeled as circular. Its radius is set programmatically from
   the acromion perimeter measurement. This means that the acromion perimeter
   should be measured about the base of the neck.

Sample measurement files
------------------------
Here are measurement data files for three people we measured:
 - :download:`male1 <../misc/samplemeasurements/male1.txt>`
 - :download:`male2 <../misc/samplemeasurements/male2.txt>`
 - :download:`male3 <../misc/samplemeasurements/male3.txt>`
 - :download:`female1 <../misc/samplemeasurements/female1.txt>`

.. _YAML: http://www.yaml.org/
