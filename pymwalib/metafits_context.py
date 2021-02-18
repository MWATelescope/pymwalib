#!/usr/bin/env python
#
# context: main interface for pymwalib for just viewing metafits data (no data files)
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
from pymwalib.common import ERROR_MESSAGE_LEN
from pymwalib.errors import *
from pymwalib.antenna import Antenna
from pymwalib.coarse_channel import CoarseChannel
from pymwalib.metafits_metadata import MetafitsMetadata
from pymwalib.rfinput import RFInput
from pymwalib.timestep import TimeStep


class MetafitsContext:
    """Main class to interface with mwalib"""
    def __init__(self, metafits_filename: str):
        """Take metafits and populate this class via mwalib"""
        self._metafits_context_object = ct.POINTER(CMetafitsContextS)()

        # First populate the context object
        self._get_metafits_context(metafits_filename)

        # Now Get metafits metadata
        self.metafits_metadata = MetafitsMetadata(self._metafits_context_object,None, None)

        # Populate rf_inputs
        self.rfinputs = RFInput.get_rfinputs(self._metafits_context_object, None, None)

        # Populate antennas
        self.antennas = Antenna.get_antennas(self._metafits_context_object, None, None, self.rfinputs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure we free the rust allocated memory in mwalib"""
        if self._metafits_context_object:
            mwalib.mwalib_metafits_context_free(self._metafits_context_object)

    def _get_metafits_context(self, metafits_filename: str):
        """This method will read and validate the metafits and gpubox files. If all has worked, then
        the context object can be used in subsequent calls to populate aspects of this class."""
        if mwalib:
            # Encode all inputs as UTF-8.
            m = ct.c_char_p(metafits_filename.encode("utf-8"))

            error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

            if mwalib.mwalib_metafits_context_new(
                m, ct.byref(self._metafits_context_object), error_message, ERROR_MESSAGE_LEN) != 0:
                raise ContextContextNewError(f"Error creating metafits context object: "
                                             f"{error_message.decode('utf-8').rstrip()}")
        else:
            raise ContextContextNewError(f"Error creating correlator context object: libmwalib.so is not loaded.")

    def display(self):
         """Displays a human readable summary of the metafits context"""
         error_message = create_string_buffer(ERROR_MESSAGE_LEN)

         if mwalib.mwalib_metafits_context_display(self._metafits_context_object,
                                                   error_message,
                                                   ERROR_MESSAGE_LEN) != 0:
             raise ContextMetafitsContextDisplayError(f"Error calling mwalib_metafits_context_display(): "
                                                        f"{error_message.decode('utf-8').rstrip()}")
