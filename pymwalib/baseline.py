#!/usr/bin/env python
#
# baseline: class representing a single baseline in mwalib
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


class Baseline:
    """
    A class representing a single mwalibBaseline

    Attributes
    ----------
    index : int
        Ordinal index of this time step.

    antenna_index1 : int
        The index in the antenna array for the first member of the baseline

    antenna_index2 : int
        The index in the antenna array for the second member of the baseline

    """

    def __init__(self,
                 index: int,
                 antenna1_index: int,
                 antenna2_index: int):
        """Initialise the class"""
        self.index: int = index
        self.antenna1_index: int = antenna1_index
        self.antenna2_index: int = antenna2_index

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Order: {self.index}, " \
               f"Antennas: {self.antenna1_index} v {self.antenna2_index})"
