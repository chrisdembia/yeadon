Release Notes
=============

Future releases
---------------
See issues on github at `<https://github.com/chrisdembia/yeadon/issues>`_.

v2.0.0
------

- Support Python 3.10 to 3.14, drop support for < 3.10.
- Removed all existing deprecation warnings; breaks some old API!
- Added method to Human for loading configurations from file.
- Added ability to load configuration files in the GUI.
- Added ability to toggle symmetry when loading measurement files in the GUI.
- Fixed decimal length display issues in the GUI.
- Now includes a pyproject.toml file for pip aligned installations.
- Dropped support for using setup.py directly.
- Dropped support for nose (for unit tests).
- Bumped minimum dependency versions to align with Ubuntu 24.04 LTS.

v1.5.0
------

- Supports Python >= 3.8.
- Made tests compatible with pytest.
- Uses entry_points for the CLI script and move the entry point into the
  package.
- Eliminated numpy.matrix/mat. Now only returns numpy.array.
- Bumped min dependencies to those in Ubuntu 22.04.

v1.4.0
------

- Dropped support for Python < 3.7 (including 2.7).
- Replaced ``yaml.load`` with ``yaml.safe_load``.
- Fixed pretty printing of results to work with newer NumPy versions.

v1.3.0
------

- Now supports Python 3.

v1.2.1
------

- Pinned the bicycle example to specific dependencies.
- Added version.py.
- Removed Mayavi print statements.
- Added badges to the README.
- Added citation note to the README.

v1.2
----

 - Added two examples, PRs #98, #101.

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
