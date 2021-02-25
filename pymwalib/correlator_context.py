#!/usr/bin/env python
#
# context: main interface for pymwalib for correlator data
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
import numpy.ctypeslib as npct
from pymwalib.mwalib import *
from pymwalib.common import ERROR_MESSAGE_LEN
from pymwalib.errors import *
from pymwalib.antenna import Antenna
from pymwalib.baseline import Baseline
from pymwalib.coarse_channel import CoarseChannel
from pymwalib.metafits_metadata import MetafitsMetadata
from pymwalib.correlator_metadata import CorrelatorMetadata
from pymwalib.rfinput import RFInput
from pymwalib.timestep import TimeStep
from pymwalib.visibility_pol import VisibilityPol


class CorrelatorContext:
    """Main class to interface with mwalib"""
    def __init__(self, metafits_filename: str, gpubox_filenames: list):
        """Take metafits and gpubox files, and populate this class via mwalib"""
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

        # Populate visibility pols
        self.visibility_pols = VisibilityPol.get_visibility_pols(None, self._correlator_context_object, None)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure we free the rust allocated memory in mwalib"""
        if self._correlator_context_object:
            mwalib.mwalib_correlator_context_free(self._correlator_context_object)

    def _get_correlator_context(self, metafits_filename: str, gpubox_filenames: list):
        """This method will read and validate the metafits and gpubox files. If all has worked, then
        the context object can be used in subsequent calls to populate aspects of this class."""
        if mwalib:
            # Encode all inputs as UTF-8.
            m = ct.c_char_p(metafits_filename.encode("utf-8"))

            # https://stackoverflow.com/questions/4145775/how-do-i-convert-a-python-list-into-a-c-array-by-using-ctypes
            encoded = []
            for g in gpubox_filenames:
                encoded.append(ct.c_char_p(g.encode("utf-8")))
            seq = ct.c_char_p * len(encoded)
            g = seq(*encoded)
            error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

            if mwalib.mwalib_correlator_context_new(
                m, g, len(encoded), ct.byref(self._correlator_context_object), error_message, ERROR_MESSAGE_LEN) != 0:
                raise ContextContextNewError(f"Error creating correlator context object: "
                                             f"{error_message.decode('utf-8').rstrip()}")
        else:
            raise ContextContextNewError(f"Error creating correlator context object: libmwalib.so is not loaded.")

    def display(self):
         """Displays a human readable summary of the correlator context"""
         error_message = create_string_buffer(ERROR_MESSAGE_LEN)

         if mwalib.mwalib_correlator_context_display(self._correlator_context_object,
                                                     error_message,
                                                     ERROR_MESSAGE_LEN) != 0:
             raise ContextCorrelatorContextDisplayError(f"Error calling mwalib_correlator_context_display(): "
                                                        f"{error_message.decode('utf-8').rstrip()}")

    def read_by_baseline(self, timestep_index, coarse_channel_index):
         """Retrieve one HDU (ordered baseline,freq,pol,r,i) as a numpy array."""
         error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN

         float_buffer_type = ct.c_float * self.correlator_metadata.num_timestep_coarse_channel_floats
         buffer = float_buffer_type()

         if mwalib.mwalib_correlator_context_read_by_baseline(self._correlator_context_object,
                                                              ct.c_size_t(timestep_index),
                                                              ct.c_size_t(coarse_channel_index),
                                                              buffer,
                                                              self.correlator_metadata.num_timestep_coarse_channel_floats,
                                                              error_message, ERROR_MESSAGE_LEN) != 0:
             raise ContextCorrelatorContextReadByBaselineException(f"Error reading data: "
                                                  f"{error_message.decode('utf-8').rstrip()}")
         else:
             return npct.as_array(buffer, shape=(self.correlator_metadata.num_timestep_coarse_channel_floats,))

    def read_by_frequency(self, timestep_index, coarse_channel_index):
        """Retrieve one HDU (ordered freq,baseline,pol,r,i) as a numpy array."""
        error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN

        float_buffer_type = ct.c_float * self.correlator_metadata.num_timestep_coarse_channel_floats
        buffer = float_buffer_type()

        if mwalib.mwalib_correlator_context_read_by_frequency(self._correlator_context_object,
                                                              ct.c_size_t(timestep_index),
                                                              ct.c_size_t(coarse_channel_index),
                                                              buffer,
                                                              self.correlator_metadata.num_timestep_coarse_channel_floats,
                                                              error_message, ERROR_MESSAGE_LEN) != 0:
            raise ContextCorrelatorContextReadByFrequencyException(f"Error reading data: "
                                                                   f"{error_message.decode('utf-8').rstrip()}")
        else:
            return npct.as_array(buffer, shape=(self.correlator_metadata.num_timestep_coarse_channel_floats,))
