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
from datetime import datetime
from pymwalib.mwalib import *
from pymwalib.common import ERROR_MESSAGE_LEN
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

            self.obs_id: int = c_object.obs_id
            self.mwa_lat_rad: float = c_object.mwa_lat_rad
            self.mwa_long_rad: float = c_object.mwa_long_rad
            self.mwa_alt_metres: float = c_object.mwa_alt_metres
            self.coax_v_factor: float = c_object.coax_v_factor
            self.global_analogue_attenuation_db: float = c_object.global_analogue_attenuation_db
            self.ra_tile_pointing_deg: float = c_object.ra_tile_pointing_deg
            self.dec_tile_pointing_deg: float = c_object.dec_tile_pointing_deg
            self.ra_phase_center_deg: float = c_object.ra_phase_center_deg
            self.dec_phase_center_deg: float = c_object.dec_phase_center_deg
            self.az_deg: float = c_object.az_deg
            self.alt_deg: float = c_object.alt_deg
            self.sun_alt_deg: float = c_object.sun_alt_deg
            self.sun_distance_deg: float = c_object.sun_distance_deg
            self.moon_distance_deg: float = c_object.moon_distance_deg
            self.jupiter_distance_deg: float = c_object.jupiter_distance_deg
            self.lst_deg: float = c_object.lst_deg
            self.hour_angle_string: str = c_object.hour_angle_string.decode("utf-8")
            self.grid_name: str = c_object.grid_name.decode("utf-8")
            self.grid_number: int = c_object.grid_number
            self.creator: str = c_object.creator.decode("utf-8")
            self.project_id: str = c_object.project_id.decode("utf-8")
            self.obs_name: str = c_object.obs_name.decode("utf-8")
            self.mode: str = c_object.mode.decode("utf-8")
            self.num_baselines: int = c_object.num_baselines
            self.num_visibility_pols: int = c_object.num_visibility_pols
            self.corr_fine_chan_width_hz: int = c_object.corr_fine_chan_width_hz
            self.corr_int_time_ms: int = c_object.corr_int_time_ms
            self.num_corr_fine_chans_per_coarse: int = c_object.num_corr_fine_chans_per_coarse
            self.sched_start_utc: datetime = datetime.utcfromtimestamp(c_object.sched_start_utc)
            self.sched_end_utc: datetime = datetime.utcfromtimestamp(c_object.sched_end_utc)
            self.sched_start_mjd: float = c_object.sched_start_mjd
            self.sched_end_mjd: float = c_object.sched_end_mjd
            self.sched_start_unix_time_ms: int = c_object.sched_start_unix_time_ms
            self.sched_end_unix_time_ms: int = c_object.sched_end_unix_time_ms
            self.sched_duration_ms: int = c_object.sched_duration_ms
            self.quack_time_duration_ms: int = c_object.quack_time_duration_ms
            self.good_time_unix_ms: int = c_object.good_time_unix_ms
            self.num_ants: int = c_object.num_ants
            self.num_rf_inputs: int = c_object.num_rf_inputs
            self.num_ant_pols: int = c_object.num_ant_pols
            self.num_coarse_chans: int = c_object.num_coarse_chans
            self.obs_bandwidth_hz: int = c_object.obs_bandwidth_hz
            self.coarse_chan_width_hz: int = c_object.coarse_chan_width_hz

            # We're now finished with the C memory, so free it
            mwalib.mwalib_metafits_metadata_free(c_object)

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(\n" \
               f"Obs ID                                : {self.obs_id}\n" \
               f"MWA Lat                               : {self.mwa_lat_rad} rad\n" \
               f"MWA Long                              : {self.mwa_long_rad} rad\n" \
               f"MWA Alt                               : {self.mwa_alt_metres} m\n" \
               f"Coax v factor                         : {self.coax_v_factor}\n" \
               f"Global attenuation                    : {self.global_analogue_attenuation_db} dB\n" \
               f"RA  (tile pointing)                   : {self.ra_tile_pointing_deg} deg\n" \
               f"Dec (tile pointing)                   : {self.dec_tile_pointing_deg} deg\n" \
               f"RA  (phase centre)                    : {self.ra_phase_center_deg} deg\n" \
               f"Dec (phase centre)                    : {self.dec_phase_center_deg} deg\n" \
               f"Az                                    : {self.az_deg} deg\n" \
               f"Alt                                   : {self.alt_deg} deg\n" \
               f"Sun Alt                               : {self.sun_alt_deg} deg\n" \
               f"Sun distance                          : {self.sun_distance_deg} deg\n" \
               f"Moon distance                         : {self.moon_distance_deg} deg\n" \
               f"Jupiter distance                      : {self.jupiter_distance_deg} deg\n" \
               f"LST                                   : {self.lst_deg} deg\n" \
               f"HA                                    : {self.hour_angle_string} dms\n" \
               f"Grid name                             : {self.grid_name}\n" \
               f"Grid number                           : {self.grid_number}\n" \
               f"Creator                               : {self.creator}\n" \
               f"Project ID                            : {self.project_id}\n" \
               f"Observation Name                      : {self.obs_name}\n" \
               f"Mode                                  : {self.mode}\n" \
               f"Correlator fine channel width (Hz)    : {self.corr_fine_chan_width_hz}\n" \
               f"Correlator int. time (ms)             : {self.corr_int_time_ms}\n" \
               f"Correlator fine channels per coarse   : {self.num_corr_fine_chans_per_coarse}\n" \
               f"Scheduled Start (UTC)                 : {self.sched_start_utc}\n" \
               f"Scheduled End (UTC)                   : {self.sched_end_utc}\n" \
               f"Scheduled Start (UNIX)                : {float(self.sched_start_unix_time_ms) / 1000.} UNIX\n" \
               f"Scheduled End (UNIX)                  : {float(self.sched_end_unix_time_ms) / 1000.} UNIX\n" \
               f"Scheduled Start (MJD)                 : {self.sched_start_mjd} MJD\n" \
               f"Scheduled End (MJD)                   : {self.sched_end_mjd} MJD\n" \
               f"Scheduled Duration                    : {float(self.sched_duration_ms) / 1000.} s\n" \
               f"Quack time (ms)                       : {float(self.quack_time_duration_ms) / 1000.} s\n" \
               f"Good start time                       : {float(self.good_time_unix_ms) / 1000.} UNIX\n" \
               f"num antennas                          : {self.num_ants}\n" \
               f"num rf_inputs                         : {self.num_rf_inputs}\n" \
               f"Baselines                             : {self.num_baselines}\n" \
               f"Visibility pols                       : {self.num_visibility_pols}\n" \
               f"num antenna pols                      : {self.num_ant_pols}\n" \
               f"(actual) num coarse channels          : {self.num_coarse_chans}\n" \
               f"(Data) Observation bandwidth          : {float(self.obs_bandwidth_hz) / 1000000.} MHz\n" \
               f"Coarse channel width                  : {float(self.coarse_chan_width_hz) / 1000000.} MHz\n)\n"
