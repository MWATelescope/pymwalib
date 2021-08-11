#!/usr/bin/env python
#
# rf_input: class representing a single rf_input in mwalib
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from .mwalib import CRFInputS, CMetafitsMetadataS


class RFInput:
    """
    A class representing a single RFInput

    Attributes
    ----------
    index : int
        Ordinal index of this RF Input.

    Please see https://github.com/MWATelescope/mwalib/blob/master/src/rf_input.rs for remaining attributes

    """

    def __init__(self,
                 index: int,
                 input: int,
                 ant: int,
                 tile_id: int,
                 tile_name: str,
                 pol: str,
                 electrical_length_m: float,
                 north_m: float,
                 east_m: float,
                 height_m: float,
                 vcs_order: int,
                 subfile_order: int,
                 flagged: bool,
                 digital_gains: [],
                 num_digital_gains: int,
                 dipole_delays: [],
                 num_dipole_delays: int,
                 dipole_gains: [],
                 num_dipole_gains: int,
                 rec_number: int,
                 rec_slot_number: int):
        """Initialise the class"""
        self.index: int = index
        self.input: int = input
        self.ant: int = ant
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
        self.num_digital_gains = num_digital_gains
        self.digital_gains = digital_gains
        self.num_dipole_delays = num_dipole_delays
        self.dipole_delays = dipole_delays
        self.num_dipole_gains = num_dipole_gains
        self.dipole_gains = dipole_gains
        self.rec_number = rec_number
        self.rec_slot_number = rec_slot_number

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Index: {self.index}, " \
               f"Input: {self.input}, " \
               f"Ant: {self.ant}, " \
               f"Tile Id: {self.tile_id}, " \
               f"Tile Name: {self.tile_name}, " \
               f"Pol: {self.pol}, " \
               f"Electrical length: {self.electrical_length_m}, " \
               f"north_m: {self.north_m}, " \
               f"east_m: {self.east_m}, " \
               f"height_m: {self.height_m}, " \
               f"vcs_order: {self.vcs_order}, " \
               f"subfile_order: {self.subfile_order}, " \
               f"flagged: {self.flagged}, " \
               f"digital_gains: {self.digital_gains}, " \
               f"dipole_delays: {self.dipole_delays}, " \
               f"dipole_gains: {self.dipole_gains}, " \
               f"rec_number: {self.rec_number}, " \
               f"rec_slot_number: {self.rec_slot_number})"

    @staticmethod
    def get_rf_inputs(metafits_metadata: CMetafitsMetadataS) -> []:
        """Retrieve all of the rf_input metadata and populate a list of rf_inputs."""
        rf_inputs = []

        for i in range(0, metafits_metadata.num_rf_inputs):
            obj: CRFInputS = metafits_metadata.rf_inputs[i]

            digital_gains = []
            for i in range(0, obj.num_digital_gains):
                digital_gains.append(obj.digital_gains[i])

            dipole_delays = []
            for j in range(0, obj.num_dipole_delays):
                dipole_delays.append(obj.dipole_delays[j])

            dipole_gains = []
            for k in range(0, obj.num_dipole_gains):
                dipole_gains.append(obj.dipole_gains[k])

            # Populate all the fields
            rf_inputs.append(RFInput(i,
                                     obj.input,
                                     obj.ant,
                                     obj.tile_id,
                                     obj.tile_name.decode("utf-8"),
                                     obj.pol.decode("utf-8"),
                                     obj.electrical_length_m,
                                     obj.north_m,
                                     obj.east_m,
                                     obj.height_m,
                                     obj.vcs_order,
                                     obj.subfile_order,
                                     obj.flagged,
                                     digital_gains,
                                     obj.num_digital_gains,
                                     dipole_delays,
                                     obj.num_dipole_delays,
                                     dipole_gains,
                                     obj.num_dipole_gains,
                                     obj.rec_number,
                                     obj.rec_slot_number))

        return rf_inputs
