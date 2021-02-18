#!/usr/bin/env python
#
# baseline: class representing a single baseline in mwalib
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
from pymwalib.mwalib import create_string_buffer, mwalib, CBaselineS, CCorrelatorContextS
from pymwalib.common import ERROR_MESSAGE_LEN
from pymwalib.errors import *
import ctypes as ct


class Baseline:
    """
    A class representing a single mwalibBaseline

    Attributes
    ----------
    index : int
        Ordinal index of this time step.

    antenna_index1 : int
        The index in the antenna array for the first member of the baseline

    antenna_index2 : int
        The index in the antenna array for the second member of the baseline

    """

    def __init__(self,
                 index: int,
                 antenna1_index: int,
                 antenna2_index: int):
        """Initialise the class"""
        self.index: int = index
        self.antenna1_index: int = antenna1_index
        self.antenna2_index: int = antenna2_index

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Order: {self.index}, " \
               f"Antennas: {self.antenna1_index} v {self.antenna2_index})"

    @staticmethod
    def get_baselines(correlator_context: ct.POINTER(CCorrelatorContextS)) -> []:
        """Retrieve all of the baseline metadata and populate a list of baselines."""
        baselines = []
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_array_ptr = ct.POINTER(CBaselineS)()
        c_len_ptr = ct.c_size_t(0)

        if mwalib.mwalib_correlator_baselines_get(correlator_context,
                                                  ct.byref(c_array_ptr),
                                                  ct.byref(c_len_ptr),
                                                  error_message,
                                                  ERROR_MESSAGE_LEN) != 0:
            # Error
            raise ContextCorrelatorBaselinesGetError(f"Error getting baseline object: "
                                                     f"{error_message.decode('utf-8').rstrip()}")
        else:
            for i in range(0, c_len_ptr.value):
                # Populate all the fields
                baselines.append(Baseline(i,
                                          c_array_ptr[i].antenna1_index,
                                          c_array_ptr[i].antenna2_index))

            # We're now finished with the C memory, so free it
            mwalib.mwalib_baselines_free(c_array_ptr, c_len_ptr.value)

            return baselines