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
from pymwalib.mwalib import create_string_buffer, mwalib, CAntennaS, CMetafitsContextS, CCorrelatorContextS, CVoltageContextS
from pymwalib.common import ERROR_MESSAGE_LEN
from pymwalib.errors import *
from pymwalib.rfinput import RFInput
import ctypes as ct

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
                 rf_input_y: RFInput):
        """Initialise the class"""
        self.index: int = index
        self.ant: int = ant
        self.tile_id: int = tile_id
        self.tile_name: str = tile_name
        self.rf_input_x: RFInput = rf_input_x
        self.rf_input_y: RFInput = rf_input_y

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Index: {self.index}, " \
               f"ant: {self.ant}, " \
               f"Tile Id: {self.tile_id}, " \
               f"Tile Name: {self.tile_name}, " \
               f"RF Input X: {self.rf_input_x!r}, " \
               f"RF Input Y: {self.rf_input_y!r})"

    @staticmethod
    def get_antennas(metafits_context: ct.POINTER(CMetafitsContextS),
                     correlator_context: ct.POINTER(CCorrelatorContextS),
                     voltage_context: ct.POINTER(CVoltageContextS),
                     rf_inputs: []) -> []:
        """Retrieve all of the antenna metadata and populate a list of antennas."""
        antennas = []
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_array_ptr = ct.POINTER(CAntennaS)()
        c_len_ptr = ct.c_size_t(0)

        if mwalib.mwalib_antennas_get(metafits_context,
                                      correlator_context,
                                      voltage_context,
                                      ct.byref(c_array_ptr),
                                      ct.byref(c_len_ptr),
                                      error_message,
                                      ERROR_MESSAGE_LEN) != 0:
            # Error
            raise ContextAntennasGetError(f"Error getting antennas object: "
                                          f"{error_message.decode('utf-8').rstrip()}")
        else:
            for i in range(0, c_len_ptr.value):
                # Populate all the fields
                antennas.append(Antenna(i,
                                 c_array_ptr[i].ant,
                                 c_array_ptr[i].tile_id,
                                 c_array_ptr[i].tile_name.decode("utf-8"),
                                 rf_inputs[i * 2],
                                 rf_inputs[(i * 2) + 1]))

            # We're now finished with the C memory, so free it
            mwalib.mwalib_antennas_free(c_array_ptr, c_len_ptr.value)

            return antennas