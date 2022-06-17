#!/usr/bin/env python

import contextlib

import numpy as np
import numpy.core.arrayprint as arrayprint


@contextlib.contextmanager
def printoptions(**kwargs):
    """Allows you to set NumPy array print formatting locally.

    Taken from:

    http://stackoverflow.com/questions/2891790/pretty-printing-of-numpy-array

    """

    original = np.get_printoptions()
    np.set_printoptions(**kwargs)
    yield
    np.set_printoptions(**original)
