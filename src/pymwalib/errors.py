#!/usr/bin/env python
#
# Error types for pymwalib
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

class PymwalibError(Exception):
    """Base class for other exceptions"""
    pass


class PymwalibMwalibVersionNotCompatibleError(PymwalibError):
    """Raised when mwalib is not a compatible version"""
    pass


class PymwalibMetafitsContextNewError(PymwalibError):
    """Raised when call to C mwalib_metafits_context_new fails"""
    pass


class PymwalibCorrelatorContextNewError(PymwalibError):
    """Raised when call to C mwalib_correaltor_context_new fails"""
    pass


class PymwalibVoltageContextNewError(PymwalibError):
    """Raised when call to C mwalib_voltage_context_new fails"""
    pass


class PymwalibAntennasGetError(PymwalibError):
    """Raised when call to C mwalib_antennas_get fails"""
    pass


class PymwalibBaselinesGetError(PymwalibError):
    """Raised when call to C mwalib_baselines_get fails"""
    pass


class PymwalibCoarseChannelsGetError(PymwalibError):
    """Raised when call to C mwalib_coarse_channels_get fails"""
    pass


class PymwalibMetafitsMetadataGetError(PymwalibError):
    """Raised when call to C mwalib_metafits_metadata_get fails"""
    pass


class PymwalibCorrelatorMetadataGetError(PymwalibError):
    """Raised when call to C mwalib_correlator_metadata_get fails"""
    pass


class PymwalibVoltageMetadataGetError(PymwalibError):
    """Raised when call to C mwalib_voltage_metadata_get fails"""
    pass


class PymwalibRFInputsGetError(PymwalibError):
    """Raised when call to C mwalib_rfinputs_get fails"""
    pass


class PymwalibTimeStepsGetError(PymwalibError):
    """Raised when call to C mwalib_timesteps_get fails"""
    pass


class PymwalibMetafitsContextDisplayError(PymwalibError):
    """Raised when call to C mwalib_metafits_context_display fails"""
    pass


class PymwalibMetafitsContextGetExpectedVoltageFilename(PymwalibError):
    """Raised when call to C mwalib_metafits_get_expected_volt_filename fails"""
    pass


class PymwalibCorrelatorContextDisplayError(PymwalibError):
    """Raised when call to C mwalib_correlator_context_display fails"""
    pass


class PymwalibCorrelatorContextGetFineChanFreqsArrayError(PymwalibError):
    """Raised when call to C mwalib_correlator_context_get_fine_chan_freqs_hz_array fails"""
    pass


class PymwalibVoltageContextDisplayError(PymwalibError):
    """Raised when call to C mwalib_voltage_context_display fails"""
    pass


class PymwalibVoltageContextReadFileError(PymwalibError):
    """Raised when call to C mwalib_voltage_context_read_file fails"""
    pass


class PymwalibVoltageContextReadSecondError(PymwalibError):
    """Raised when call to C mwalib_voltage_context_read_second fails"""
    pass


class PymwalibVoltageContextGetFineChanFreqsArrayError(PymwalibError):
    """Raised when call to C mwalib_voltage_context_get_fine_chan_freqs_hz_array fails"""
    pass


class PymwalibCorrelatorContextReadByBaselineError(PymwalibError):
    """Raised when call to C mwalib_correlator_context_read_by_baseline fails"""
    pass


class PymwalibCorrelatorContextReadByFrequencyError(PymwalibError):
    """Raised when call to C mwalib_correlator_context_read_by_frequency fails"""
    pass


class PymwalibNoDataForTimestepAndCoarseChannelError(PymwalibError):
    """Raised when call to C mwalib functions that read data ask for data at a timestep/coarse channel where
    there is no data"""
    pass
