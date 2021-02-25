#!/usr/bin/env python
#
# context: main interface for pymwalib
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
import enum
import numpy.ctypeslib as npct
from datetime import datetime
from pymwalib.mwalib import *
from pymwalib.errors import *
from pymwalib.common import CorrelatorVersion, ERROR_MESSAGE_LEN


class VoltageMetadata:
    def __init__(self,
                 voltage_context: ct.POINTER(CVoltageContextS)):
        """Retrieve all of the metafits metadata and populate this class."""
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_object_ptr = ct.POINTER(CVoltageMetadataS)()

        if mwalib.mwalib_voltage_metadata_get(voltage_context,
                                              ct.byref(c_object_ptr),
                                              error_message,
                                              ERROR_MESSAGE_LEN) != 0:
            raise ContextVoltageMetadataGetError(
                f"Error creating voltage metadata object: {error_message.decode('utf-8').rstrip()}")
        else:
            c_object = c_object_ptr.contents

            # Populate all the fields
            self.corr_version: CorrelatorVersion = c_object.corr_version
            self.start_gps_time_milliseconds: int = c_object.start_gps_time_milliseconds
            self.end_gps_time_milliseconds: int = c_object.end_gps_time_milliseconds
            self.duration_milliseconds: int = c_object.duration_milliseconds
            self.num_timesteps: int = c_object.num_timesteps
            self.num_coarse_channels: int = c_object.num_coarse_channels
            self.bandwidth_hz: int = c_object.bandwidth_hz
            self.coarse_channel_width_hz: int = c_object.coarse_channel_width_hz
            self.fine_channel_width_hz: int = c_object.fine_channel_width_hz
            self.num_fine_channels_per_coarse: int = c_object.num_fine_channels_per_coarse

            # We're now finished with the C memory, so free it
            mwalib.mwalib_voltage_metadata_free(c_object)

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(\n" \
               f"Correlator Version                    : {CorrelatorVersion(self.corr_version).name}\n" \
               f"(actual) Start time (GPS)             : {float(self.start_gps_time_milliseconds) / 1000.} UNIX\n" \
               f"(actual) End time (GPS)               : {float(self.end_gps_time_milliseconds) / 1000.} UNIX\n" \
               f"(actual) Duration                     : {float(self.duration_milliseconds) / 1000.} s\n" \
               f"(actual) num timesteps                : {self.num_timesteps}\n" \
               f"(actual) num coarse channels          : {self.num_coarse_channels}\n" \
               f"Correlator fine channel width         : {float(self.fine_channel_width_hz) / 1000.} kHz\n" \
               f"(Data) Observation bandwidth          : {float(self.bandwidth_hz) / 1000000.} MHz\n" \
               f"Coarse channel width                  : {float(self.coarse_channel_width_hz) / 1000000.} MHz\n" \
               f"Num fine channels per coarse          : {self.num_fine_channels_per_coarse}\n)\n"