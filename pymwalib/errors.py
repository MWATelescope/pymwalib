#!/usr/bin/env python
#
# Error types for pymwalib
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

class ContextError(Exception):
    """Base class for other exceptions"""
    pass


class ContextContextNewError(ContextError):
    """Raised when call to C mwalibContext_get fails"""
    pass


class ContextAntennasGetError(ContextError):
    """Raised when call to C mwalib_antennas_get fails"""
    pass


class ContextCorrelatorBaselinesGetError(ContextError):
    """Raised when call to C mwalib_correlator_baselines_get fails"""
    pass


class ContextCorrelatorCoarseChannelsGetError(ContextError):
    """Raised when call to C mwalib_correlator_coarse_channels_get fails"""
    pass

class ContextVoltageCoarseChannelsGetError(ContextError):
    """Raised when call to C mwalib_voltage_coarse_channels_get fails"""
    pass

class ContextCoarseChannelsGetError(ContextError):
    """Raised when no context is provided"""
    pass

class ContextMetafitsMetadataGetError(ContextError):
    """Raised when call to C mwalib_metafits_metadata_get fails"""
    pass

class ContextCorrelatorMetadataGetError(ContextError):
    """Raised when call to C mwalib_correlator_metadata_get fails"""
    pass

class ContextVoltageMetadataGetError(ContextError):
    """Raised when call to C mwalib_voltage_metadata_get fails"""
    pass

class ContextRFInputsGetError(ContextError):
    """Raised when call to C mwalib_rfinputs_get fails"""
    pass

class ContextCorrelatorTimeStepsGetError(ContextError):
    """Raised when call to C mwalib_correlator_timesteps_get fails"""
    pass

class ContextVoltageTimeStepsGetError(ContextError):
    """Raised when call to C mwalib_voltage_timesteps_get fails"""
    pass

class ContextTimeStepsGetError(ContextError):
    """Raised when no context is provided"""
    pass

class ContextCorrelatorVisibilityPolsGetError(ContextError):
    """Raised when call to C mwalib_correlator_visibility_pols_get fails"""
    pass

class ContextMetafitsContextDisplayError(ContextError):
    """Raised when call to C mwalib_metafits_context_display fails"""
    pass

class ContextCorrelatorContextDisplayError(ContextError):
    """Raised when call to C mwalib_correlator_context_display fails"""
    pass

class ContextVoltageContextDisplayError(ContextError):
    """Raised when call to C mwalib_voltage_context_display fails"""
    pass

class ContextVoltageContextReadFileException(ContextError):
    """Raised when call to C mwalib_voltage_context_read_file fails"""
    pass

class ContextVoltageContextReadSecondException(ContextError):
    """Raised when call to C mwalib_voltage_context_read_second fails"""
    pass

class ContextCorrelatorContextReadByBaselineException(ContextError):
    """Raised when call to C mwalibContext_read_by_baseline fails"""
    pass

class ContextCorrelatorContextReadByFrequencyException(ContextError):
    """Raised when call to C mwalibContext_read_by_frequency fails"""
    pass