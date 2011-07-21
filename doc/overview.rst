Overview
========

This page describes the basics of Yeadon's inertia model. It is expected that
the user of this package has read Yeadon's 1990 papers, especially Yeadon
1990-ii [1]. There are four related papers, identified by numerals i-iv.

A summary of the content of his four papers is provided:

- i: motivation, conceptual description of joints, obtaining orientation angles
  from film
- ii: modeling human geometry using stadium solids
- iii: inertia transforms and angular momentum of the stadium solids
- iv: joint description

The measurements page in this documentation describes the particularly relevant
parts of paper ii, while the configuration page does the same for paper iv.

Yeadon models a human using 39 stadium solids, and 1 semi-ellipsoid for the
cranium. The relatively simple geometry allows for one to develop important
dynamics/mechanics/inertia quantities. These quantities are mass, center of
mass positions, and inertia tensors. These quantities can be queried in the
reference frame of the entire human, or in the local reference frame of a
segment or a solid. More details about how to use the package are provided on
the usage page.

One can use this package to incorporate a human into dynamics equations, though
this endeavor is left up to the user. The package does not deal at all with
angular momentum (the topic of paper iii).

There are a few key differences between Yeadon's model and this model.

- In Yeadon's model, the fixed coordinate axes of the human are defined in a
  complicated way, such that the fixed axes are not fixed to any one body
  segment. In this package, the fixed coordinate system is "fixed" to the
  pelvis segment.
- In Yeadon's model, the orientation of both legs are tied to each other, so
  that there are less degrees of freedom than there are joint angles. No joint
  angles are coupled in this package.
- Yeadon provides the option of formulating the model with additional joints
  for the feet and hands. In this version of ``yeadon``, the feet and hands are
  not separated segments
- Yeadon indexes his solid names from 1 (s1 is the first solid), while this
  package indexes solids from 0 (s0 is the first solid). The names of the limbs
  (e.g. A1, J1, etc.) are unchanged.

[1] Yeadon, M. R. (1990c). The Simulation of Aerial Movement-ii. A Mathematical
Model of the Human Body. Journal of Biomechanics, 23:67-74.
