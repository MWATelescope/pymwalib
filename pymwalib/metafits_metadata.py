#!/usr/bin/env python
#
# Main class for access metafits metadata
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import ctypes as ct
from datetime import datetime
from .mwalib import mwalib_library, CMetafitsMetadataS, CMetafitsContextS, CCorrelatorContextS, CVoltageContextS, \
    create_string_buffer
from .common import ERROR_MESSAGE_LEN, MWAMode, MWAVersion, GeometricDelaysApplied
from .errors import PymwalibMetafitsMetadataGetError
from .antenna import Antenna
from .baseline import Baseline
from .rfinput import RFInput
from .coarse_channel import CoarseChannel
from .timestep import TimeStep


class MetafitsMetadata:
    def __init__(self,
                 metafits_context: ct.POINTER(CMetafitsContextS),
                 correlator_context: ct.POINTER(CCorrelatorContextS),
                 voltage_context: ct.POINTER(CVoltageContextS)):
        """Retrieve all of the metafits metadata and populate this class."""
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_object_ptr = ct.POINTER(CMetafitsMetadataS)()

        if mwalib_library.mwalib_metafits_metadata_get(metafits_context,
                                                       correlator_context,
                                                       voltage_context,
                                                       ct.byref(c_object_ptr),
                                                       error_message,
                                                       ERROR_MESSAGE_LEN) != 0:
            raise PymwalibMetafitsMetadataGetError(
                f"Error creating metafits metadata object: {error_message.decode('utf-8').rstrip()}")
        else:
            # Populate all the fields
            c_object = c_object_ptr.contents

            self.mwa_version: MWAVersion = c_object.mwa_version
            self.obs_id: int = c_object.obs_id
            self.global_analogue_attenuation_db: float = c_object.global_analogue_attenuation_db
            self.ra_tile_pointing_deg: float = c_object.ra_tile_pointing_deg
            self.dec_tile_pointing_deg: float = c_object.dec_tile_pointing_deg
            self.ra_phase_center_deg: float = c_object.ra_phase_center_deg
            self.dec_phase_center_deg: float = c_object.dec_phase_center_deg
            self.az_deg: float = c_object.az_deg
            self.alt_deg: float = c_object.alt_deg
            self.za_deg: float = c_object.za_deg
            self.az_rad: float = c_object.az_rad
            self.alt_rad: float = c_object.alt_rad
            self.za_rad: float = c_object.za_rad
            self.sun_alt_deg: float = c_object.sun_alt_deg
            self.sun_distance_deg: float = c_object.sun_distance_deg
            self.moon_distance_deg: float = c_object.moon_distance_deg
            self.jupiter_distance_deg: float = c_object.jupiter_distance_deg
            self.lst_deg: float = c_object.lst_deg
            self.lst_rad: float = c_object.lst_rad
            self.hour_angle_string: str = c_object.hour_angle_string.decode("utf-8")
            self.grid_name: str = c_object.grid_name.decode("utf-8")
            self.grid_number: int = c_object.grid_number
            self.creator: str = c_object.creator.decode("utf-8")
            self.project_id: str = c_object.project_id.decode("utf-8")
            self.obs_name: str = c_object.obs_name.decode("utf-8")
            self.mode: MWAMode = c_object.mode
            self.geometric_delays_applied: GeometricDelaysApplied = c_object.geometric_delays_applied
            self.cable_delays_applied: bool = c_object.cable_delays_applied
            self.calibration_delays_and_gains_applied: bool = c_object.calibration_delays_and_gains_applied
            self.corr_fine_chan_width_hz: int = c_object.corr_fine_chan_width_hz
            self.corr_int_time_ms: int = c_object.corr_int_time_ms
            self.num_corr_fine_chans_per_coarse: int = c_object.num_corr_fine_chans_per_coarse
            self.volt_fine_chan_width_hz: int = c_object.volt_fine_chan_width_hz
            self.num_volt_fine_chans_per_coarse: int = c_object.num_volt_fine_chans_per_coarse
            self.num_receivers = c_object.num_receivers
            self.receivers = []
            for r in range(0, self.num_receivers):
                self.receivers.append(c_object.receivers[r])
            self.num_delays = c_object.num_delays
            self.delays = []
            for d in range(0, self.num_delays):
                self.delays.append(c_object.delays[d])
            self.sched_start_utc: datetime = datetime.utcfromtimestamp(c_object.sched_start_utc)
            self.sched_end_utc: datetime = datetime.utcfromtimestamp(c_object.sched_end_utc)
            self.sched_start_mjd: float = c_object.sched_start_mjd
            self.sched_end_mjd: float = c_object.sched_end_mjd
            self.sched_start_unix_time_ms: int = c_object.sched_start_unix_time_ms
            self.sched_end_unix_time_ms: int = c_object.sched_end_unix_time_ms
            self.sched_start_gps_time_ms: int = c_object.sched_start_gps_time_ms
            self.sched_end_gps_time_ms: int = c_object.sched_end_gps_time_ms
            self.sched_duration_ms: int = c_object.sched_duration_ms
            self.quack_time_duration_ms: int = c_object.quack_time_duration_ms
            self.good_time_unix_ms: int = c_object.good_time_unix_ms
            self.good_time_gps_ms: int = c_object.good_time_gps_ms
            self.num_ants: int = c_object.num_ants
            self.num_rf_inputs: int = c_object.num_rf_inputs
            self.num_ant_pols: int = c_object.num_ant_pols
            self.num_baselines: int = c_object.num_baselines
            self.num_visibility_pols: int = c_object.num_visibility_pols
            self.num_metafits_timesteps: int = c_object.num_metafits_timesteps
            self.num_metafits_coarse_chans: int = c_object.num_metafits_coarse_chans
            self.num_metafits_fine_chan_freqs: int = c_object.num_metafits_fine_chan_freqs
            self.obs_bandwidth_hz: int = c_object.obs_bandwidth_hz
            self.coarse_chan_width_hz: int = c_object.coarse_chan_width_hz
            self.centre_freq_hz: int = c_object.centre_freq_hz
            self.metafits_filename: str = c_object.metafits_filename.decode("utf-8")

            # Populate rf_inputs
            self.rf_inputs = RFInput.get_rf_inputs(c_object)

            # Populate antennas
            self.antennas = Antenna.get_antennas(c_object, self.rf_inputs)

            # Populate baselines
            self.baselines = Baseline.get_baselines(c_object)

            # Populate timesteps
            self.metafits_timesteps = TimeStep.get_metafits_timesteps(c_object)

            # Populate coarse channels
            self.metafits_coarse_chans = CoarseChannel.get_metafits_coarse_channels(c_object)

            # fine chan frequencies
            self.metafits_fine_chan_freqs_hz = []
            for i in range(0, self.num_metafits_fine_chan_freqs):
                self.metafits_fine_chan_freqs_hz.append(c_object.metafits_fine_chan_freqs_hz[i])

            # We're now finished with the C memory, so free it
            mwalib_library.mwalib_metafits_metadata_free(c_object)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(\n" \
               f"MWA Version                           : {self.mwa_version.name}\n" \
               f"Obs ID                                : {self.obs_id}\n" \
               f"Global attenuation                    : {self.global_analogue_attenuation_db} dB\n" \
               f"RA  (tile pointing)                   : {self.ra_tile_pointing_deg} deg\n" \
               f"Dec (tile pointing)                   : {self.dec_tile_pointing_deg} deg\n" \
               f"RA  (phase centre)                    : {self.ra_phase_center_deg} deg\n" \
               f"Dec (phase centre)                    : {self.dec_phase_center_deg} deg\n" \
               f"Az                                    : {self.az_deg} deg\n" \
               f"Alt                                   : {self.alt_deg} deg\n" \
               f"Zenith Angle                          : {self.za_deg} deg\n" \
               f"Az                                    : {self.az_rad} rad\n" \
               f"Alt                                   : {self.alt_rad} rad\n" \
               f"Zenith Angle                          : {self.za_rad} rad\n" \
               f"Sun Alt                               : {self.sun_alt_deg} deg\n" \
               f"Sun distance                          : {self.sun_distance_deg} deg\n" \
               f"Moon distance                         : {self.moon_distance_deg} deg\n" \
               f"Jupiter distance                      : {self.jupiter_distance_deg} deg\n" \
               f"LST                                   : {self.lst_deg} deg\n" \
               f"LST                                   : {self.lst_rad} rad\n" \
               f"HA                                    : {self.hour_angle_string} dms\n" \
               f"Grid name                             : {self.grid_name}\n" \
               f"Grid number                           : {self.grid_number}\n" \
               f"Creator                               : {self.creator}\n" \
               f"Project ID                            : {self.project_id}\n" \
               f"Observation Name                      : {self.obs_name}\n" \
               f"Mode                                  : {self.mode}\n" \
               f"geometric_delays_applied              : {self.geometric_delays_applied}\n" \
               f"cable_delays_applied                  : {self.cable_delays_applied}\n" \
               f"calibration_delays_and_gains_applied  : {self.calibration_delays_and_gains_applied}\n" \
               f"Correlator fine channel width (Hz)    : {self.corr_fine_chan_width_hz}\n" \
               f"Correlator int. time (ms)             : {self.corr_int_time_ms}\n" \
               f"Correlator fine channels per coarse   : {self.num_corr_fine_chans_per_coarse}\n" \
               f"Receivers                             : {self.receivers}\n" \
               f"Delays                                : {self.delays}\n" \
               f"Scheduled Start (UTC)                 : {self.sched_start_utc}\n" \
               f"Scheduled End (UTC)                   : {self.sched_end_utc}\n" \
               f"Scheduled Start (UNIX)                : {float(self.sched_start_unix_time_ms) / 1000.} UNIX\n" \
               f"Scheduled End (UNIX)                  : {float(self.sched_end_unix_time_ms) / 1000.} UNIX\n" \
               f"Scheduled Start (MJD)                 : {self.sched_start_mjd} MJD\n" \
               f"Scheduled End (MJD)                   : {self.sched_end_mjd} MJD\n" \
               f"Scheduled Duration                    : {float(self.sched_duration_ms) / 1000.} s\n" \
               f"Quack time (ms)                       : {float(self.quack_time_duration_ms) / 1000.} s\n" \
               f"Good start time (UNIX)                : {float(self.good_time_unix_ms) / 1000.} UNIX\n" \
               f"Good start time (GPS)                 : {float(self.good_time_gps_ms) / 1000.} GPS\n" \
               f"num antennas                          : {self.num_ants}\n" \
               f"num rf_inputs                         : {self.num_rf_inputs}\n" \
               f"Baselines                             : {self.num_baselines}\n" \
               f"Visibility pols                       : {self.num_visibility_pols}\n" \
               f"num antenna pols                      : {self.num_ant_pols}\n" \
               f"num metafits timesteps                : {self.num_metafits_timesteps}\n" \
               f"num metafits coarse channels          : {self.num_metafits_coarse_chans}\n" \
               f"num metafits fine channels            : {self.num_metafits_fine_chan_freqs}\n" \
               f"Observation bandwidth                 : {float(self.obs_bandwidth_hz) / 1000000.} MHz\n" \
               f"Coarse channel width                  : {float(self.coarse_chan_width_hz) / 1000000.} MHz\n)\n"
