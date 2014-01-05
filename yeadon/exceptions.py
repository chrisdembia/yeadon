#!/usr/bin/env python


class YeadonDeprecationWarning(DeprecationWarning):
    """Simple wrapper so that our deprecation warnings are shown to the
    user. By default, DeprecationWarning's are not printed."""
    pass
