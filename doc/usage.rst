=====
Usage
=====

This page tells how to use yeadon, and lists the methods that a user would use
(the methods that would remain public if any functions were made private).

There are two suggested ways of using the yeadon module. The first is the
command line interface. This can be run by entering a python command prompt and
entering

::

    import yeadon
    yeadon.start_ui()

The interface will guide you through its use. You can enter in
measurements, then configuration (joint angles), and then can modify joint
angles, access data, or use one of the "features" listed below.

The other way is to create a human object and just access the "features" by
executing methods.

::

    import yeadon
    H = yeadon.human(<meas>,<cfg>)

Where ``<meas>`` and ``<cfg>`` are either paths to input .txt files, or
dictionaries. The ``<cfg>`` argument is optional. The constructor for the human
object will perform the calculation of the inertia properties of all segments
and solids of the human.

The user does not interact directly with any of the modules aside from
``human`` and ``ui``.

Features
========

**Print inertia properties**
    There are methods to print the properties of the entire human, of segments,
    or of solids. These are:

    - ``H.print_properties()``
    - ``H.J1.print_properties()``
    - ``H.J1.print_solid_properties()``

    where J1 is just an example of a segment. These commands print the
    information to the python command window or a terminal.

**Return inertia properties**
    It may be desirable to directly access the data from the attributes as
    below:

    - ``H.Mass``
    - ``H.COM``
    - ``H.Inertia``
    - ``H.J1.Mass``
    - ``H.J1.relCOM`` (in the local coordinates of the J1 segment)
    - ``H.J1.pos`` (in fixed human coordinates; position of the "root" of a
      segment)
    - ``H.J1.COM``
    - ``H.J1.endpos`` (in fixed human coordinates; position of "tip" of a
      segment)
    - ``H.J1.relInertia`` (in the local coordinates of the J1 segment)
    - ``H.J1.Inertia``
    - ``H.j[0].Mass``
    - ``H.j[0].relCOM``
    - ``H.j[0].pos``
    - ``H.j[0].COM``
    - ``H.j[0].endpos``
    - ``H.j[0].relInertia``
    - ``H.j[0].Inertia``

    See below for a full list of all segment objects and solid objects.

**Draw**
    There are three methods for drawing the human.

    - ``H.draw()``: matplotlib, 3D. This was the first method implemented, and
      does not look too great because matplotlib does not manage depth of the
      objects.
    - ``H.draw2D()``: matplotlib, 2D. Not implemented well currently, pretty
      much unusable.
    - ``H.draw_visual()``: python-visual. This works pretty well. Requires the
      VPython (python-visual) package.

**Combine inertia**
    Provides the mass, center of mass, and inertia tensor for a combination of
    solids and/or segments. This can be done from the method
    ``yeadon.human.combine_inertia``. See the help for the method to to use it.

**Scale by mass**
    Set the mass of the human to be a measured mass by scaling the densities
    that the code uses. This is done by providing a positive value for
    ``totalmass`` in the measurement text input file.

**Symmetry**
    The measurements for the left and right limbs are averaged to create
    symmetrical limbs. This may be desirable depending on a user's use of the
    package. By default, this average is set to occur, It can be turned off for
    a human by using a third input to the human constructor of ``False``.

**File Input/Output**
    The measurements can be written to a txt file using
    ``yeadon.human.write_measurements``. The configuration can be written using
    ``yeadon.human.write_CFG``. The measurements can be converted and written
    to a text file that is ready for Yeadon's ISEG fortran code that performs
    many of the same calculations as this packge by using
    ``yeadon.human.write_meas_for_ISEG``.

The human segment attributes
----------------------------

 - ``human.P`` pelvis
 - ``human.T`` thorax
 - ``human.C`` chest-head
 - ``human.A1`` left upper arm
 - ``human.A2`` left forearm-hand
 - ``human.B1`` right upper arm
 - ``human.B2`` right forearm-hand
 - ``human.J1`` left thigh
 - ``human.J2`` left shank-foot
 - ``human.K1`` right thigh
 - ``human.K2`` right shank-foot

The human solids can be access from the segments or from the human.
-------------------------------------------------------------------

 - ``human.s[0] - human.s[7]`` for the torso
 - ``human.a[0] - human.a[6]`` for the left arm
 - ``human.b[0] - human.b[6]`` for the right arm
 - ``human.j[0] - human.j[8]`` for the left leg
 - ``human.k[0] - human.k[8]`` for the right leg
 - ``human.P.solids[0] - human.P.solids[1]`` for the pelvis solids
 - ``human.T.solids[0]`` for the thorax solid
 - ``human.C.solids[0] - human.C.solids[4]`` for the chest-head
 - ``human.A1.solids[0] - human.A1.solids[1]`` for the left upper arm
 - ``human.A2.solids[0] - human.A2.solids[4]`` for the left forearm-hand
 - ditto for the right arm
 - ``human.J1.solids[0] - human.J1.solids[3]`` for the left thigh
 - ``human.J1.solids[0] - human.J2.solids[5]`` for the left shank-foot
 - ditto for the right leg
