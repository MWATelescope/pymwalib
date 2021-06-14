#!/usr/bin/env python
#
# MetafitsContext: main interface for pymwalib for just viewing metafits data (no data files)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import ctypes as ct
from .mwalib import CMetafitsContextS,mwalib_library,create_string_buffer
from .common import ERROR_MESSAGE_LEN
from .errors import PymwalibMetafitsContextNewError,PymwalibMetafitsContextDisplayError
from .antenna import Antenna
from .baseline import Baseline
from .metafits_metadata import MetafitsMetadata
from .rfinput import RFInput
from .coarse_channel import CoarseChannel
from .timestep import TimeStep
from .version import check_mwalib_version


class MetafitsContext:
    """Main class to interface with mwalib metafits infomation"""
    def __init__(self, metafits_filename: str):
        """Take metafits and populate this class via mwalib"""
        #
        # Ensure we have a compatible version of mwalib
        #
        check_mwalib_version()

        self._metafits_context_object = ct.POINTER(CMetafitsContextS)()

        # First populate the context object
        self._get_metafits_context(metafits_filename)

        # Now Get metafits metadata
        self.metafits_metadata = MetafitsMetadata(self._metafits_context_object,None, None)

        # Populate rf_inputs
        self.rfinputs = RFInput.get_rfinputs(self._metafits_context_object, None, None)

        # Populate antennas
        self.ants = Antenna.get_antennas(self._metafits_context_object, None, None, self.rfinputs)

        # Populate baselines
        self.baselines = Baseline.get_baselines(self._metafits_context_object, None, None)

        # Populate timesteps
        self.metafits_timesteps = TimeStep.get_metafits_timesteps(self._metafits_context_object,None, None)

        # Populate coarse channels
        self.metafits_coarse_chans = CoarseChannel.get_metafits_coarse_channels(self._metafits_context_object, None, None)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure we free the rust allocated memory in mwalib"""
        if self._metafits_context_object:
            mwalib_library.mwalib_metafits_context_free(self._metafits_context_object)

    def _get_metafits_context(self, metafits_filename: str):
        """This method will read and validate the metafits and gpubox files. If all has worked, then
        the context object can be used in subsequent calls to populate aspects of this class."""
        if mwalib_library:
            # Encode all inputs as UTF-8.
            m = ct.c_char_p(metafits_filename.encode("utf-8"))

            error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

            if mwalib_library.mwalib_metafits_context_new(
                m, ct.byref(self._metafits_context_object), error_message, ERROR_MESSAGE_LEN) != 0:
                raise PymwalibMetafitsContextNewError(f"Error creating metafits context object: "
                                             f"{error_message.decode('utf-8').rstrip()}")
        else:
            raise PymwalibMetafitsContextNewError(f"Error creating metafits context object: mwalib.so is not loaded.")

    def display(self):
         """Displays a human readable summary of the metafits context"""
         error_message = create_string_buffer(ERROR_MESSAGE_LEN)

         if mwalib_library.mwalib_metafits_context_display(self._metafits_context_object,
                                                   error_message,
                                                   ERROR_MESSAGE_LEN) != 0:
             raise PymwalibMetafitsContextDisplayError(f"Error calling mwalib_metafits_context_display(): "
                                                        f"{error_message.decode('utf-8').rstrip()}")
