#!/usr/bin/env python
#
# antenna: class representing a single antenna in mwalib
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from .mwalib import CAntennaS, CMetafitsMetadataS
from .rfinput import RFInput


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
                 ant: int,
                 tile_id: int,
                 tile_name: str,
                 rf_input_x: RFInput,
                 rf_input_y: RFInput,
                 electrical_length_m: float,
                 north_m: float,
                 east_m: float,
                 height_m: float):
        """Initialise the class"""
        self.index: int = index
        self.ant: int = ant
        self.tile_id: int = tile_id
        self.tile_name: str = tile_name
        self.rf_input_x: RFInput = rf_input_x
        self.rf_input_y: RFInput = rf_input_y
        self.electrical_length_m = electrical_length_m
        self.north_m = north_m
        self.east_m = east_m
        self.height_m = height_m

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Index: {self.index}, " \
               f"ant: {self.ant}, " \
               f"Tile Id: {self.tile_id}, " \
               f"Tile Name: {self.tile_name}, " \
               f"RF Input X: {self.rf_input_x!r}, " \
               f"RF Input Y: {self.rf_input_y!r}, " \
               f"Electrical length: {self.electrical_length_m!r} m, " \
               f"North: {self.north_m} m, " \
               f"East: {self.east_m} m, " \
               f"Height: {self.height_m} m)"

    @staticmethod
    def get_antennas(metafits_metadata: CMetafitsMetadataS,
                     rf_inputs: []) -> []:
        """Retrieve all of the antenna metadata and populate a list of antennas."""
        antennas = []

        for i in range(0, metafits_metadata.num_ants):
            obj: CAntennaS = metafits_metadata.antennas[i]

            # Populate all the fields
            antennas.append(Antenna(i,
                                    obj.ant,
                                    obj.tile_id,
                                    obj.tile_name.decode("utf-8"),
                                    rf_inputs[obj.rfinput_x],
                                    rf_inputs[obj.rfinput_y],
                                    obj.electrical_length_m,
                                    obj.north_m,
                                    obj.east_m,
                                    obj.height_m))

        return antennas
