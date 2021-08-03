#!/usr/bin/env python
#
# timestep: class representing a single timestep in mwalib
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from .mwalib import CTimeStepS, CMetafitsMetadataS


class TimeStep:
    """
    A class representing a single TimeStep

    Attributes
    ----------
    index : int
        Ordinal index of this time step.

    unix_time_ms : int
        The UNIX time (in milliseconds) of the start of this time step

    gps_time_ms : int
        The GPS time (in milliseconds) of the start of this time step

    """

    def __init__(self,
                 index: int,
                 unix_time_ms: int,
                 gps_time_ms: int):
        """Initialise the class"""
        self.index: int = index
        self.unix_time_ms: int = unix_time_ms
        self.gps_time_ms: int = gps_time_ms

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Order: {self.index}, " \
               f"UNIX time: {float(self.unix_time_ms) / 1000.}, " \
               f"GPS time: {float(self.gps_time_ms) / 1000.})"

    @staticmethod
    def get_metafits_timesteps(metafits_metadata: CMetafitsMetadataS) -> []:
        """Retrieve all of the metafits timestep metadata and populate a list of metafits timesteps."""
        timesteps = []

        for i in range(0, metafits_metadata.num_metafits_timesteps):
            obj: CTimeStepS = metafits_metadata.metafits_timesteps[i]

            # Populate all the fields
            timesteps.append(TimeStep(i,
                                      obj.unix_time_ms,
                                      obj.gps_time_ms))

        return timesteps

    @staticmethod
    def get_correlator_or_voltage_timesteps(correlator_or_voltage_metadata) -> []:
        """Retrieve all of the timestep metadata and populate a list of timesteps."""
        timesteps = []

        for i in range(0, correlator_or_voltage_metadata.num_timesteps):
            obj: CTimeStepS = correlator_or_voltage_metadata.timesteps[i]

            # Populate all the fields
            timesteps.append(TimeStep(i,
                                      obj.unix_time_ms,
                                      obj.gps_time_ms))

        return timesteps
