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
from pymwalib.mwalib import create_string_buffer, mwalib, CRFInputS, CMetafitsContextS, CCorrelatorContextS, CVoltageContextS
from pymwalib.common import ERROR_MESSAGE_LEN
from pymwalib.errors import *
import ctypes as ct


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
                 flagged: bool,
                 receiver_number: int,
                 receiver_slot_number: int):
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
        self.receiver_number = receiver_number
        self.receiver_slot_number = receiver_slot_number

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
               f"flagged: {self.flagged}, " \
               f"receiver_number: {self.receiver_number}, " \
               f"receiver_slot_number: {self.receiver_slot_number})"

    @staticmethod
    def get_rfinputs(metafits_context: ct.POINTER(CMetafitsContextS),
                     correlator_context: ct.POINTER(CCorrelatorContextS),
                     voltage_context: ct.POINTER(CVoltageContextS)) -> []:
        """Retrieve all of the rf_input metadata and populate a list of rf_inputs."""
        rf_inputs = []
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_array_ptr = ct.POINTER(CRFInputS)()
        c_len_ptr = ct.c_size_t(0)

        if mwalib.mwalib_rfinputs_get(metafits_context,
                                      correlator_context,
                                      voltage_context,
                                      ct.byref(c_array_ptr),
                                      ct.byref(c_len_ptr),
                                      error_message,
                                      ERROR_MESSAGE_LEN) != 0:
            # Error
            raise ContextRFInputsGetError(f"Error getting rf_inputs object: "
                                          f"{error_message.decode('utf-8').rstrip()}")
        else:
            for i in range(0, c_len_ptr.value):
                # Populate all the fields
                rf_inputs.append(RFInput(i,
                                         c_array_ptr[i].input,
                                         c_array_ptr[i].antenna,
                                         c_array_ptr[i].tile_id,
                                         c_array_ptr[i].tile_name.decode("utf-8"),
                                         c_array_ptr[i].pol.decode("utf-8"),
                                         c_array_ptr[i].electrical_length_m,
                                         c_array_ptr[i].north_m,
                                         c_array_ptr[i].east_m,
                                         c_array_ptr[i].height_m,
                                         c_array_ptr[i].vcs_order,
                                         c_array_ptr[i].subfile_order,
                                         c_array_ptr[i].flagged,
                                         c_array_ptr[i].receiver_number,
                                         c_array_ptr[i].receiver_slot_number))

            # We're now finished with the C memory, so free it
            mwalib.mwalib_rfinputs_free(c_array_ptr, c_len_ptr.value)

            return rf_inputs