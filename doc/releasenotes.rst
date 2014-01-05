Release Notes
=============

Future releases
---------------
See issues on github at `<https://github.com/chrisdembia/yeadon/issues>`_

v1.1
----

 - Fixed somersault mispelling, issue #67.
 - Configuration variables indicate proper sense. For example, flexion means
   flexion; not extension.
 - Fix serious bug in the computation of inertia tensors in different reference
   frames. The calculation of all solids' and segments' inertia
   tensors in the global frame was incorrect.
 - Use a consistent definition for rotation matrices: now, all rotation
   matrices `R` are of the form `v_a = R * v_b`.

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
