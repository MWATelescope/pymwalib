#!/usr/bin/env python
#
# baseline: class representing a single baseline in mwalib
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from .mwalib import CBaselineS, CMetafitsMetadataS


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
    def get_baselines(metafits_metadata: CMetafitsMetadataS) -> []:
        """Retrieve all of the baseline metadata and populate a list of baselines."""
        baselines = []

        for i in range(0, metafits_metadata.num_baselines):
            obj: CBaselineS = metafits_metadata.baselines[i]

            # Populate all the fields
            baselines.append(Baseline(i,
                                      obj.ant1_index,
                                      obj.ant2_index))

        return baselines
