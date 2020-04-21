#!/usr/bin/env python

import contextlib
from distutils.version import StrictVersion

import numpy as np
import numpy.core.arrayprint as arrayprint


@contextlib.contextmanager
def printoptions(strip_zeros=False, **kwargs):
    """Allows you to set NumPy array print formatting locally.
    Taken from:
    http://stackoverflow.com/questions/2891790/pretty-printing-of-numpy-array
    """
    if StrictVersion(np.__version__) >= StrictVersion('1.18.0'):
        origcall = arrayprint.FloatingFormat.__call__
    else:
        origcall = arrayprint.FloatFormat.__call__

    def __call__(self, x, strip_zeros=strip_zeros):
        return origcall.__call__(self, x, strip_zeros)

    if StrictVersion(np.__version__) >= StrictVersion('1.18.0'):
        arrayprint.FloatingFormat.__call__ = __call__
    else:
        arrayprint.FloatFormat.__call__ = __call__

    original = np.get_printoptions()
    np.set_printoptions(**kwargs)
    yield
    np.set_printoptions(**original)

    if StrictVersion(np.__version__) >= StrictVersion('1.18.0'):
        arrayprint.FloatingFormat.__call__ = origcall
    else:
        arrayprint.FloatFormat.__call__ = origcall
