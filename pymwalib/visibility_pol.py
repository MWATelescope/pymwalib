#!/usr/bin/env python
#
# visibility_pol: class representing a single visibility_pol in mwalib
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
from pymwalib.mwalib import create_string_buffer, mwalib, CVisibilityPolS, CCorrelatorContextS
from pymwalib.common import ERROR_MESSAGE_LEN
from pymwalib.errors import *
import ctypes as ct


class VisibilityPol:
    """
    A class representing a single mwalibVisibilityPol

    Attributes
    ----------
    index : int
        Ordinal index of this visibility pol.

    polarisation : str
        The polarisation of this object- e.g. "XX", "XY", "YX" or "YY"

    """

    def __init__(self,
                 index: int,
                 polarisation: str):
        """Initialise the class"""
        self.index: int = index
        self.polarisation: str = polarisation

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Order: {self.index}, " \
               f"UNIX time: {self.polarisation})"

    @staticmethod
    def get_visibility_pols(correlator_context: ct.POINTER(CCorrelatorContextS)) -> []:
        """Retrieve all of the visibility_pol metadata and populate a list of visibility_pols."""
        visibility_pols = []
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_array_ptr = ct.POINTER(CVisibilityPolS)()
        c_len_ptr = ct.c_size_t(0)

        if mwalib.mwalib_correlator_visibility_pols_get(correlator_context,
                                                        ct.byref(c_array_ptr),
                                                        ct.byref(c_len_ptr),
                                                        error_message,
                                                        ERROR_MESSAGE_LEN) != 0:
            # Error
            raise ContextCorrelatorVisibilityPolsGetError(f"Error getting visibility_pol object: "
                                                          f"{error_message.decode('utf-8').rstrip()}")
        else:
            for i in range(0, c_len_ptr.value):
                # Populate all the fields
                visibility_pols.append(VisibilityPol(i, c_array_ptr[i].polarisation.decode("utf-8")))

            # We're now finished with the C memory, so free it
            mwalib.mwalib_visibility_pols_free(c_array_ptr, c_len_ptr.value)

            return visibility_pols