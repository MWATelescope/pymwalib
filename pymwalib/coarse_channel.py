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


class CoarseChannel:
    """
    A class representing a single mwalibCoarseChannel

    Attributes
    ----------
    index : int
        Ordinal index of this coarse channel.

    Please see https://github.com/MWATelescope/mwalib/blob/master/src/coarse_channel.rs for remaining attributes

    """

    def __init__(self,
                 index: int,
                 correlator_channel_number: int,
                 receiver_channel_number: int,
                 gpubox_number: int,
                 channel_width_hz: int,
                 channel_start_hz: int,
                 channel_centre_hz: int,
                 channel_end_hz: int):
        """Initialise the class"""
        self.index: int = index
        self.correlator_channel_number: int = correlator_channel_number
        self.receiver_channel_number: int = receiver_channel_number
        self.gpubox_number: int = gpubox_number
        self.channel_width_hz: int = channel_width_hz
        self.channel_start_hz: int = channel_start_hz
        self.channel_centre_hz: int = channel_centre_hz
        self.channel_end_hz: int = channel_end_hz

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Order: {self.index}, " \
               f"Correlator channel number: {self.correlator_channel_number}, " \
               f"Receiver channel number: {self.receiver_channel_number}, " \
               f"GPUBox Number: {self.gpubox_number}, " \
               f"Channel width MHz: {float(self.channel_width_hz) / 1000000.}, " \
               f"Channel start MHz: {float(self.channel_start_hz) / 1000000.}, " \
               f"Channel centre MHz: {float(self.channel_centre_hz) / 1000000.}, " \
               f"Channel end MHz: {float(self.channel_end_hz) / 1000000.})"
