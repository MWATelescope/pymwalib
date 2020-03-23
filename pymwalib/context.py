#!/usr/bin/env python
#
# context: main interface for pymwalib
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
import enum
import numpy.ctypeslib as npct
from pymwalib.mwalib import *
from pymwalib.antenna import Antenna
from pymwalib.coarse_channel import CoarseChannel
from pymwalib.rfinput import RFInput
from pymwalib.timestep import TimeStep


ERROR_MESSAGE_LEN = 1024


class ContextError(Exception):
    """Base class for other exceptions"""
    pass


class ContextGetContextError(ContextError):
    """Raised when call to C mwalibContext_get fails"""
    pass


class ContextGetAntennaError(ContextError):
    """Raised when call to C mwalibAntenna_get fails"""
    pass


class ContextGetCoarseChannelError(ContextError):
    """Raised when call to C mwalibCoarseChannel_get fails"""
    pass


class ContextGetMetadataError(ContextError):
    """Raised when call to C mwalibMetadata_get fails"""
    pass


class ContextGetRFInputError(ContextError):
    """Raised when call to C mwalibRFInput_get fails"""
    pass


class ContextGetTimeStepError(ContextError):
    """Raised when call to C mwalibTimeStep_get fails"""
    pass


class ContextDisplayError(ContextError):
    """Raised when call to C mwalibContext_display fails"""
    pass


class ContextReadByBaselineException(ContextError):
    """Raised when call to C mwalibContext_read_by_baseline fails"""
    pass


class ContextReadByFrequencyException(ContextError):
    """Raised when call to C mwalibContext_read_by_frequency fails"""
    pass


class CorrelatorVersion(enum.Enum):
    """Enum for Correlator version"""
    # MWAX correlator(v2)
    V2 = 0
    # MWA Legacy correlator(v1), having data files with "gpubox" and batch numbers in their names.
    Legacy = 1
    # MWA Old Legacy correlator(v1), having data files without any batch numbers.
    OldLegacy = 2


