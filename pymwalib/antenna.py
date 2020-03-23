#!/usr/bin/env python
#
# antenna: class representing a single antenna in mwalib
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
from pymwalib.rfinput import RFInput


class Antenna:
    """
    A class representing a single mwalibAntenna

    Attributes
    ----------
    index : int
        Ordinal index of this RF Input.

    Please see https://github.com/MWATelescope/mwalib/blob/master/src/antenna.rs for remaining attributes

    """

    def __init__(self,
                 index: int,
                 antenna: int,
                 tile_id: int,
                 tile_name: str,
                 rf_input_x: RFInput,
                 rf_input_y: RFInput):
        """Initialise the class"""
        self.index: int = index
        self.antenna: int = antenna
        self.tile_id: int = tile_id
        self.tile_name: str = tile_name
        self.rf_input_x: RFInput = rf_input_x
        self.rf_input_y: RFInput = rf_input_y

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Index: {self.index}, " \
               f"Antenna: {self.antenna}, " \
               f"Tile Id: {self.tile_id}, " \
               f"Tile Name: {self.tile_name}, " \
               f"RF Input X: {self.rf_input_x!r}, " \
               f"RF Input Y: {self.rf_input_y!r})"
