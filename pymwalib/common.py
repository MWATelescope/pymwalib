#!/usr/bin/env python
#
# Common classes and functions
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import enum

ERROR_MESSAGE_LEN = 1024


class MWAVersion(enum.Enum):
    """Enum for MWA version"""
    # MWA correlator(v1.0), having data files without any batch numbers.
    CorrOldLegacy = 1
    # MWA correlator(v1.0), having data files with "gpubox" and batch numbers in their names.
    CorrLegacy = 2
    # MWAX correlator(v2.0)
    CorrMWAXv2 = 3
    # Legacy VCS Recombined
    VCSLegacyRecombined = 4
    # MWAX VCS
    VCSMWAXv2 = 5


class VisPol(enum.Enum):
    """Enum representing the four visibility polarisations for MWA"""
    XX = 1
    XY = 2
    YX = 3
    YY = 4


class GeometricDelaysApplied(enum.Enum):
    """Enum representing the state of Geometric delays applied for this observation"""
    No = 0
    Zenith = 1
    TilePointing = 2
    AzElTracking = 3


class MWAMode(enum.Enum):
    """Enum representing the correlator mode"""
    No_Capture = 0
    Burst_Vsib = 1
    Sw_Cor_Vsib = 2
    Hw_Cor_Pkts = 3
    Rts_32t = 4
    Hw_Lfiles = 5
    Hw_Lfiles_Nomentok = 6
    Sw_Cor_Vsib_Nomentok = 7
    Burst_Vsib_Synced = 8
    Burst_Vsib_Raw = 9
    Lfiles_Client = 16
    No_Capture_Burst = 17
    Enter_Burst = 18
    Enter_Channel = 19
    Voltage_Raw = 20
    Corr_Mode_Change = 21
    Voltage_Start = 22
    Voltage_Stop = 23
    Voltage_Buffer = 24
    Mwax_Correlator = 30
    Mwax_Vcs = 31
