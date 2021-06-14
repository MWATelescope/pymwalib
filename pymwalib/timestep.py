#!/usr/bin/env python
#
# timestep: class representing a single timestep in mwalib
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import ctypes as ct
from .mwalib import create_string_buffer, mwalib_library, CTimeStepS, CMetafitsContextS, CCorrelatorContextS, CVoltageContextS
from .common import ERROR_MESSAGE_LEN
from .errors import PymwalibTimeStepsGetError


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
    def get_metafits_timesteps(metafits_context: ct.POINTER(CMetafitsContextS),
                               correlator_context: ct.POINTER(CCorrelatorContextS),
                               voltage_context: ct.POINTER(CVoltageContextS)) -> []:
        """Retrieve all of the metafits timestep metadata and populate a list of metafits timesteps."""
        timesteps = []
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_array_ptr = ct.POINTER(CTimeStepS)()
        c_len_ptr = ct.c_size_t(0)

        if metafits_context is not None or correlator_context is not None or voltage_context is not None:
            if mwalib_library.mwalib_metafits_timesteps_get(metafits_context,
                                                    correlator_context,
                                                    voltage_context,
                                                    ct.byref(c_array_ptr),
                                                    ct.byref(c_len_ptr),
                                                    error_message,
                                                    ERROR_MESSAGE_LEN) != 0:
                # Error
                raise PymwalibTimeStepsGetError(f"Error getting metafits timestep object: "
                                                f"{error_message.decode('utf-8').rstrip()}")
        else:
            raise PymwalibTimeStepsGetError(f"Error getting metafits timestep object: "
                                            f"neither metafits nor correlator nor voltage context provided.")

        for i in range(0, c_len_ptr.value):
            # Populate all the fields
            timesteps.append(TimeStep(i,
                                      c_array_ptr[i].unix_time_ms,
                                      c_array_ptr[i].gps_time_ms))

        # We're now finished with the C memory, so free it
        mwalib_library.mwalib_timesteps_free(c_array_ptr, c_len_ptr.value)

        return timesteps

    @staticmethod
    def get_timesteps(correlator_context: ct.POINTER(CCorrelatorContextS),
                      voltage_context: ct.POINTER(CVoltageContextS)) -> []:
        """Retrieve all of the timestep metadata and populate a list of timesteps."""
        timesteps = []
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_array_ptr = ct.POINTER(CTimeStepS)()
        c_len_ptr = ct.c_size_t(0)

        if correlator_context is not None or voltage_context is not None:
            if mwalib_library.mwalib_timesteps_get(correlator_context,
                                           voltage_context,
                                           ct.byref(c_array_ptr),
                                           ct.byref(c_len_ptr),
                                           error_message,
                                           ERROR_MESSAGE_LEN) != 0:
                # Error
                raise PymwalibTimeStepsGetError(f"Error getting timestep object: "
                                               f"{error_message.decode('utf-8').rstrip()}")
        else:
            raise PymwalibTimeStepsGetError(f"Error getting timestep object: "
                                           f"neither correlator nor voltage context provided.")

        for i in range(0, c_len_ptr.value):
            # Populate all the fields
            timesteps.append(TimeStep(i,
                                      c_array_ptr[i].unix_time_ms,
                                      c_array_ptr[i].gps_time_ms))

        # We're now finished with the C memory, so free it
        mwalib_library.mwalib_timesteps_free(c_array_ptr, c_len_ptr.value)

        return timesteps