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
from datetime import datetime
from pymwalib.mwalib import *
from pymwalib.common import CorrelatorVersion, ERROR_MESSAGE_LEN
from pymwalib.errors import *


class MetafitsMetadata:
    def __init__(self,
                 metafits_context: ct.POINTER(CMetafitsContextS),
                 correlator_context: ct.POINTER(CCorrelatorContextS),
                 voltage_context: ct.POINTER(CVoltageContextS)):
        """Retrieve all of the metafits metadata and populate this class."""
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_object_ptr = ct.POINTER(CMetafitsMetadataS)()

        if mwalib.mwalib_metafits_metadata_get(metafits_context,
                                               correlator_context,
                                               voltage_context,
                                               ct.byref(c_object_ptr),
                                               error_message,
                                               ERROR_MESSAGE_LEN) != 0:
            raise ContextMetafitsMetadataGetError(
                f"Error creating metafits metadata object: {error_message.decode('utf-8').rstrip()}")
        else:
            # Populate all the fields
            c_object = c_object_ptr.contents

            self.obsid: int = c_object.obsid
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
            self.scheduled_start_utc: datetime = datetime.utcfromtimestamp(c_object.scheduled_start_utc)
            self.scheduled_end_utc: datetime = datetime.utcfromtimestamp(c_object.scheduled_end_utc)
            self.scheduled_start_mjd: float = c_object.scheduled_start_mjd
            self.scheduled_end_mjd: float = c_object.scheduled_end_mjd
            self.scheduled_start_unix_time_milliseconds: int = c_object.scheduled_start_unix_time_milliseconds
            self.scheduled_end_unix_time_milliseconds: int = c_object.scheduled_end_unix_time_milliseconds
            self.scheduled_duration_milliseconds: int = c_object.scheduled_duration_milliseconds
            self.quack_time_duration_milliseconds: int = c_object.quack_time_duration_milliseconds
            self.good_time_unix_milliseconds: int = c_object.good_time_unix_milliseconds
            self.num_antennas: int = c_object.num_antennas
            self.num_rf_inputs: int = c_object.num_rf_inputs
            self.num_antenna_pols: int = c_object.num_antenna_pols
            self.num_coarse_channels: int = c_object.num_coarse_channels
            self.observation_bandwidth_hz: int = c_object.observation_bandwidth_hz
            self.coarse_channel_width_hz: int = c_object.coarse_channel_width_hz

            # We're now finished with the C memory, so free it
            mwalib.mwalib_metafits_metadata_free(c_object)

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(\n" \
               f"Obs ID                                : {self.obsid}\n" \
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
               f"Scheduled Start (UTC)                 : {self.scheduled_start_utc}\n" \
               f"Scheduled End (UTC)                   : {self.scheduled_end_utc}\n" \
               f"Scheduled Start (UNIX)                : {float(self.scheduled_start_unix_time_milliseconds) / 1000.} UNIX\n" \
               f"Scheduled End (UNIX)                  : {float(self.scheduled_end_unix_time_milliseconds) / 1000.} UNIX\n" \
               f"Scheduled Start (MJD)                 : {self.scheduled_start_mjd} MJD\n" \
               f"Scheduled End (MJD)                   : {self.scheduled_end_mjd} MJD\n" \
               f"Scheduled Duration                    : {float(self.scheduled_duration_milliseconds) / 1000.} s\n" \
               f"Quack time (ms)                       : {float(self.quack_time_duration_milliseconds) / 1000.} s\n" \
               f"Good start time                       : {float(self.good_time_unix_milliseconds) / 1000.} UNIX\n" \
               f"(actual) num antennas                 : {self.num_antennas}\n" \
               f"(actual) num rf_inputs                : {self.num_rf_inputs}\n" \
               f"(actual) num antenna pols             : {self.num_antenna_pols}\n" \
               f"(actual) num coarse channels          : {self.num_coarse_channels}\n" \
               f"(Data) Observation bandwidth          : {float(self.observation_bandwidth_hz) / 1000000.} MHz\n" \
               f"Coarse channel width                  : {float(self.coarse_channel_width_hz) / 1000000.} MHz\n)\n"
