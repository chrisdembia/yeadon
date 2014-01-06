Release Notes
=============

Future releases
---------------
See issues on github at `<https://github.com/chrisdembia/yeadon/issues>`_

v1.1
----

 - Fixed somersault mispelling, issue #67.
 - Now, configuration variables indicate proper sense. For example, flexion
   means flexion; not extension.
 - Fixed serious bug in the computation of inertia tensors in different
   reference frames. The calculation of all solids' and segments' inertia
   tensors in the global frame was incorrect, PRs #79, #80.
 - Now, use a consistent definition for rotation matrices: now, all rotation
   matrices ``R`` are of the form ``v_a = R * v_b``, PR #88.
 - Added a center of mass sphere to the GUI visualization, PR #95.
 - Made mass center sphere and inertia ellipsoid off by default in the GUI, PR
   #93.
 - Fixed default orientation of human in GUI visualization, PR #93.
 - Improved the printing of human, segement, and solid properties, PR #81.
 - Renamed ``rotate3_inertia`` to ``rotate_inertia`` and changed its definition
   to match the rotation matrix definitions in the rest of the software, PR
   #79.
 - Setuptools now recommended, PR #72.
 - ``yeadon.__version__`` now works, PR #69.
 - Fixed Sphinx warnings in the docs.

v1.0
----
 - Fairly thorough unit tests.
 - Clarified documentation and docstrings.
 - Improved the way rotation matrices are formed.
 - Moved visualization to the MayaVi library, and introduced a GUI.
 - Introduced the :py:meth:`yeadon.human.Human.inertia_transformed` method.
 - Use of python properties for inertia properties and other important
   attributes.
 - Improved setup/build/installation process.

v0.8 on 18 July 2011
--------------------
This is the first release.
