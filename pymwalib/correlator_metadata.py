#!/usr/bin/env python
#
# Class for accessing Correlator Metadata
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import ctypes as ct
from .mwalib import mwalib_library,CCorrelatorMetadataS,CCorrelatorContextS,create_string_buffer
from .common import ERROR_MESSAGE_LEN,MWAVersion
from .errors import PymwalibCorrelatorMetadataGetError


class CorrelatorMetadata:
    def __init__(self,
                 correlator_context: ct.POINTER(CCorrelatorContextS)
                 ):
        """Retrieve all of the correlator metadata and populate this class."""
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_object_ptr = ct.POINTER(CCorrelatorMetadataS)()

        if mwalib_library.mwalib_correlator_metadata_get(correlator_context,
                                                 ct.byref(c_object_ptr),
                                                 error_message,
                                                 ERROR_MESSAGE_LEN) != 0:
            raise PymwalibCorrelatorMetadataGetError(
                f"Error creating correlator metadata object: {error_message.decode('utf-8').rstrip()}")
        else:
            c_object =c_object_ptr.contents

            # Populate all the fields
            self.mwa_version: MWAVersion = MWAVersion(c_object.mwa_version)

            self.num_timesteps = c_object.num_timesteps
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

            self.num_timestep_coarse_chan_bytes: int = c_object.num_timestep_coarse_chan_bytes
            self.num_timestep_coarse_chan_floats: int = c_object.num_timestep_coarse_chan_floats
            self.num_gpubox_files: int = c_object.num_gpubox_files

            # We're now finished with the C memory, so free it
            mwalib_library.mwalib_correlator_metadata_free(c_object)

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(\n" \
               f"MWA Version                           : {MWAVersion(self.mwa_version).name}\n" \
               f"Num timesteps                         : {self.num_timesteps}\n" \
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
               f"Num bytes per timestep coarse channel : " \
               f"{float(self.num_timestep_coarse_chan_bytes) / (1024. * 1024.)} MB\n" \
               f"Num floats per timestep coarse channel: " \
               f"{self.num_timestep_coarse_chan_floats}\n" \
               f"(actual) num GPUBox files             : {self.num_gpubox_files}\n)\n"