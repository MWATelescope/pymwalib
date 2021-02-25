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
from pymwalib.mwalib import *
from pymwalib.common import ERROR_MESSAGE_LEN,CorrelatorVersion
from pymwalib.errors import *


class CorrelatorMetadata:
    def __init__(self,
                 correlator_context: ct.POINTER(CCorrelatorContextS)
                 ):
        """Retrieve all of the correlator metadata and populate this class."""
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_object_ptr = ct.POINTER(CCorrelatorMetadataS)()

        if mwalib.mwalib_correlator_metadata_get(correlator_context,
                                                 ct.byref(c_object_ptr),
                                                 error_message,
                                                 ERROR_MESSAGE_LEN) != 0:
            raise ContextCorrelatorMetadataGetError(
                f"Error creating correlator metadata object: {error_message.decode('utf-8').rstrip()}")
        else:
            c_object =c_object_ptr.contents

            # Populate all the fields
            self.corr_version: CorrelatorVersion = c_object.corr_version
            self.start_unix_time_milliseconds: int = c_object.start_unix_time_milliseconds
            self.end_unix_time_milliseconds: int = c_object.end_unix_time_milliseconds
            self.duration_milliseconds: int = c_object.duration_milliseconds
            self.num_timesteps: int = c_object.num_timesteps
            self.num_coarse_channels: int = c_object.num_coarse_channels
            self.bandwidth_hz: int = c_object.bandwidth_hz
            self.num_timestep_coarse_channel_bytes: int = c_object.num_timestep_coarse_channel_bytes
            self.num_timestep_coarse_channel_floats: int = c_object.num_timestep_coarse_channel_floats
            self.num_gpubox_files: int = c_object.num_gpubox_files

            # We're now finished with the C memory, so free it
            mwalib.mwalib_correlator_metadata_free(c_object)

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(\n" \
               f"Correlator Version                    : {CorrelatorVersion(self.corr_version).name}\n" \
               f"(actual) Start time                   : {float(self.start_unix_time_milliseconds) / 1000.} UNIX\n" \
               f"(actual) End time                     : {float(self.end_unix_time_milliseconds) / 1000.} UNIX\n" \
               f"(actual) Duration                     : {float(self.duration_milliseconds) / 1000.} s\n" \
               f"(actual) num timesteps                : {self.num_timesteps}\n" \
               f"(actual) num coarse channels          : {self.num_coarse_channels}\n" \
               f"(Data) Observation bandwidth          : {float(self.bandwidth_hz) / 1000000.} MHz\n" \
               f"Num bytes per timestep coarse channel : " \
               f"{float(self.num_timestep_coarse_channel_bytes) / (1024. * 1024.)} MB\n" \
               f"Num floats per timestep coarse channel: " \
               f"{self.num_timestep_coarse_channel_floats}\n" \
               f"(actual) num GPUBox files             : {self.num_gpubox_files}\n)\n"