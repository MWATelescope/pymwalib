#!/usr/bin/env python
#
# CorrelatorContext: main interface for pymwalib for correlator data
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import ctypes

import numpy.ctypeslib as npct
import ctypes as ct
from .mwalib import CCorrelatorContextS, CCorrelatorMetadataS, mwalib_library, create_string_buffer, MWALIB_SUCCESS, \
    MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN
from .coarse_channel import CoarseChannel
from .common import ERROR_MESSAGE_LEN, MWAVersion
from .errors import PymwalibCorrelatorContextNewError, PymwalibCorrelatorContextDisplayError, \
    PymwalibNoDataForTimestepAndCoarseChannelError, PymwalibCorrelatorContextReadByBaselineError, \
    PymwalibCorrelatorContextReadByFrequencyError, PymwalibCorrelatorMetadataGetError, \
    PymwalibCorrelatorContextGetFineChanFreqsArrayError
from .metafits_metadata import MetafitsMetadata
from .timestep import TimeStep
from .version import check_mwalib_version


class CorrelatorContext:
    """Main class to interface with mwalib correlator observations"""

    def __init__(self, metafits_filename: str, gpubox_filenames: list):
        """Take metafits and gpubox files, and populate this class via mwalib"""
        #
        # Ensure we have a compatible version of mwalib
        #
        check_mwalib_version()

        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)
        self._correlator_context_object = ct.POINTER(CCorrelatorContextS)()

        # First populate the context object
        self._get_correlator_context(metafits_filename, gpubox_filenames)

        # Get correlator metadata
        c_object_ptr = ct.POINTER(CCorrelatorMetadataS)()
        if mwalib_library.mwalib_correlator_metadata_get(self._correlator_context_object,
                                                         ct.byref(c_object_ptr),
                                                         error_message,
                                                         ERROR_MESSAGE_LEN) != 0:
            raise PymwalibCorrelatorMetadataGetError(
                f"Error creating correlator metadata object: {error_message.decode('utf-8').rstrip()}")

        c_object = c_object_ptr.contents

        # Populate all the fields
        self.mwa_version: MWAVersion = MWAVersion(c_object.mwa_version)

        self.num_timesteps: int = c_object.num_timesteps
        self.num_coarse_chans: int = c_object.num_coarse_chans

        self.num_common_timesteps: int = c_object.num_common_timesteps
        self.num_common_coarse_chans: int = c_object.num_common_coarse_chans
        self.common_start_unix_time_ms = c_object.common_start_unix_time_ms
        self.common_end_unix_time_ms = c_object.common_end_unix_time_ms
        self.common_start_gps_time_ms = c_object.common_start_gps_time_ms
        self.common_end_gps_time_ms = c_object.common_end_gps_time_ms
        self.common_duration_ms = c_object.common_duration_ms
        self.common_bandwidth_hz = c_object.common_bandwidth_hz

        self.num_common_good_timesteps: int = c_object.num_common_good_timesteps
        self.num_common_good_coarse_chans: int = c_object.num_common_good_coarse_chans
        self.common_good_start_unix_time_ms = c_object.common_good_start_unix_time_ms
        self.common_good_end_unix_time_ms = c_object.common_good_end_unix_time_ms
        self.common_good_start_gps_time_ms = c_object.common_good_start_gps_time_ms
        self.common_good_end_gps_time_ms = c_object.common_good_end_gps_time_ms
        self.common_good_duration_ms = c_object.common_good_duration_ms
        self.common_good_bandwidth_hz = c_object.common_good_bandwidth_hz

        self.num_provided_timesteps: int = c_object.num_provided_timesteps
        self.num_provided_coarse_chans: int = c_object.num_provided_coarse_chans

        self.num_timestep_coarse_chan_bytes: int = c_object.num_timestep_coarse_chan_bytes
        self.num_timestep_coarse_chan_floats: int = c_object.num_timestep_coarse_chan_floats
        self.num_gpubox_files: int = c_object.num_gpubox_files

        # Common timesteps
        self.common_timestep_indices = []
        for i in range(self.num_common_timesteps):
            self.common_timestep_indices.append(c_object.common_timestep_indices[i])

        # Common coarse chans
        self.common_coarse_chan_indices = []
        for i in range(self.num_common_coarse_chans):
            self.common_coarse_chan_indices.append(c_object.common_coarse_chan_indices[i])

        # Common Good timesteps
        self.common_good_timestep_indices = []
        for i in range(self.num_common_good_timesteps):
            self.common_good_timestep_indices.append(c_object.common_good_timestep_indices[i])

        # Common Good coarse chans
        self.common_good_coarse_chan_indices = []
        for i in range(self.num_common_good_coarse_chans):
            self.common_good_coarse_chan_indices.append(c_object.common_good_coarse_chan_indices[i])

        # Provided timesteps
        self.provided_timestep_indices = []
        for i in range(self.num_provided_timesteps):
            self.provided_timestep_indices.append(c_object.provided_timestep_indices[i])

        # Provided coarse chans
        self.provided_coarse_chan_indices = []
        for i in range(self.num_provided_coarse_chans):
            self.provided_coarse_chan_indices.append(c_object.provided_coarse_chan_indices[i])

        # Now Get metafits context
        self.metafits_context: MetafitsMetadata = MetafitsMetadata(None, self._correlator_context_object, None)

        # Populate coarse channels
        self.coarse_channels = CoarseChannel.get_correlator_or_voltage_coarse_channels(c_object_ptr.contents)

        # Populate timesteps
        self.timesteps = TimeStep.get_correlator_or_voltage_timesteps(c_object_ptr.contents)

        # We're now finished with the C memory, so free it
        mwalib_library.mwalib_correlator_metadata_free(c_object)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure we free the rust allocated memory in mwalib"""
        if self._correlator_context_object:
            mwalib_library.mwalib_correlator_context_free(self._correlator_context_object)

    def _get_correlator_context(self, metafits_filename: str, gpubox_filenames: list):
        """This method will read and validate the metafits and gpubox files. If all has worked, then
        the context object can be used in subsequent calls to populate aspects of this class."""
        if mwalib_library:
            # Encode all inputs as UTF-8.
            m = ct.c_char_p(metafits_filename.encode("utf-8"))

            # https://stackoverflow.com/questions/4145775/how-do-i-convert-a-python-list-into-a-c-array-by-using-ctypes
            encoded = []
            for g in gpubox_filenames:
                encoded.append(ct.c_char_p(g.encode("utf-8")))
            seq = ct.c_char_p * len(encoded)
            g = seq(*encoded)
            error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

            if mwalib_library.mwalib_correlator_context_new(
                    m, g, len(encoded), ct.byref(self._correlator_context_object), error_message,
                    ERROR_MESSAGE_LEN) != 0:
                raise PymwalibCorrelatorContextNewError(f"Error creating correlator context object: "
                                                        f"{error_message.decode('utf-8').rstrip()}")
        else:
            raise PymwalibCorrelatorContextNewError("Error creating correlator context object: mwalib is not loaded.")

    def get_fine_chan_freqs_hz_array(self, corr_coarse_chan_indices) -> list:
        """Populates a list of fine channel centre frequencies based on the input list of coarse channel
           indices"""
        error_message = create_string_buffer(ERROR_MESSAGE_LEN)

        corr_coarse_chan_indices_type = ctypes.c_ulong * len(corr_coarse_chan_indices)
        corr_coarse_chan_indices_array = corr_coarse_chan_indices_type(*corr_coarse_chan_indices)

        out_frequencies_len = len(corr_coarse_chan_indices) * self.metafits_context.num_corr_fine_chans_per_coarse
        out_frequencies_type = ct.c_double * out_frequencies_len
        out_frequencies = out_frequencies_type()

        if mwalib_library.mwalib_correlator_context_get_fine_chan_freqs_hz_array(self._correlator_context_object,
                                                                                 corr_coarse_chan_indices_array,
                                                                                 len(corr_coarse_chan_indices),
                                                                                 out_frequencies,
                                                                                 out_frequencies_len,
                                                                                 error_message,
                                                                                 ERROR_MESSAGE_LEN) != 0:
            raise PymwalibCorrelatorContextGetFineChanFreqsArrayError(
                f"Error calling mwalib_correlator_get_fine_chan_freqs_hz_array(): "
                f"{error_message.decode('utf-8').rstrip()}")
        out_frequencies_list = []

        for i in range(0, out_frequencies_len):
            out_frequencies_list.append(out_frequencies[i])

        return out_frequencies_list

    def display(self):
        """Displays a human readable summary of the correlator context"""
        error_message = create_string_buffer(ERROR_MESSAGE_LEN)

        if mwalib_library.mwalib_correlator_context_display(self._correlator_context_object,
                                                            error_message,
                                                            ERROR_MESSAGE_LEN) != 0:
            raise PymwalibCorrelatorContextDisplayError(f"Error calling mwalib_correlator_context_display(): "
                                                        f"{error_message.decode('utf-8').rstrip()}")

    def read_by_baseline(self, timestep_index: int, coarse_chan_index: int):
        """Retrieve one HDU (ordered baseline,freq,pol,r,i) as a numpy array."""
        error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN

        float_buffer_type = ct.c_float * self.num_timestep_coarse_chan_floats
        buffer = float_buffer_type()

        ret_val = mwalib_library.mwalib_correlator_context_read_by_baseline(self._correlator_context_object,
                                                                            ct.c_size_t(timestep_index),
                                                                            ct.c_size_t(coarse_chan_index),
                                                                            buffer,
                                                                            self.num_timestep_coarse_chan_floats,
                                                                            error_message, ERROR_MESSAGE_LEN)

        if ret_val == MWALIB_SUCCESS:
            return npct.as_array(buffer, shape=(self.num_timestep_coarse_chan_floats,))
        elif ret_val == MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN:
            raise PymwalibNoDataForTimestepAndCoarseChannelError(
                f"No data exists for this timestep {timestep_index} and coarse channel {coarse_chan_index}")
        else:
            raise PymwalibCorrelatorContextReadByBaselineError(f"Error reading data: "
                                                               f"{error_message.decode('utf-8').rstrip()}")

    def read_by_frequency(self, timestep_index: int, coarse_chan_index: int):
        """Retrieve one HDU (ordered freq,baseline,pol,r,i) as a numpy array."""
        error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN

        float_buffer_type = ct.c_float * self.num_timestep_coarse_chan_floats
        buffer = float_buffer_type()

        ret_val = mwalib_library.mwalib_correlator_context_read_by_frequency(self._correlator_context_object,
                                                                             ct.c_size_t(timestep_index),
                                                                             ct.c_size_t(coarse_chan_index),
                                                                             buffer,
                                                                             self.num_timestep_coarse_chan_floats,
                                                                             error_message, ERROR_MESSAGE_LEN)
        if ret_val == MWALIB_SUCCESS:
            return npct.as_array(buffer, shape=(self.num_timestep_coarse_chan_floats,))
        elif ret_val == MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN:
            raise PymwalibNoDataForTimestepAndCoarseChannelError(
                f"No data exists for this timestep {timestep_index} and coarse channel {coarse_chan_index}")
        else:
            raise PymwalibCorrelatorContextReadByFrequencyError(f"Error reading data: "
                                                                f"{error_message.decode('utf-8').rstrip()}")

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(\n" \
               f"MWA Version                           : {MWAVersion(self.mwa_version).name}\n" \
               f"Num timesteps                         : {self.num_timesteps}\n" \
               f"Num coarse channels                   : {self.num_coarse_chans}\n" \
               f"num_provided_timestep_indices         : {self.num_provided_timesteps}\n" \
               f"num_provided_coarse_chan_indices      : {self.num_provided_coarse_chans}\n" \
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
