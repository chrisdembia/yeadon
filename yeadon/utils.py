#!/usr/bin/env python

import contextlib

import numpy as np


@contextlib.contextmanager
def printoptions(*args, strip_zeros=False, **kwargs):
    """Allows you to set NumPy array print formatting locally.

    Taken from:

    http://stackoverflow.com/questions/2891790/pretty-printing-of-numpy-array

    """
    original = np.get_printoptions()
    np.set_printoptions(*args, strip_zeros=strip_zeros, **kwargs)
    try:
        yield
    finally:
        np.set_printoptions(**original)
