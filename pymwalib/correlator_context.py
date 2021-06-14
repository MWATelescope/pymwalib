#!/usr/bin/env python
#
# CorrelatorContext: main interface for pymwalib for correlator data
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import numpy.ctypeslib as npct
import ctypes as ct
from .mwalib import CCorrelatorContextS,mwalib_library,create_string_buffer,MWALIB_SUCCESS,MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN
from .common import ERROR_MESSAGE_LEN
from .errors import PymwalibCorrelatorContextNewError,PymwalibCorrelatorContextDisplayError,PymwalibNoDataForTimestepAndCoarseChannel,PymwalibCorrelatorContextReadByBaselineException,PymwalibCorrelatorContextReadByFrequencyException
from .antenna import Antenna
from .baseline import Baseline
from .coarse_channel import CoarseChannel
from .metafits_metadata import MetafitsMetadata
from .correlator_metadata import CorrelatorMetadata
from .rfinput import RFInput
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

        self._correlator_context_object = ct.POINTER(CCorrelatorContextS)()

        # First populate the context object
        self._get_correlator_context(metafits_filename, gpubox_filenames)

        # Now Get metafits metadata
        self.metafits_metadata = MetafitsMetadata(None, self._correlator_context_object, None)

        # Now Get correlator metadata
        self.correlator_metadata = CorrelatorMetadata(self._correlator_context_object)

        # Populate rf_inputs
        self.rfinputs = RFInput.get_rfinputs(None, self._correlator_context_object, None)

        # Populate antennas
        self.antennas = Antenna.get_antennas(None, self._correlator_context_object, None, self.rfinputs)

        # Populate baselines
        self.baselines = Baseline.get_baselines(None, self._correlator_context_object, None)

        # Populate coarse channels
        self.coarse_channels = CoarseChannel.get_coarse_channels(self._correlator_context_object, None)

        # Populate timesteps
        self.timesteps = TimeStep.get_timesteps(self._correlator_context_object, None)

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
                m, g, len(encoded), ct.byref(self._correlator_context_object), error_message, ERROR_MESSAGE_LEN) != 0:
                raise PymwalibCorrelatorContextNewError(f"Error creating correlator context object: "
                                             f"{error_message.decode('utf-8').rstrip()}")
        else:
            raise PymwalibCorrelatorContextNewError(f"Error creating correlator context object: mwalib is not loaded.")

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

         float_buffer_type = ct.c_float * self.correlator_metadata.num_timestep_coarse_chan_floats
         buffer = float_buffer_type()

         ret_val = mwalib_library.mwalib_correlator_context_read_by_baseline(self._correlator_context_object,
                                                              ct.c_size_t(timestep_index),
                                                              ct.c_size_t(coarse_chan_index),
                                                              buffer,
                                                              self.correlator_metadata.num_timestep_coarse_chan_floats,
                                                              error_message, ERROR_MESSAGE_LEN)

         if ret_val == MWALIB_SUCCESS:
             return npct.as_array(buffer, shape=(self.correlator_metadata.num_timestep_coarse_chan_floats,))
         elif ret_val == MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN:
             raise PymwalibNoDataForTimestepAndCoarseChannel(f"No data exists for this timestep {timestep_index} and coarse channel {coarse_chan_index}")
         else:
             raise PymwalibCorrelatorContextReadByBaselineException(f"Error reading data: "
                                                  f"{error_message.decode('utf-8').rstrip()}")


    def read_by_frequency(self, timestep_index: int, coarse_chan_index: int):
        """Retrieve one HDU (ordered freq,baseline,pol,r,i) as a numpy array."""
        error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN

        float_buffer_type = ct.c_float * self.correlator_metadata.num_timestep_coarse_chan_floats
        buffer = float_buffer_type()

        ret_val = mwalib_library.mwalib_correlator_context_read_by_frequency(self._correlator_context_object,
                                                              ct.c_size_t(timestep_index),
                                                              ct.c_size_t(coarse_chan_index),
                                                              buffer,
                                                              self.correlator_metadata.num_timestep_coarse_chan_floats,
                                                              error_message, ERROR_MESSAGE_LEN)
        if ret_val == MWALIB_SUCCESS:
            return npct.as_array(buffer, shape=(self.correlator_metadata.num_timestep_coarse_chan_floats,))
        elif ret_val == MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN:
            raise PymwalibNoDataForTimestepAndCoarseChannel(f"No data exists for this timestep {timestep_index} and coarse channel {coarse_chan_index}")
        else:
            raise PymwalibCorrelatorContextReadByFrequencyException(f"Error reading data: "
                                                                   f"{error_message.decode('utf-8').rstrip()}")
