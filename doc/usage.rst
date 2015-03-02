.. _usage:

=====
Usage
=====

This page shows how one can use :mod:`yeadon` once it's installed.

Three different interfaces
==========================

There are three ways of using the :mod:`yeadon` package: through the text-based
user interface (UI), through the graphical user interafce (GUI), and through a
Python interpreter or in your own Python code. The can run the UI by entering
the following in a terminal or command window::

   $ yeadon --ui

or by entering a Python interpreter and executing the following::

    import yeadon
    yeadon.start_ui()

The interface will guide you through its use. You can enter in
measurements, then configuration (joint angles), and then can modify joint
angles, access data, or use one of the features listed below.

The GUI is run by entering the following in a terminal or command window::

    $ yeadon --gui

or by entering a Python interpreter and executing the following::

    >>> yeadon.start_gui()

The last way is through the API in a Python script or module. You import the
module and then create a :class:`Human`::

    >>> import yeadon
    >>> human = yeadon.Human(<measfilename>, <CFGfilename>)

where ``<measfilename>`` and ``<CFGfilename>`` are either paths to .txt
files, or are dictionaries. The ``<CFGfilename>`` argument is optional. If not
provided, the human is created in a default configuration. See
:ref:`measurements` or :ref:`configuration` for more detail.  With an instance
of :class:`Human`, we can access inertia properties of the entire human, of
its segments (e.g. limbs), or of the individual solids that make up the
segments.

Attributes of :class:`Human`
============================

Suppose we have an instance of :class:`Human`, named ``chad``. Before we show
what one can do with a :py:class:`Human`, we present the attributes that
represent the human's segments.  There is an attribute for each segment, whose
name is the same as that used by Yeadon.

 - ``chad.P`` pelvis
 - ``chad.T`` thorax
 - ``chad.C`` chest-head
 - ``chad.A1`` left upper arm
 - ``chad.A2`` left forearm-hand
 - ``chad.B1`` right upper arm
 - ``chad.B2`` right forearm-hand
 - ``chad.J1`` left thigh
 - ``chad.J2`` left shank-foot
 - ``chad.K1`` right thigh
 - ``chad.K2`` right shank-foot

Also, one can access a list of all these segments, perhaps for iteration, via
the ``chad.segments`` attribute. The solids that make up each segment can be
accessed through the ``solids`` attribute of each of the ``Segments``'s above::

    >>> chad.P.solids[0].label
    's0: hip joint centre'

Setting the configuration
=========================

One can set the configuration of the model using a ``<CFGfilename>`` as
described above, or by using the ``chad.set_CFG()`` method::

    >>> chad.set_CFG('somersault', 0.5 * 3.1416)

When one calls this method, the inertia properties are recomputed. The list of
configuration variables is stored in ``Human.CFGnames``.

Summary of functionality
========================

Print inertia properties
------------------------
This is the quickest way to get the relevant information out of the model.
There are methods to print the properties of the entire human, of segments,
or of solids. The following prints the inertia properties for the entire
human::

    >>> chad.print_properties()
    Mass (kg): 58.2004885884

    COM in global frame from bottom center of pelvis (Ls0) (m):
    [[  1.62144613e-17]
    [  0.00000000e+00]
    [  1.19967938e-02]]

    Inertia tensor in global frame about human's COM (kg-m^2):
    [[  9.63093850e+00   2.20795600e-20   6.10622664e-16]
    [  2.20795600e-20   9.99497872e+00   2.70396625e-36]
    [  6.10622664e-16   2.70396625e-36   5.45117742e-01]]

The following shows how one can print the inertia properties for the
``J1``, or left thigh, segment::

    >>> chad.J1.print_properties()
    J1: Left thigh properties:

    Mass (kg): 8.50477532204

    COM in segment's frame from segment's origin (m):
    [[ 0.        ]
    [ 0.        ]
    [ 0.19276748]]

    COM in global frame from bottom center of pelvis (Ls0) (m):
    [[ 0.081     ]
    [ 0.        ]
    [-0.19276748]]

    Inertia tensor in segment's frame about segment's COM (kg-m^2):
    [[ 0.14109999  0.          0.        ]
    [ 0.          0.14109999  0.        ]
    [ 0.          0.          0.02718329]]

    Inertia tensor in global frame about segment's COM (kg-m^2):
    [[  1.41099994e-01   0.00000000e+00   1.39507727e-17]
    [  0.00000000e+00   1.41099994e-01   0.00000000e+00]
    [  1.39507727e-17   0.00000000e+00   2.71832899e-02]]

Lastly, there is a method for each segment that prints the inertia
properties of the individual solids that make up the segment (output not
shown)::

    >>> chad.J1.print_solid_properties()

Below, we delve into more detail about what these quantities are.

Return inertia properties
-------------------------
It may be desirable to directly access the kinematics information and
inertia properties from the attributes. Below, we show the
docstrings for these properties, as can be accessed in an `IPython
<ipython.org>`_ interpreter. Also, one can obtain iinformation about the data
type of the properties using ``help(<property>)`` (e.g.,
``help(chad.mass)``). The docstrings make reference to *the bottom center of the
pelvis (Ls0)*, the  *origin of the segment/solid*; and the *global* and
*segment* frames. These locations and frames are descrbed in
:ref:`configuration`.

