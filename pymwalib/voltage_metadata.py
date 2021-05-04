#!/usr/bin/env python
#
# Main interface for accessing Voltage metadata.
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
            self.start_gps_time_ms: int = c_object.start_gps_time_ms
            self.end_gps_time_ms: int = c_object.end_gps_time_ms
            self.start_unix_time_ms: int = c_object.start_unix_time_ms
            self.end_unix_time_ms: int = c_object.end_unix_time_ms
            self.duration_ms: int = c_object.duration_ms
            self.num_timesteps: int = c_object.num_timesteps
            self.timesteps_duration_ms: int = c_object.timestep_duration_ms
            self.num_coarse_chans: int = c_object.num_coarse_chans
            self.bandwidth_hz: int = c_object.bandwidth_hz
            self.coarse_chan_width_hz: int = c_object.coarse_chan_width_hz
            self.fine_chan_width_hz: int = c_object.fine_chan_width_hz
            self.num_fine_chans_per_coarse: int = c_object.num_fine_chans_per_coarse

            self.sample_size_bytes: int = c_object.sample_size_bytes
            self.num_voltage_blocks_per_timestep: int = c_object.num_voltage_blocks_per_timestep
            self.num_voltage_blocks_per_second: int = c_object.num_voltage_blocks_per_second
            self.num_samples_per_voltage_block: int = c_object.num_samples_per_voltage_block
            self.voltage_block_size_bytes: int = c_object.voltage_block_size_bytes
            self.delay_block_size_bytes: int = c_object.delay_block_size_bytes
            self.data_file_header_size_bytes: int = c_object.data_file_header_size_bytes
            self.expected_voltage_data_file_size_bytes: int = c_object.expected_voltage_data_file_size_bytes

            # We're now finished with the C memory, so free it
            mwalib.mwalib_voltage_metadata_free(c_object)

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(\n" \
               f"Correlator Version                    : {CorrelatorVersion(self.corr_version).name}\n" \
               f"(actual) Start time (UNIX)            : {float(self.start_unix_time_ms) / 1000.} UNIX\n" \
               f"(actual) End time (UNIX)              : {float(self.end_unix_time_ms) / 1000.} UNIX\n" \
               f"(actual) Start time (GPS)             : {float(self.start_gps_time_ms) / 1000.} GPS\n" \
               f"(actual) End time (GPS)               : {float(self.end_gps_time_ms) / 1000.} GPS\n" \
               f"(actual) Duration                     : {float(self.duration_ms) / 1000.} s\n" \
               f"(actual) num timesteps                : {self.num_timesteps}\n" \
               f"Tmestep duration (ms)                 : {self.timesteps_duration_ms} ms\n" \               
               f"(actual) num coarse channels          : {self.num_coarse_chans}\n" \
               f"(Data) Bandwidth (of data we have)    : {float(self.bandwidth_hz) / 1000000.} MHz\n" \
               f"Coarse channel width                  : {float(self.coarse_chan_width_hz) / 1000000.} MHz\n" \
               f"Fine channel width                    : {float(self.fine_chan_width_hz) / 1000.} kHz\n" \
               f"Num fine channels per coarse          : {self.num_fine_chans_per_coarse}\n" \               
               f"Sample size                           : {self.sample_size_bytes} bytes\n" \
               f"Num voltage blocks per timeste        : {self.num_voltage_blocks_per_timestep}\n" \
               f"Num voltage blocks per second         : {self.num_voltage_blocks_per_second}\n" \
               f"Num samples per voltage block         : {self.num_samples_per_voltage_block}\n" \
               f"Voltage block size                    : {self.voltage_block_size_bytes} bytes\n" \
               f"Delay block size                      : {self.delay_block_size_bytes} bytes\n" \
               f"Data file header size                 : {self.data_file_header_size_bytes} bytes\n" \
               f"Expected voltage data file size       : {self.expected_voltage_data_file_size_bytes} bytes\n)\n"
