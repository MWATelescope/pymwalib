#!/usr/bin/env python
#
# timestep: class representing a single timestep in mwalib
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Adapted from:
# http://jakegoulding.com/rust-ffi-omnibus/objects/
#
# Additional documentation:
# https://docs.python.org/3.8/library/ctypes.html#module-ctypes
#


class TimeStep:
    """
    A class representing a single mwalibTimeStep

    Attributes
    ----------
    index : int
        Ordinal index of this time step.

    unix_time_ms : int
        The UNIX time (in milliseconds) of the start of this time step

    """

    def __init__(self,
                 index: int,
                 unix_time_ms: int):
        """Initialise the class"""
        self.index: int = index
        self.unix_time_ms: int = unix_time_ms

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Order: {self.index}, " \
               f"UNIX time: {float(self.unix_time_ms) / 1000.})"
