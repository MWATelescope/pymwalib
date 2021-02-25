#!/usr/bin/env python
#
# coarse_channel: class representing a single coarse_channel in mwalib
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
from pymwalib.mwalib import create_string_buffer, mwalib, CCoarseChannelS, CCorrelatorContextS, CVoltageContextS
from pymwalib.common import ERROR_MESSAGE_LEN
from pymwalib.errors import *
import ctypes as ct


class CoarseChannel:
    """
    A class representing a single CoarseChannel

    Attributes
    ----------
    index : int
        Ordinal index of this coarse channel.

    Please see https://github.com/MWATelescope/mwalib/blob/master/src/coarse_channel.rs for remaining attributes

    """

    def __init__(self,
                 index: int,
                 corr_chan_number: int,
                 rec_chan_number: int,
                 gpubox_number: int,
                 chan_width_hz: int,
                 chan_start_hz: int,
                 chan_centre_hz: int,
                 chan_end_hz: int):
        """Initialise the class"""
        self.index: int = index
        self.corr_chan_number: int = corr_chan_number
        self.rec_chan_number: int = rec_chan_number
        self.gpubox_number: int = gpubox_number
        self.chan_width_hz: int = chan_width_hz
        self.chan_start_hz: int = chan_start_hz
        self.chan_centre_hz: int = chan_centre_hz
        self.chan_end_hz: int = chan_end_hz

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Order: {self.index}, " \
               f"Correlator channel number: {self.corr_chan_number}, " \
               f"Receiver channel number: {self.rec_chan_number}, " \
               f"GPUBox Number: {self.gpubox_number}, " \
               f"Channel width MHz: {float(self.chan_width_hz) / 1000000.}, " \
               f"Channel start MHz: {float(self.chan_start_hz) / 1000000.}, " \
               f"Channel centre MHz: {float(self.chan_centre_hz) / 1000000.}, " \
               f"Channel end MHz: {float(self.chan_end_hz) / 1000000.})"

    @staticmethod
    def get_coarse_channels(correlator_context: ct.POINTER(CCorrelatorContextS),
                            voltage_context: ct.POINTER(CVoltageContextS)) -> []:
        """Retrieve all of the coarse_channel metadata and populate a list of coarse_channels."""
        coarse_channels = []
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_array_ptr = ct.POINTER(CCoarseChannelS)()
        c_len_ptr = ct.c_size_t(0)

        if correlator_context is not None:
            if mwalib.mwalib_correlator_coarse_channels_get(correlator_context,
                                                      ct.byref(c_array_ptr),
                                                      ct.byref(c_len_ptr),
                                                      error_message,
                                                      ERROR_MESSAGE_LEN) != 0:
                # Error
                raise ContextCorrelatorCoarseChannelsGetError(f"Error getting coarse_channel object: "
                                                              f"{error_message.decode('utf-8').rstrip()}")
        elif voltage_context is not None:
             if mwalib.mwalib_voltage_coarse_channels_get(correlator_context,
                                                       ct.byref(c_array_ptr),
                                                       ct.byref(c_len_ptr),
                                                       error_message,
                                                       ERROR_MESSAGE_LEN) != 0:
                # Error
                raise ContextVoltageCoarseChannelsGetError(f"Error getting coarse_channel object: "
                                                           f"{error_message.decode('utf-8').rstrip()}")
        else:
            raise ContextCoarseChannelsGetError(f"Error getting coarse_channel object: "
                                                f"neither correlator nor voltage context provided.")

        for i in range(0, c_len_ptr.value):
            # Populate all the fields
            coarse_channels.append(CoarseChannel(i,
                                                 c_array_ptr[i].corr_chan_number,
                                                 c_array_ptr[i].rec_chan_number,
                                                 c_array_ptr[i].gpubox_number,
                                                 c_array_ptr[i].chan_width_hz,
                                                 c_array_ptr[i].chan_start_hz,
                                                 c_array_ptr[i].chan_centre_hz,
                                                 c_array_ptr[i].chan_end_hz,))

        # We're now finished with the C memory, so free it
        mwalib.mwalib_coarse_channels_free(c_array_ptr, c_len_ptr.value)

        return coarse_channels