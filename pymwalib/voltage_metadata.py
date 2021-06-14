#!/usr/bin/env python
#
# Main interface for accessing Voltage metadata.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from .mwalib import mwalib_library,ct,CVoltageMetadataS, CVoltageContextS,create_string_buffer
from .errors import PymwalibVoltageMetadataGetError
from .common import MWAVersion, ERROR_MESSAGE_LEN


class VoltageMetadata:
    def __init__(self,
                 voltage_context: ct.POINTER(CVoltageContextS)):
        """Retrieve all of the metafits metadata and populate this class."""
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_object_ptr = ct.POINTER(CVoltageMetadataS)()

        if mwalib_library.mwalib_voltage_metadata_get(voltage_context,
                                              ct.byref(c_object_ptr),
                                              error_message,
                                              ERROR_MESSAGE_LEN) != 0:
            raise PymwalibVoltageMetadataGetError(
                f"Error creating voltage metadata object: {error_message.decode('utf-8').rstrip()}")
        else:
            c_object = c_object_ptr.contents

            # Populate all the fields
            self.mwa_version: MWAVersion = MWAVersion(c_object.mwa_version)

            self.num_timesteps = c_object.num_timesteps
            self.timestep_duration_ms: int = c_object.timestep_duration_ms
            self.num_coarse_chans = c_object.num_coarse_chans

            self.num_common_timesteps = c_object.num_common_timesteps
            self.num_common_coarse_chans = c_object.num_common_coarse_chans
            self.common_start_unix_time_ms = c_object.common_start_unix_time_ms
            self.common_end_unix_time_ms = c_object.common_end_unix_time_ms
            self.common_start_gps_time_ms = c_object.common_start_gps_time_ms
            self.common_end_gps_time_ms = c_object.common_end_gps_time_ms
            self.common_duration_ms = c_object.common_duration_ms
            self.common_bandwidth_hz = c_object.common_bandwidth_hz

            self.num_common_good_timesteps = c_object.num_common_good_timesteps
            self.num_common_good_coarse_chans = c_object.num_common_good_coarse_chans
            self.common_good_start_unix_time_ms = c_object.common_good_start_unix_time_ms
            self.common_good_end_unix_time_ms = c_object.common_good_end_unix_time_ms
            self.common_good_start_gps_time_ms = c_object.common_good_start_gps_time_ms
            self.common_good_end_gps_time_ms = c_object.common_good_end_gps_time_ms
            self.common_good_duration_ms = c_object.common_good_duration_ms
            self.common_good_bandwidth_hz = c_object.common_good_bandwidth_hz

            self.num_provided_timestep_indices = c_object.num_provided_timestep_indices
            self.num_provided_coarse_chan_indices = c_object.num_provided_coarse_chan_indices

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
            mwalib_library.mwalib_voltage_metadata_free(c_object)

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(\n" \
               f"MWA Version                           : {MWAVersion(self.mwa_version).name}\n" \
               f"Num timesteps                         : {self.num_timesteps}\n" \
               f"Tmestep duration (ms)                 : {self.timestep_duration_ms} ms\n" \
               f"Num coarse channels                   : {self.num_coarse_chans}\n" \
               f"num_provided_timestep_indices         : {self.num_provided_timestep_indices}\n" \
               f"num_provided_coarse_chan_indices      : {self.num_provided_coarse_chan_indices}\n" \
               f"(common) Start time (UNIX)            : {float(self.common_start_unix_time_ms) / 1000.}\n" \
               f"(common) End time (UNIX)              : {float(self.common_end_unix_time_ms) / 1000.}\n" \
               f"(common) Start time (GPS)             : {float(self.common_start_gps_time_ms) / 1000.}\n" \
               f"(common) End time (GPS)               : {float(self.common_end_gps_time_ms) / 1000.}\n" \
               f"(common) Duration                     : {float(self.common_duration_ms) / 1000.} s\n" \
               f"(common) num timesteps                : {self.num_common_timesteps}\n" \
               f"(common) num coarse channels          : {self.num_common_coarse_chans}\n" \
               f"(common) Bandwidth                    : {float(self.common_bandwidth_hz) / 1000000.} MHz\n" \
               f"(common good) Start time (UNIX)       : {float(self.common_good_start_unix_time_ms) / 1000.}\n" \
               f"(common good) End time (UNIX)         : {float(self.common_good_end_unix_time_ms) / 1000.}\n" \
               f"(common good) Start time (GPS)        : {float(self.common_good_start_gps_time_ms) / 1000.}\n" \
               f"(common good) End time (GPS)          : {float(self.common_good_end_gps_time_ms) / 1000.}\n" \
               f"(common good) Duration                : {float(self.common_good_duration_ms) / 1000.} s\n" \
               f"(common good) num timesteps           : {self.num_common_good_timesteps}\n" \
               f"(common good) num coarse channels     : {self.num_common_good_coarse_chans}\n" \
               f"(common good) Bandwidth               : {float(self.common_good_bandwidth_hz) / 1000000.} MHz\n" \
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
