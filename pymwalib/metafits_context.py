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
from .common import ERROR_MESSAGE_LEN, MWAMode, MWAVersion, GeometricDelaysApplied
from .errors import PymwalibMetafitsContextNewError,PymwalibMetafitsContextDisplayError
from .metafits_metadata import MetafitsMetadata
from .version import check_mwalib_version
from datetime import datetime


class MetafitsContext(MetafitsMetadata):
    """Main class to interface with mwalib metafits infomation"""
    def __init__(self, metafits_filename: str, mwa_version: MWAVersion):
        """Take metafits and populate this class via mwalib"""
        #
        # Ensure we have a compatible version of mwalib
        #
        check_mwalib_version()

        self._metafits_context_object = ct.POINTER(CMetafitsContextS)()

        # First populate the context object
        self._get_metafits_context(metafits_filename, mwa_version)

        # Get metafits metadata
        super().__init__(self._metafits_context_object, None, None)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure we free the rust allocated memory in mwalib"""
        if self._metafits_context_object:
            mwalib_library.mwalib_metafits_context_free(self._metafits_context_object)

    def _get_metafits_context(self, metafits_filename: str, mwa_version: MWAVersion):
        """This method will read and validate the metafits and gpubox files. If all has worked, then
        the context object can be used in subsequent calls to populate aspects of this class."""
        if mwalib_library:
            # Encode all inputs as UTF-8.
            m = ct.c_char_p(metafits_filename.encode("utf-8"))

            error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)
            if mwalib_library.mwalib_metafits_context_new(
                m, mwa_version, ct.byref(self._metafits_context_object), error_message, ERROR_MESSAGE_LEN) != 0:
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

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(\n" \
               f"{super().__repr__()}\n)\n"
