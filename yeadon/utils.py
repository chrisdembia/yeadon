#!/usr/bin/env python

import contextlib

import numpy as np
import numpy.core.arrayprint as arrayprint


@contextlib.contextmanager
def printoptions(strip_zeros=False, **kwargs):
    """Allows you to set NumPy array print formatting locally.

    Taken from:

    http://stackoverflow.com/questions/2891790/pretty-printing-of-numpy-array

    """

    origcall = arrayprint.FloatFormat.__call__

    def __call__(self, x, strip_zeros=strip_zeros):
        return origcall.__call__(self, x, strip_zeros)

    arrayprint.FloatFormat.__call__ = __call__
    original = np.get_printoptions()
    np.set_printoptions(**kwargs)
    yield
    np.set_printoptions(**original)
    arrayprint.FloatFormat.__call__ = origcall
