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
from pymwalib.mwalib import create_string_buffer, mwalib, CBaselineS, CMetafitsContextS, CCorrelatorContextS, CVoltageContextS
from pymwalib.common import ERROR_MESSAGE_LEN
from pymwalib.errors import *
import ctypes as ct


class Baseline:
    """
    A class representing a single Baseline

    Attributes
    ----------
    index : int
        Ordinal index of this time step.

    ant1_index : int
        The index in the antenna array for the first member of the baseline

    ant2_index : int
        The index in the antenna array for the second member of the baseline

    """

    def __init__(self,
                 index: int,
                 ant1_index: int,
                 ant2_index: int):
        """Initialise the class"""
        self.index: int = index
        self.ant1_index: int = ant1_index
        self.ant2_index: int = ant2_index

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Order: {self.index}, " \
               f"Antennas: {self.ant1_index} v {self.ant2_index})"

    @staticmethod
    def get_baselines(metafits_context: ct.POINTER(CMetafitsContextS),
                      correlator_context: ct.POINTER(CCorrelatorContextS),
                      voltage_context: ct.POINTER(CVoltageContextS)) -> []:
        """Retrieve all of the baseline metadata and populate a list of baselines."""
        baselines = []
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_array_ptr = ct.POINTER(CBaselineS)()
        c_len_ptr = ct.c_size_t(0)

        if mwalib.mwalib_baselines_get(metafits_context,
                                       correlator_context,
                                       voltage_context,
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
                                          c_array_ptr[i].ant1_index,
                                          c_array_ptr[i].ant2_index))

            # We're now finished with the C memory, so free it
            mwalib.mwalib_baselines_free(c_array_ptr, c_len_ptr.value)

            return baselines