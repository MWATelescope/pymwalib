#!/usr/bin/env python
#
# coarse_channel: class representing a single coarse_channel in mwalib
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from .mwalib import CCoarseChannelS, CMetafitsMetadataS


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
    def get_metafits_coarse_channels(metafits_metadata: CMetafitsMetadataS) -> []:
        """Retrieve all of the coarse_channel metadata and populate a list of coarse_channels."""
        coarse_channels = []

        for i in range(0, metafits_metadata.num_metafits_coarse_chans):
            obj: CCoarseChannelS = metafits_metadata.metafits_coarse_chans[i]

            # Populate all the fields
            coarse_channels.append(CoarseChannel(i,
                                                 obj.corr_chan_number,
                                                 obj.rec_chan_number,
                                                 obj.gpubox_number,
                                                 obj.chan_width_hz,
                                                 obj.chan_start_hz,
                                                 obj.chan_centre_hz,
                                                 obj.chan_end_hz, ))

        return coarse_channels

    @staticmethod
    def get_correlator_or_voltage_coarse_channels(correlator_or_voltage_metadata) -> []:
        """Retrieve all of the coarse_channel metadata and populate a list of coarse_channels."""
        coarse_channels = []

        for i in range(0, correlator_or_voltage_metadata.num_coarse_chans):
            obj: CCoarseChannelS = correlator_or_voltage_metadata.coarse_chans[i]

            # Populate all the fields
            coarse_channels.append(CoarseChannel(i,
                                                 obj.corr_chan_number,
                                                 obj.rec_chan_number,
                                                 obj.gpubox_number,
                                                 obj.chan_width_hz,
                                                 obj.chan_start_hz,
                                                 obj.chan_centre_hz,
                                                 obj.chan_end_hz, ))

        return coarse_channels
