#!/usr/bin/env python
#
# VoltageContext: main interface for pymwalib for voltage data
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import numpy.ctypeslib as npct
from .mwalib import CVoltageContextS,ct,mwalib_library,create_string_buffer,MWALIB_SUCCESS,MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN
from .common import ERROR_MESSAGE_LEN
from .errors import PymwalibVoltageContextNewError,PymwalibCorrelatorContextDisplayError,PymwalibNoDataForTimestepAndCoarseChannel,PymwalibVoltageContextReadFileException,PymwalibVoltageContextReadSecondException
from .antenna import Antenna
from .coarse_channel import CoarseChannel
from .metafits_metadata import MetafitsMetadata
from .voltage_metadata import VoltageMetadata
from .rfinput import RFInput
from .timestep import TimeStep
from .version import check_mwalib_version


class VoltageContext:
    """Main class to interface with mwalib"""
    def __init__(self, metafits_filename: str, voltage_filenames: list):
        """Take metafits and voltage files, and populate this class via mwalib"""
        #
        # Ensure we have a compatible version of mwalib
        #
        check_mwalib_version()

        self._voltage_context_object = ct.POINTER(CVoltageContextS)()

        # First populate the context object
        self._get_voltage_context(metafits_filename, voltage_filenames)

        # Now Get metafits metadata
        self.metafits_metadata = MetafitsMetadata(None, None, self._voltage_context_object)

        # Now Get correlator metadata
        self.voltage_metadata = VoltageMetadata(self._voltage_context_object)

        # Populate rf_inputs
        self.rfinputs = RFInput.get_rfinputs(None, None, self._voltage_context_object)

        # Populate antennas
        self.ants = Antenna.get_antennas(None, None, self._voltage_context_object, self.rfinputs)

        # Populate coarse channels
        self.coarse_channels = CoarseChannel.get_coarse_channels(None, self._voltage_context_object)

        # Populate timesteps
        self.timesteps = TimeStep.get_timesteps(None, self._voltage_context_object)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure we free the rust allocated memory in mwalib"""
        if self._voltage_context_object:
            mwalib_library.mwalib_voltage_context_free(self._voltage_context_object)

    def _get_voltage_context(self, metafits_filename: str, voltage_filenames: list):
        """This method will read and validate the metafits and voltage files. If all has worked, then
        the context object can be used in subsequent calls to populate aspects of this class."""
        if mwalib_library:
            # Encode all inputs as UTF-8.
            m = ct.c_char_p(metafits_filename.encode("utf-8"))

            # https://stackoverflow.com/questions/4145775/how-do-i-convert-a-python-list-into-a-c-array-by-using-ctypes
            encoded = []
            for v in voltage_filenames:
                encoded.append(ct.c_char_p(v.encode("utf-8")))
            seq = ct.c_char_p * len(encoded)
            g = seq(*encoded)
            error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

            if mwalib_library.mwalib_voltage_context_new(
                m, g, len(encoded), ct.byref(self._voltage_context_object), error_message, ERROR_MESSAGE_LEN) != 0:
                raise PymwalibVoltageContextNewError(f"Error creating voltage context object: "
                                             f"{error_message.decode('utf-8').rstrip()}")
        else:
            raise PymwalibVoltageContextNewError(f"Error creating voltage context object: mwalib is not loaded.")

    def display(self):
         """Displays a human readable summary of the voltage context"""
         error_message = create_string_buffer(ERROR_MESSAGE_LEN)

         if mwalib_library.mwalib_voltage_context_display(self._voltage_context_object,
                                                  error_message,
                                                  ERROR_MESSAGE_LEN) != 0:
             raise PymwalibCorrelatorContextDisplayError(f"Error calling mwalib_voltage_context_display(): "
                                                        f"{error_message.decode('utf-8').rstrip()}")

    def read_file(self, timestep_index: int, coarse_chan_index: int):
         """Retrieve one file of VCS data as a numpy array."""
         error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN

         byte_buffer_len = self.voltage_metadata.voltage_block_size_bytes * \
                           self.voltage_metadata.num_voltage_blocks_per_timestep

         byte_buffer_type = ct.c_byte * byte_buffer_len
         buffer = byte_buffer_type()

         ret_val = mwalib_library.mwalib_voltage_context_read_file(self._voltage_context_object,
                                                    ct.c_size_t(timestep_index),
                                                    ct.c_size_t(coarse_chan_index),
                                                    buffer,
                                                    byte_buffer_len,
                                                    error_message, ERROR_MESSAGE_LEN)

         if ret_val == MWALIB_SUCCESS:
             return npct.as_array(buffer, shape=(byte_buffer_len,))
         elif ret_val == MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN:
             raise PymwalibNoDataForTimestepAndCoarseChannel(f"No data exists for this timestep {timestep_index} and coarse channel {coarse_chan_index}")
         else:
             raise PymwalibVoltageContextReadFileException(f"Error reading data: "
                                                         f"{error_message.decode('utf-8').rstrip()}")


    def read_second(self, gps_second_start: int , gps_second_count: int, coarse_chan_index: int):
         """Retrieve multiple seconds of VCS data as a numpy array."""
         error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN

         byte_buffer_len = self.voltage_metadata.voltage_block_size_bytes * \
                           self.voltage_metadata.num_voltage_blocks_per_timestep

         byte_buffer_type = ct.c_byte * byte_buffer_len
         buffer = byte_buffer_type()

         ret_val = mwalib_library.mwalib_voltage_context_read_second(self._voltage_context_object,
                                                      ct.c_ulong(gps_second_start),
                                                      ct.c_size_t(gps_second_count),
                                                      ct.c_size_t(coarse_chan_index),
                                                      buffer,
                                                      byte_buffer_len,
                                                      error_message, ERROR_MESSAGE_LEN)

         if ret_val == MWALIB_SUCCESS:
             return npct.as_array(buffer, shape=(byte_buffer_len,))
         elif ret_val == MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN:
             raise PymwalibNoDataForTimestepAndCoarseChannel(f"Not all data exists for {gps_second_start} (for {gps_second_count} sec) and coarse channel {coarse_chan_index}")
         else:
             raise PymwalibVoltageContextReadSecondException(f"Error reading data: "
                                                             f"{error_message.decode('utf-8').rstrip()}")