class Context:
    """Main class to interface with mwalib"""
    def __init__(self, metafits_filename: str, gpubox_filenames: list):
        """Take metafits and gpubox files, and populate this class via mwalib"""
        # First populate the context object
        self._get_context(metafits_filename, gpubox_filenames)

        # Second populate the metadata object
        self._get_metadata()

        # Populate timesteps
        self._get_timesteps()

        # Populate rf_inputs
        self._get_rf_inputs()

        # Populate antennas
        self._get_antennas()

        # Populate coarse channels
        self._get_coarse_channels()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure we free the rust allocated memory in mwalib"""
        if self._context_object:
            mwalib.mwalibContext_free(self._context_object)

    def _get_context(self, metafits_filename: str, gpubox_filenames: list):
        """This method will read and validate the metafits and gpubox files. If all has worked, then
        the context object can be used in subsequent calls to populate aspects of this class."""
        # Encode all inputs as UTF-8.
        m = ct.c_char_p(metafits_filename.encode("utf-8"))

        # https://stackoverflow.com/questions/4145775/how-do-i-convert-a-python-list-into-a-c-array-by-using-ctypes
        encoded = []
        for g in gpubox_filenames:
            encoded.append(ct.c_char_p(g.encode("utf-8")))
        seq = ct.c_char_p * len(encoded)
        g = seq(*encoded)
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)
        self._context_object = mwalib.mwalibContext_get(
            m, g, len(encoded), error_message, ERROR_MESSAGE_LEN)

        if not self._context_object:
            raise ContextGetContextError(f"Error creating context object: {error_message.decode('utf-8').rstrip()}")

    def _get_metadata(self):
        """Retrieve all of the context metadata and populate this class."""
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_object = CmwalibMetadata.from_address(
                                        mwalib.mwalibMetadata_get(self._context_object,
                                        error_message,
                                        ERROR_MESSAGE_LEN))

        if not c_object:
            raise ContextGetMetadataError(f"Error creating metadata object: {error_message.decode('utf-8').rstrip()}")
        else:
            # Populate all the fields
            self.obsid: int = c_object.obsid
            self.corr_version: CorrelatorVersion = c_object.corr_version
            self.mwa_latitude_radians: float = c_object.mwa_latitude_radians
            self.mwa_longitude_radians: float = c_object.mwa_longitude_radians
            self.mwa_altitude_metres: float = c_object.mwa_altitude_metres
            self.coax_v_factor: float = c_object.coax_v_factor
            self.global_analogue_attenuation_db: float = c_object.global_analogue_attenuation_db
            self.ra_tile_pointing_degrees: float = c_object.ra_tile_pointing_degrees
            self.dec_tile_pointing_degrees: float = c_object.dec_tile_pointing_degrees
            self.ra_phase_center_degrees: float = c_object.ra_phase_center_degrees
            self.dec_phase_center_degrees: float = c_object.dec_phase_center_degrees
            self.azimuth_degrees: float = c_object.azimuth_degrees
            self.altitude_degrees: float = c_object.altitude_degrees
            self.sun_altitude_degrees: float = c_object.sun_altitude_degrees
            self.sun_distance_degrees: float = c_object.sun_distance_degrees
            self.moon_distance_degrees: float = c_object.moon_distance_degrees
            self.jupiter_distance_degrees: float = c_object.jupiter_distance_degrees
            self.lst_degrees: float = c_object.lst_degrees
            self.hour_angle_string: str = c_object.hour_angle_string.decode("utf-8")
            self.grid_name: str = c_object.grid_name.decode("utf-8")
            self.grid_number: int = c_object.grid_number
            self.creator: str = c_object.creator.decode("utf-8")
            self.project_id: str = c_object.project_id.decode("utf-8")
            self.observation_name: str = c_object.observation_name.decode("utf-8")
            self.mode: str = c_object.mode.decode("utf-8")
            self.scheduled_start_utc: int = c_object.scheduled_start_utc
            self.scheduled_start_mjd: float = c_object.scheduled_start_mjd
            self.scheduled_duration_milliseconds: int = c_object.scheduled_duration_milliseconds
            self.quack_time_duration_milliseconds: int = c_object.quack_time_duration_milliseconds
            self.good_time_unix_milliseconds: int = c_object.good_time_unix_milliseconds
            self.start_unix_time_milliseconds: int = c_object.start_unix_time_milliseconds
            self.end_unix_time_milliseconds: int = c_object.end_unix_time_milliseconds
            self.duration_milliseconds: int = c_object.duration_milliseconds
            self.num_timesteps: int = c_object.num_timesteps
            self.num_antennas: int = c_object.num_antennas
            self.num_baselines: int = c_object.num_baselines
            self.num_rf_inputs: int = c_object.num_rf_inputs
            self.num_antenna_pols: int = c_object.num_antenna_pols
            self.num_visibility_pols: int = c_object.num_visibility_pols
            self.num_coarse_channels: int = c_object.num_coarse_channels
            self.integration_time_milliseconds: int = c_object.integration_time_milliseconds
            self.fine_channel_width_hz: int = c_object.fine_channel_width_hz
            self.observation_bandwidth_hz: int = c_object.observation_bandwidth_hz
            self.coarse_channel_width_hz: int = c_object.coarse_channel_width_hz
            self.num_fine_channels_per_coarse: int = c_object.num_fine_channels_per_coarse
            self.num_timestep_coarse_channel_bytes: int = c_object.num_timestep_coarse_channel_bytes
            self.num_timestep_coarse_channel_floats: int = c_object.num_timestep_coarse_channel_floats
            self.num_gpubox_files: int = c_object.num_gpubox_files

            # We're now finished with the C memory, so free it
            mwalib.mwalibMetadata_free(c_object)

    def _get_coarse_channels(self):
        """Retrieve all of the coarse channel metadata and populate a list of coarse channels."""
        self.coarse_channels = []
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        for i in range(0, self.num_coarse_channels):
            c_object = CmwalibCoarseChannel.from_address(
                mwalib.mwalibCoarseChannel_get(self._context_object,
                                               i,
                                               error_message,
                                               ERROR_MESSAGE_LEN))

            if not c_object:
                raise ContextGetTimeStepError(f"Error creating coarse channel object:"
                                              f" {error_message.decode('utf-8').rstrip()}")
            else:
                # Populate all the fields
                self.coarse_channels.append(CoarseChannel(i,
                                                          c_object.correlator_channel_number,
                                                          c_object.receiver_channel_number,
                                                          c_object.gpubox_number,
                                                          c_object.channel_width_hz,
                                                          c_object.channel_start_hz,
                                                          c_object.channel_centre_hz,
                                                          c_object.channel_end_hz,))

                # We're now finished with the C memory, so free it
                mwalib.mwalibCoarseChannel_free(c_object)

    def _get_timesteps(self):
        """Retrieve all of the time step metadata and populate a list of time steps."""
        self.timesteps = []
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        for i in range(0, self.num_timesteps):
            c_object = CmwalibTimeStep.from_address(
                mwalib.mwalibTimeStep_get(self._context_object,
                                          i,
                                          error_message,
                                          ERROR_MESSAGE_LEN))

            if not c_object:
                raise ContextGetTimeStepError(f"Error creating timestep object: {error_message.decode('utf-8').rstrip()}")
            else:
                # Populate all the fields
                self.timesteps.append(TimeStep(i, c_object.unix_time_ms))

                # We're now finished with the C memory, so free it
                mwalib.mwalibTimeStep_free(c_object)

    def _get_rf_inputs(self):
        """Retrieve all of the rf_input metadata and populate a list of rf inputs."""
        self.rf_inputs = []
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        for i in range(0, self.num_rf_inputs):
            c_object = CmwalibRFInput.from_address(
                mwalib.mwalibRFInput_get(self._context_object,
                                         i,
                                         error_message,
                                         ERROR_MESSAGE_LEN))

            if not c_object:
                raise ContextGetRFInputError(f"Error creating rf_input object: "
                                             f"{error_message.decode('utf-8').rstrip()}")
            else:
                # Populate all the fields
                self.rf_inputs.append(RFInput(i,
                                      c_object.input,
                                      c_object.antenna,
                                      c_object.tile_id,
                                      c_object.tile_name.decode("utf-8"),
                                      c_object.pol.decode("utf-8"),
                                      c_object.electrical_length_m,
                                      c_object.north_m,
                                      c_object.east_m,
                                      c_object.height_m,
                                      c_object.vcs_order,
                                      c_object.subfile_order,
                                      c_object.flagged,))

                # We're now finished with the C memory, so free it
                mwalib.mwalibRFInput_free(c_object)

    def _get_antennas(self):
        """Retrieve all of the antenna metadata and populate a list of antennas."""
        self.antennas = []
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        for i in range(0, self.num_antennas):
            c_object = CmwalibAntenna.from_address(
                mwalib.mwalibAntenna_get(self._context_object,
                                         i,
                                         error_message,
                                         ERROR_MESSAGE_LEN))

            if not c_object:
                raise ContextGetAntennaError(f"Error creating antenna object: "
                                             f"{error_message.decode('utf-8').rstrip()}")
            else:
                # Populate all the fields
                self.antennas.append(Antenna(i,
                                     c_object.antenna,
                                     c_object.tile_id,
                                     c_object.tile_name.decode("utf-8"),
                                     self.rf_inputs[i * 2],
                                     self.rf_inputs[(i * 2) + 1]))

                # We're now finished with the C memory, so free it
                mwalib.mwalibAntenna_free(c_object)

    def display(self):
        """Displays a human readable summary of the observation"""
        error_message = create_string_buffer(ERROR_MESSAGE_LEN)

        if mwalib.mwalibContext_display(self._context_object, error_message, ERROR_MESSAGE_LEN) != 0:
            raise ContextDisplayError(f"Error calling mwalibContext_display(): "
                                      f"{error_message.decode('utf-8').rstrip()}")

    def read_by_baseline(self, timestep_index, coarse_channel_index):
        """Retrieve one HDU (ordered baseline,freq,pol,r,i) as a numpy array."""
        error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN

        float_buffer_type = ct.c_float * self.num_timestep_coarse_channel_floats
        buffer = float_buffer_type()

        if mwalib.mwalibContext_read_by_baseline(self._context_object,
                                                 ct.c_size_t(timestep_index),
                                                 ct.c_size_t(coarse_channel_index),
                                                 buffer,
                                                 self.num_timestep_coarse_channel_floats,
                                                 error_message, ERROR_MESSAGE_LEN) != 0:
            raise ContextReadByBaselineException(f"Error reading data: "
                                                 f"{error_message.decode('utf-8').rstrip()}")
        else:
            return npct.as_array(buffer, shape=(self.num_timestep_coarse_channel_floats,))

    def read_by_frequency(self, timestep_index, coarse_channel_index):
        """Retrieve one HDU (ordered freq,baseline,pol,r,i) as a numpy array."""
        error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN

        float_buffer_type = ct.c_float * self.num_timestep_coarse_channel_floats
        buffer = float_buffer_type()

        if mwalib.mwalibContext_read_by_frequency(self._context_object,
                                                  ct.c_size_t(timestep_index),
                                                  ct.c_size_t(coarse_channel_index),
                                                  buffer,
                                                  self.num_timestep_coarse_channel_floats,
                                                  error_message, ERROR_MESSAGE_LEN) != 0:
            raise ContextReadByFrequencyException(f"Error reading data: "
                                                 f"{error_message.decode('utf-8').rstrip()}")
        else:
            return npct.as_array(buffer, shape=(self.num_timestep_coarse_channel_floats,))

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(\n" \
               f"Obs ID                                : {self.obsid}\n" \
               f"Correlator Version                    : {CorrelatorVersion(self.corr_version).name}\n" \
               f"MWA Lat                               : {self.mwa_latitude_radians} rad\n" \
               f"MWA Long                              : {self.mwa_longitude_radians} rad\n" \
               f"MWA Alt                               : {self.mwa_altitude_metres} m\n" \
               f"Coax v factor                         : {self.coax_v_factor}\n" \
               f"Global attenuation                    : {self.global_analogue_attenuation_db} dB\n" \
               f"RA  (tile pointing)                   : {self.ra_tile_pointing_degrees} deg\n" \
               f"Dec (tile pointing)                   : {self.dec_tile_pointing_degrees} deg\n" \
               f"RA  (phase centre)                    : {self.ra_phase_center_degrees} deg\n" \
               f"Dec (phase centre)                    : {self.dec_phase_center_degrees} deg\n" \
               f"Az                                    : {self.azimuth_degrees} deg\n" \
               f"Alt                                   : {self.altitude_degrees} deg\n" \
               f"Sun Alt                               : {self.sun_altitude_degrees} deg\n" \
               f"Sun distance                          : {self.sun_distance_degrees} deg\n" \
               f"Moon distance                         : {self.moon_distance_degrees} deg\n" \
               f"Jupiter distance                      : {self.jupiter_distance_degrees} deg\n" \
               f"LST                                   : {self.lst_degrees} deg\n" \
               f"HA                                    : {self.hour_angle_string} dms\n" \
               f"Grid name                             : {self.grid_name}\n" \
               f"Grid number                           : {self.grid_number}\n" \
               f"Creator                               : {self.creator}\n" \
               f"Project ID                            : {self.project_id}\n" \
               f"Observation Name                      : {self.observation_name}\n" \
               f"Mode                                  : {self.mode}\n" \
               f"Scheduled Start                       : {self.scheduled_start_utc} UNIX\n" \
               f"Scheduled Start                       : {self.scheduled_start_mjd} MJD\n" \
               f"Scheduled Duration                    : {float(self.scheduled_duration_milliseconds) / 1000.} s\n" \
               f"Quack time (ms)                       : {float(self.quack_time_duration_milliseconds) / 1000.} s\n" \
               f"Good start time                       : {float(self.good_time_unix_milliseconds) / 1000.} UNIX\n" \
               f"(actual) Start time                   : {float(self.start_unix_time_milliseconds) / 1000.} UNIX\n" \
               f"(actual) End time                     : {float(self.end_unix_time_milliseconds) / 1000.} UNIX\n" \
               f"(actual) Duration                     : {float(self.duration_milliseconds) / 1000.} s\n" \
               f"(actual) num timesteps                : {self.num_timesteps}\n" \
               f"(actual) num antennas                 : {self.num_antennas}\n" \
               f"(actual) num baselines                : {self.num_baselines}\n" \
               f"(actual) num rf_inputs                : {self.num_rf_inputs}\n" \
               f"(actual) num antenna pols             : {self.num_antenna_pols}\n" \
               f"(actual) num visibility pols          : {self.num_visibility_pols}\n" \
               f"(actual) num coarse channels          : {self.num_coarse_channels}\n" \
               f"Correlator fine channel width         : {float(self.fine_channel_width_hz) / 1000.} kHz\n" \
               f"Correlator Integration time           : {float(self.integration_time_milliseconds) / 1000.} s\n" \
               f"(Data) Observation bandwidth          : {float(self.observation_bandwidth_hz) / 1000000.} MHz\n" \
               f"Coarse channel width                  : {float(self.coarse_channel_width_hz) / 1000000.} MHz\n" \
               f"Num fine channels per coarse          : {self.num_fine_channels_per_coarse}\n" \
               f"Num bytes per timestep coarse channel : " \
               f"{float(self.num_timestep_coarse_channel_bytes) / (1024. * 1024.)} MB\n" \
               f"Num floats per timestep coarse channel: " \
               f"{self.num_timestep_coarse_channel_floats}\n" \
               f"(actual) num GPUBox files             : {self.num_gpubox_files})"
