Overview
========

This page describes the basics of Yeadon's inertia model. It is expected that
the user of this package has read Yeadon's 1990 papers, especially Yeadon
1990-ii. There are four related papers, identified by numerals i-iv.

Here is a summary of his four papers:

- i: motivation, conceptual description of joints, obtaining orientation angles
  from film
- ii: modeling human geometry using stadium solids
- iii: inertia transforms and angular momentum of the stadium solids
- iv: simulation verification

The :ref:`measurements` page in this documentation describes the particularly
relevant parts of paper ii, while the :ref:`configuration` page does the same
for paper iv.

Yeadon models a human using 39 stadium solids and 1 semi-ellipsoid (for the
head). These 40 solids make up 11 rigid body segments, which are connected to
each other via joints (e.g., the knee). This relatively simple geometry allows
for one to swiftly calculate quantities relevant for dynamics. These quantities
are mass, center of mass positions, and inertia tensors. These quantities can
be obtained in the global reference frame, or in the local frame of a segment
or solid.

One can use this package to incorporate a human into equations of motion,
though this endeavor is left to the user. The package does not deal at all
with angular momentum (the topic of paper iii).

There are a few differences between Yeadon's model described in his
publications and the model implemented in this package. Here are some of the
bigger ones:

- In Yeadon's model, the global frame of the human is defined in a complicated
  way that depends on the configuration of the human.  In this package, the
  global frame does not depend on the configuration.
- In Yeadon's model, the orientation of the legs are related to each other, so
  that there are less degrees of freedom than there are joint angles
  (generalized coordinates). No joint angles are coupled in this package.
- Yeadon provides the option of formulating the model with additional joints
  for the feet and hands. Here, the feet and hands are rigid parts of the legs
  and forearms, respectively.
- Yeadon labels the *solids* with indices starting from 1 (s1 is the first
  solid), while this package indexes the solids from 0 (s0 is the first solid).
  The labels for the *segments* (e.g. A1, J1, etc.) are unchanged.
- Both packages allow making the model symmetric (averaging both the two arms
  and the two legs), but do so in different ways.  We average the input
  measurements for the limbs, and then proceed to compute masses, center of
  mass positions, and inertia tensors with these averaged measurements. Yeadon,
  however, enforces symmetry by averaging these three quantities as the last
  step (the measurements across limbs are not averaged).
