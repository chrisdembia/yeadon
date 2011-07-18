Measurements
============

There are 95 measurements to make.

*Stadiums* can be defined by either
 * a radius :math:'r'and thickness :math:'t',
 * a perimeter :math:'p'and width :math:'w'along the stadium's longitudinal axis
 * a perimeter :math:'p'and a depth :math:'d = 2r'.
 * a depth :math:'d' and a width :math:'w'.

.. image:: stadium.png
   :scale: 15 %
A circle can be defined by a stadium solid whose thickness is zero, :math:'t = 0'.

*Stadium solids* are defined by two stadiums, as well as the height :math:'h'of the solid between the two stadiums.

To define the stadium solids that compose the human model, one can take the measurements outlined here. The measurements consist of *lengths* :math:'L'(not heights), perimeters :math:'p', heights :math:'h', and depths :math:'d'.

Exceptions
----------
To actually measure someone, perhaps the easiest thing to do is to print a copy of the meastemplate.txt file EDIT.

Length exceptions: Lengths to arm level 1 and leg levels 2 and 7 are not measured. The length from La0 to La1 (or Lb0 to Lb2) is set as half the length from La0 to La2 (or Lb0 to Lb2). The lengths to leg levels 2 and 7 are calculated as averages of the two length around leg levels 2 and 7.

Levels that are circles (degenerate stadiums): Arm levels 0-3 (the first four arm levels) and leg levels 0-5 and 7 (the first six and the arch). For these, only a perimeter measurement is required (no width or depth is measured).

Depth measurements:

The base of the neck, which is also located at level Ls5, acromion, is modeled as circular, with the radius of the stadium at Ls5.

Mass correction:

It is possible to "correct" the mass of the model by inputting an actual measured mass of the human. This will cause all the densities (and thus all the masses) to be scaled by the actual total mass. This is done by setting a value for "totalmass" in the measurement input text file. The variable can be omitted from the text file though, or alternatively can have a non-positive value.

    yeadonmeas.pdf
