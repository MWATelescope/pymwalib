#!/usr/bin/env python
#
# rf_input: class representing a single rf_input in mwalib
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


class RFInput:
    """
    A class representing a single mwalibRFInput

    Attributes
    ----------
    index : int
        Ordinal index of this RF Input.

    Please see https://github.com/MWATelescope/mwalib/blob/master/src/rf_input.rs for remaining attributes

    """

    def __init__(self,
                 index: int,
                 input: int,
                 antenna: int,
                 tile_id: int,
                 tile_name: str,
                 pol: str,
                 electrical_length_m: float,
                 north_m: float,
                 east_m: float,
                 height_m: float,
                 vcs_order: int,
                 subfile_order: int,
                 flagged: bool):
        """Initialise the class"""
        self.index: int = index
        self.input: int = input
        self.antenna: int = antenna
        self.tile_id: int = tile_id
        self.tile_name: str = tile_name
        self.pol: str = pol
        self.electrical_length_m: float = electrical_length_m
        self.north_m: float = north_m
        self.east_m: float = east_m
        self.height_m: float = height_m
        self.vcs_order: int = vcs_order
        self.subfile_order: int = subfile_order
        self.flagged: bool = flagged

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Index: {self.index}, " \
               f"Input: {self.input}, " \
               f"Antenna: {self.antenna}, " \
               f"Tile Id: {self.tile_id}, " \
               f"Tile Name: {self.tile_name}, " \
               f"Pol: {self.pol}, " \
               f"Electrical length: {self.electrical_length_m}, " \
               f"north_m: {self.north_m}, " \
               f"east_m: {self.east_m}, " \
               f"height_m: {self.height_m}, " \
               f"vcs_order: {self.vcs_order}, " \
               f"subfile_order: {self.subfile_order}, " \
               f"flagged: {self.flagged})"
