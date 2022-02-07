#!/usr/bin/env python
#
# MetafitsContext: main interface for pymwalib for just viewing metafits data (no data files)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import typing
import ctypes as ct
from .mwalib import CMetafitsContextS, mwalib_library, create_string_buffer
from .common import ERROR_MESSAGE_LEN, MWAVersion
from .errors import PymwalibMetafitsContextNewError, PymwalibMetafitsContextDisplayError
from .metafits_metadata import MetafitsMetadata
from .version import check_mwalib_version


class MetafitsContext(MetafitsMetadata):
    """Main class to interface with mwalib metafits infomation"""

    def __init__(self, metafits_filename: str, mwa_version: typing.Optional[MWAVersion] = None):
        """Take metafits and an MWAVersion or None, and populate this class via mwalib"""
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

    def _get_metafits_context(self, metafits_filename: str, mwa_version: typing.Optional[MWAVersion] = None):
        """This method will read and validate the metafits and mwa version"""
        if mwalib_library:
            # Encode all inputs as UTF-8.
            m = ct.c_char_p(metafits_filename.encode("utf-8"))

            # If mwa_version is None, then use alt method, otherwise pass the value for the enum
            error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

            if mwa_version is None:
                if mwalib_library.mwalib_metafits_context_new2(
                        m, ct.byref(self._metafits_context_object), error_message,
                        ERROR_MESSAGE_LEN) != 0:
                    raise PymwalibMetafitsContextNewError(f"Error creating metafits context object: "
                                                          f"{error_message.decode('utf-8').rstrip()}")
            else:
                if mwalib_library.mwalib_metafits_context_new(
                        m, mwa_version.value, ct.byref(self._metafits_context_object), error_message,
                        ERROR_MESSAGE_LEN) != 0:
                    raise PymwalibMetafitsContextNewError(f"Error creating metafits context object: "
                                                          f"{error_message.decode('utf-8').rstrip()}")
        else:
            raise PymwalibMetafitsContextNewError("Error creating metafits context object: mwalib.so is not loaded.")

    def display(self):
        """Displays a human readable summary of the metafits context"""
        error_message = create_string_buffer(ERROR_MESSAGE_LEN)

        if mwalib_library.mwalib_metafits_context_display(self._metafits_context_object,
                                                          error_message,
                                                          ERROR_MESSAGE_LEN) != 0:
            raise PymwalibMetafitsContextDisplayError(f"Error calling mwalib_metafits_context_display(): "
                                                      f"{error_message.decode('utf-8').rstrip()}")

    def get_expected_volt_filename(self, metafits_timestep_index: int, metafits_coarse_chan_index: int) -> str:
        """Displays a human readable summary of the metafits context"""
        error_message = create_string_buffer(ERROR_MESSAGE_LEN)
        filename_len = 64
        filename = create_string_buffer(filename_len)

        if mwalib_library.mwalib_metafits_get_expected_volt_filename(self._metafits_context_object,
                                                                     metafits_timestep_index,
                                                                     metafits_coarse_chan_index,
                                                                     filename,
                                                                     filename_len,
                                                                     error_message,
                                                                     ERROR_MESSAGE_LEN) != 0:
            raise PymwalibMetafitsContextDisplayError(f"Error calling mwalib_metafits_context_display(): "
                                                      f"{error_message.decode('utf-8').rstrip()}")
        return filename.decode('utf-8').strip()

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(\n" \
               f"{super().__repr__()}\n)\n"
