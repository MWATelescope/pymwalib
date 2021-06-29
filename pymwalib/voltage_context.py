#!/usr/bin/env python
#
# VoltageContext: main interface for pymwalib for voltage data
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import numpy.ctypeslib as npct
from .mwalib import CVoltageContextS,ct,mwalib_library,create_string_buffer,CVoltageMetadataS,MWALIB_SUCCESS,MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN
from .common import ERROR_MESSAGE_LEN,MWAVersion
from .errors import PymwalibVoltageMetadataGetError,PymwalibVoltageContextNewError,PymwalibCorrelatorContextDisplayError,PymwalibNoDataForTimestepAndCoarseChannel,PymwalibVoltageContextReadFileException,PymwalibVoltageContextReadSecondException
from .coarse_channel import CoarseChannel
from .metafits_metadata import MetafitsMetadata
from .timestep import TimeStep
from .version import check_mwalib_version


class VoltageContext:
    """Main class to interface with mwalib"""
    def __init__(self, metafits_filename: str, voltage_filenames: list):
        """Take metafits and voltage files, and populate this class via mwalib"""
        #
        # Ensure we have a compatible version of mwalib
        #
        check_mwalib_version()

        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)
        self._voltage_context_object = ct.POINTER(CVoltageContextS)()

        # First populate the context object
        self._get_voltage_context(metafits_filename, voltage_filenames)

        # Now Get voltage metadata
        c_object_ptr = ct.POINTER(CVoltageMetadataS)()
        if mwalib_library.mwalib_voltage_metadata_get(self._voltage_context_object,
                                                      ct.byref(c_object_ptr),
                                                      error_message,
                                                      ERROR_MESSAGE_LEN) != 0:
            raise PymwalibVoltageMetadataGetError(
                f"Error creating voltage metadata object: {error_message.decode('utf-8').rstrip()}")

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

        # Now Get metafits metadata
        self.metafits_metadata: MetafitsMetadata = MetafitsMetadata(None, None, self._voltage_context_object)

        # Populate coarse channels
        self.coarse_channels = CoarseChannel.get_correlator_or_voltage_coarse_channels(c_object_ptr.contents)

        # Populate timesteps
        self.timesteps = TimeStep.get_correlator_or_voltage_timesteps(c_object_ptr.contents)

        # We're now finished with the C memory, so free it
        mwalib_library.mwalib_voltage_metadata_free(c_object)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure we free the rust allocated memory in mwalib"""
        if self._voltage_context_object:
            mwalib_library.mwalib_voltage_context_free(self._voltage_context_object)

    def _get_voltage_context(self, metafits_filename: str, voltage_filenames: list):
        """This method will read and validate the metafits and voltage files. If all has worked, then
        the context object can be used in subsequent calls to populate aspects of this class."""
        if mwalib_library:
            # Encode all inputs as UTF-8.
            m = ct.c_char_p(metafits_filename.encode("utf-8"))

            # https://stackoverflow.com/questions/4145775/how-do-i-convert-a-python-list-into-a-c-array-by-using-ctypes
            encoded = []
            for v in voltage_filenames:
                encoded.append(ct.c_char_p(v.encode("utf-8")))
            seq = ct.c_char_p * len(encoded)
            g = seq(*encoded)
            error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

            if mwalib_library.mwalib_voltage_context_new(
                m, g, len(encoded), ct.byref(self._voltage_context_object), error_message, ERROR_MESSAGE_LEN) != 0:
                raise PymwalibVoltageContextNewError(f"Error creating voltage context object: "
                                             f"{error_message.decode('utf-8').rstrip()}")
        else:
            raise PymwalibVoltageContextNewError(f"Error creating voltage context object: mwalib is not loaded.")

    def display(self):
         """Displays a human readable summary of the voltage context"""
         error_message = create_string_buffer(ERROR_MESSAGE_LEN)

         if mwalib_library.mwalib_voltage_context_display(self._voltage_context_object,
                                                  error_message,
                                                  ERROR_MESSAGE_LEN) != 0:
             raise PymwalibCorrelatorContextDisplayError(f"Error calling mwalib_voltage_context_display(): "
                                                        f"{error_message.decode('utf-8').rstrip()}")

    def read_file(self, timestep_index: int, coarse_chan_index: int):
         """Retrieve one file of VCS data as a numpy array."""
         error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN

         byte_buffer_len = self.voltage_block_size_bytes * \
                           self.num_voltage_blocks_per_timestep

         byte_buffer_type = ct.c_byte * byte_buffer_len
         buffer = byte_buffer_type()

         ret_val = mwalib_library.mwalib_voltage_context_read_file(self._voltage_context_object,
                                                    ct.c_size_t(timestep_index),
                                                    ct.c_size_t(coarse_chan_index),
                                                    buffer,
                                                    byte_buffer_len,
                                                    error_message, ERROR_MESSAGE_LEN)

         if ret_val == MWALIB_SUCCESS:
             return npct.as_array(buffer, shape=(byte_buffer_len,))
         elif ret_val == MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN:
             raise PymwalibNoDataForTimestepAndCoarseChannel(f"No data exists for this timestep {timestep_index} and coarse channel {coarse_chan_index}")
         else:
             raise PymwalibVoltageContextReadFileException(f"Error reading data: "
                                                         f"{error_message.decode('utf-8').rstrip()}")


    def read_second(self, gps_second_start: int , gps_second_count: int, coarse_chan_index: int):
         """Retrieve multiple seconds of VCS data as a numpy array."""
         error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN

         byte_buffer_len = self.voltage_block_size_bytes * \
                           self.num_voltage_blocks_per_timestep

         byte_buffer_type = ct.c_byte * byte_buffer_len
         buffer = byte_buffer_type()

         ret_val = mwalib_library.mwalib_voltage_context_read_second(self._voltage_context_object,
                                                      ct.c_ulong(gps_second_start),
                                                      ct.c_size_t(gps_second_count),
                                                      ct.c_size_t(coarse_chan_index),
                                                      buffer,
                                                      byte_buffer_len,
                                                      error_message, ERROR_MESSAGE_LEN)

         if ret_val == MWALIB_SUCCESS:
             return npct.as_array(buffer, shape=(byte_buffer_len,))
         elif ret_val == MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN:
             raise PymwalibNoDataForTimestepAndCoarseChannel(f"Not all data exists for {gps_second_start} (for {gps_second_count} sec) and coarse channel {coarse_chan_index}")
         else:
             raise PymwalibVoltageContextReadSecondException(f"Error reading data: "
                                                             f"{error_message.decode('utf-8').rstrip()}")

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
