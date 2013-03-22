.. _usage:

=====
Usage
=====

This page shows how one can use :mod:`yeadon` once it's installed.

Three different interfaces
==========================

There are three ways of using the yeadon module: through the text based user
interface (UI), through a GUI, and through the API. The UI can be run by
entering the following in a terminal or command window::

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

where ``<measfilename>`` and ``<CFGfilename>`` are either paths to input .txt
files, or dictionaries. The ``<CFGfilename>`` argument is optional. If not
provided, the human is created in a default configuration. See
:ref:`measurements` or :ref:`configuration` for more detail.  With an instance
of :class:`Human`, we can access inertia properties of the entire human, of
its segments (e.g. limbs), or of the individual solids that make up the
segments.


Suppose we have an instance of :class:`Human`, named ``chad``. Here is a
summary of what we can do with it. Before we show what one can do with a
:class:`Human`, we present the attributes that represent the human's segments.
There is an attribute for each segment, whose name is that as the label given
to it by Yeadon.

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

Also, one can access a list of all segments, perhaps for iteration, via the
``chad.segments`` attribute. The solids that make up each segment can be
accessed through the :py:class:`Segment` attributes via the ``solids``
attribute, which is a list::

    >>> chad.P.solids[0].label
    's0: hip joint centre'


Summary of functionality
========================

**Print inertia properties**
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

**Return inertia properties**
    It may be desirable to directly access the inertia properties from the
    attributes as below:

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
    - ``H.draw_mayavi()``: MayaVi. This works a little faster than matplotlib.

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