There are three inertia properties for the human overall::

    >>> chad.mass?
    ...Docstring:  Mass of the human, in units of kg....

    >>> chad.center_of_mass?
    ...Docstring: Center of mass of the human, a np.ndarray, in units of m,
    expressed the global frame, from the bottom center of the pelvis
    (center of the Ls0 stadium)....

    >>> chad.inertia?
    ...Docstring: Inertia matrix/dyadic of the human, a np.matrix, in units
    of kg-m^2, about the center of mass of the human, expressed in the
    global frame....

For each segment, there are five properties that are related to inertia,
and three related strictly to kinematics::

    >>> chad.J1.mass?
    ...Docstring:  Mass of the segment, in units of kg....

    >>> chad.J1.rel_center_of_mass?
    ...Docstring: Center of mass of the segment, a np.ndarray, in units of
    m, expressed in the frame of the segment, from the origin of the
    segment....

    >>> chad.J1.center_of_mass?
    ...Docstring: Center of mass of the segment, a np.ndarray, in units of
    m, expressed in the global frame, from the bottom center of the
    pelvis....

    >>> chad.J1.rel_inertia?
    ...Docstring: Inertia matrix/dyadic of the segment, a np.matrix, in
    units of kg-m^2, about the center of mass of the segment, expressed in
    the frame of the segment....

    >>> chad.J1.inertia?
    ...Docstring: Inertia matrix/dyadic of the segment, a np.matrix, in
    units of kg-m^2, about the center of mass of the human, expressed in
    the global frame....

    >>> chad.J1.pos?
    ...Docstring: Position of the origin of the segment, a np.ndarray, in
    units of m, expressed in the global frame, from the bottom center of
    the pelvis (Ls0)....

    >>> chad.J1.end_pos?
    ...Docstring: Position of the center of the last (farthest from pelvis)
    stadium in this segment, a np.ndarray, in units of m, expressed in the
    global frame, from the bottom center of the pelvis (Ls0)....

    >>> chad.J1.rot_mat?
    ...Docstring: Rotation matrix specifying the orientation of this
    segment relative to the orientation of the global frame, a np.matrix,
    unitless.  Multiplying a vector expressed in this segment's frame with
    this rotation matrix on the left gives that same vector, but expressed
    in the global frame....

The attributes for the solids are similar to those for the segments, except
that they do not have a ``rot_mat`` attribute (their ``rot_mat`` is that of
the segment containing them)::

    >>> chad.J1.solids[0].mass?
    ...Docstring: Mass of the solid, in units of kg....

    >>> chad.J1.solids[0].center_of_mass?
    ...Docstring: Center of mass of the solid, a np.ndarray, in units of m,
    expressed in the global frame, from the bottom center of the pelvis
    (Ls0)....

    >>> chad.J1.solids[0].inertia?
    ...Docstring: Inertia matrix/dyadic of the solid, a np.matrix, in units
    of kg-m^2, about the center of mass of the human, expressed in the
    global frame....

    >>> chad.J1.solids[0].rel_center_of_mass?
    ...Docstring: Center of mass of the solid, a np.ndarray, in units of m,
    expressed in the frame of the solid, from the origin of the solid....

    >>> chad.J1.solids[0].rel_inertia?
    ...Docstring: Inertia matrix/dyadic of the solid, a np.matrix, in units
    of kg-m^2, about the center of mass of the solid, expressed in the
    frame of the solid....

    >>> chad.J1.solids[0].pos?
    ...Docstring: Position of the origin of the solid, which is the center
    of the surface closest to the pelvis, a np.ndarray, in units of m,
    expressed in the global frame, from the bottom center of the pelvis
    (Ls0)....

    >>> chad.J1.solids[0].end_pos?
    ...Docstring: Position of the point on the solid farthest from the
    origin along the longitudinal axis of the segment, a np.ndarray, in
    units of m, expressed in the global frame, from the bottom center of
    the pelvis (Ls0)....

Draw
----
One can create a window with a 3D rendering of the human model. The
rendering portrays the human with the given measurements and specified
configuration::

    >>> chad.draw()

Scale by mass
-------------
The mass of the human that we calculate probably doesn't match that of the
actual human subject being modeled. We calculate this mass using densities from
literature. If you measure the human's actual mass and want to use that in
`yeadon`, we can change the model's mass to this measured mass by scaling these
densities. This can be done via the measurement input file by providing a
positive value for ``totalmass`` (see measurement file template) or by a call
to the ``chad.scale_human_by_mass()`` method.

Symmetry
--------
One can average the measurements for the left and right limbs to create
symmetrical limbs. This may be desirable depending on your use of the package.
This symmetry is imposed by default. It can be changed by setting the keyword
argument ``symmetric`` of the ``Human`` constructor to ``False``. The symmetry
of the model cannot be modified after the ``Human`` is constructed.

Combine inertia
---------------
One can obtain inertia properties for a combination of solids and/or segments.
This is done via the ``chad.combine_inertia()`` method. See :ref:`apidoc` for
more information.

Transform inertia tensor
------------------------
By default, the inertia tensor of the human is expressed in the global frame,
whose origin is located at the bottom center of the pelvis (Ls0), and whose
orientation is shown in :ref:`configuration`, ``draw()`` and the GUI. To
transform the inertia tensor so it's expressed in a different frame, you can
use ``chad.inertia_transformed()``.

File input/output
-----------------
The measurements can be written to a text file using
``chad.write_measurements()``. The configuration can be written using
``chad.write_CFG()``. The measurements can be written to a text file that is
ready for Yeadon's ISEG Fortran code using ``chad.write_meas_for_ISEG()``.
