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

from numpy import double
from .mwalib import (
    mwalib_library,
    CMetafitsMetadataS,
    CMetafitsContextS,
    CCorrelatorContextS,
    CVoltageContextS,
    create_string_buffer,
)
from .common import (
    ERROR_MESSAGE_LEN,
    MWAMode,
    MWAVersion,
    GeometricDelaysApplied,
    CableDelaysApplied,
)
from .errors import PymwalibMetafitsMetadataGetError
from .antenna import Antenna
from .baseline import Baseline
from .rfinput import RFInput
from .coarse_channel import CoarseChannel
from .timestep import TimeStep


class MetafitsMetadata:
    def __init__(
        self,
        metafits_context: ct.POINTER(CMetafitsContextS),
        correlator_context: ct.POINTER(CCorrelatorContextS),
        voltage_context: ct.POINTER(CVoltageContextS),
    ):
        """Retrieve all of the metafits metadata and populate this class."""
        error_message: bytes = create_string_buffer(ERROR_MESSAGE_LEN)

        c_object_ptr = ct.POINTER(CMetafitsMetadataS)()

        if (
            mwalib_library.mwalib_metafits_metadata_get(
                metafits_context,
                correlator_context,
                voltage_context,
                ct.byref(c_object_ptr),
                error_message,
                ERROR_MESSAGE_LEN,
            )
            != 0
        ):
            raise PymwalibMetafitsMetadataGetError(
                "Error creating metafits metadata object:"
                f" {error_message.decode('utf-8').rstrip()}"
            )
        else:
            # Populate all the fields
            c_object = c_object_ptr.contents

            self.mwa_version: MWAVersion = c_object.mwa_version
            self.obs_id: int = c_object.obs_id
            self.global_analogue_attenuation_db: float = (
                c_object.global_analogue_attenuation_db
            )
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
            self.hour_angle_string: str = c_object.hour_angle_string.decode(
                "utf-8"
            )
            self.grid_name: str = c_object.grid_name.decode("utf-8")
            self.grid_number: int = c_object.grid_number
            self.creator: str = c_object.creator.decode("utf-8")
            self.project_id: str = c_object.project_id.decode("utf-8")
            self.obs_name: str = c_object.obs_name.decode("utf-8")
            self.mode: MWAMode = c_object.mode
            self.geometric_delays_applied: GeometricDelaysApplied = (
                c_object.geometric_delays_applied
            )
            self.cable_delays_applied: CableDelaysApplied = (
                c_object.cable_delays_applied
            )
            self.calibration_delays_and_gains_applied: bool = (
                c_object.calibration_delays_and_gains_applied
            )
            self.corr_fine_chan_width_hz: int = (
                c_object.corr_fine_chan_width_hz
            )
            self.corr_int_time_ms: int = c_object.corr_int_time_ms
            self.corr_raw_scale_factor: float = c_object.corr_raw_scale_factor
            self.num_corr_fine_chans_per_coarse: int = (
                c_object.num_corr_fine_chans_per_coarse
            )
            self.volt_fine_chan_width_hz: int = (
                c_object.volt_fine_chan_width_hz
            )
            self.num_volt_fine_chans_per_coarse: int = (
                c_object.num_volt_fine_chans_per_coarse
            )
            self.num_receivers = c_object.num_receivers
            self.receivers = []
            for r in range(0, self.num_receivers):
                self.receivers.append(c_object.receivers[r])
            self.num_delays = c_object.num_delays
            self.delays = []
            for d in range(0, self.num_delays):
                self.delays.append(c_object.delays[d])
            self.calibrator = c_object.calibrator
            self.calibrator_source: str = c_object.calibrator_source.decode(
                "utf-8"
            )
            self.sched_start_utc: datetime = datetime.utcfromtimestamp(
                c_object.sched_start_utc
            )
            self.sched_end_utc: datetime = datetime.utcfromtimestamp(
                c_object.sched_end_utc
            )
            self.sched_start_mjd: float = c_object.sched_start_mjd
            self.sched_end_mjd: float = c_object.sched_end_mjd
            self.sched_start_unix_time_ms: int = (
                c_object.sched_start_unix_time_ms
            )
            self.sched_end_unix_time_ms: int = c_object.sched_end_unix_time_ms
            self.sched_start_gps_time_ms: int = (
                c_object.sched_start_gps_time_ms
            )
            self.sched_end_gps_time_ms: int = c_object.sched_end_gps_time_ms
            self.sched_duration_ms: int = c_object.sched_duration_ms
            self.dut1: double = c_object.dut1
            self.quack_time_duration_ms: int = c_object.quack_time_duration_ms
            self.good_time_unix_ms: int = c_object.good_time_unix_ms
            self.good_time_gps_ms: int = c_object.good_time_gps_ms
            self.num_ants: int = c_object.num_ants
            self.num_rf_inputs: int = c_object.num_rf_inputs
            self.num_ant_pols: int = c_object.num_ant_pols
            self.num_baselines: int = c_object.num_baselines
            self.num_visibility_pols: int = c_object.num_visibility_pols
            self.num_metafits_timesteps: int = c_object.num_metafits_timesteps
            self.num_metafits_coarse_chans: int = (
                c_object.num_metafits_coarse_chans
            )
            self.num_metafits_fine_chan_freqs: int = (
                c_object.num_metafits_fine_chan_freqs
            )
            self.obs_bandwidth_hz: int = c_object.obs_bandwidth_hz
            self.coarse_chan_width_hz: int = c_object.coarse_chan_width_hz
            self.centre_freq_hz: int = c_object.centre_freq_hz
            self.metafits_filename: str = c_object.metafits_filename.decode(
                "utf-8"
            )

            # Populate rf_inputs
            self.rf_inputs = RFInput.get_rf_inputs(c_object)

            # Populate antennas
            self.antennas = Antenna.get_antennas(c_object, self.rf_inputs)

            # Populate baselines
            self.baselines = Baseline.get_baselines(c_object)

            # Populate timesteps
            self.metafits_timesteps = TimeStep.get_metafits_timesteps(c_object)

            # Populate coarse channels
            self.metafits_coarse_chans = (
                CoarseChannel.get_metafits_coarse_channels(c_object)
            )

            # fine chan frequencies
            self.metafits_fine_chan_freqs_hz = []
            for i in range(0, self.num_metafits_fine_chan_freqs):
                self.metafits_fine_chan_freqs_hz.append(
                    c_object.metafits_fine_chan_freqs_hz[i]
                )

            # We're now finished with the C memory, so free it
            mwalib_library.mwalib_metafits_metadata_free(c_object)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        """Returns a representation of the class"""
        return (
            f"{self.__class__.__name__}(\nMWA Version                         "
            f"  : {self.mwa_version.name}\nObs ID                             "
            f"   : {self.obs_id}\nGlobal attenuation                    :"
            f" {self.global_analogue_attenuation_db} dB\nRA  (tile pointing)  "
            f"                 : {self.ra_tile_pointing_deg} deg\nDec (tile"
            " pointing)                   :"
            f" {self.dec_tile_pointing_deg} deg\nRA  (phase centre)           "
            f"         : {self.ra_phase_center_deg} deg\nDec (phase centre)   "
            f"                 : {self.dec_phase_center_deg} deg\nAz          "
            f"                          : {self.az_deg} deg\nAlt              "
            f"                     : {self.alt_deg} deg\nZenith Angle         "
            f"                 : {self.za_deg} deg\nAz                        "
            f"            : {self.az_rad} rad\nAlt                            "
            f"       : {self.alt_rad} rad\nZenith Angle                       "
            f"   : {self.za_rad} rad\nSun Alt                               :"
            f" {self.sun_alt_deg} deg\nSun distance                          :"
            f" {self.sun_distance_deg} deg\nMoon distance                     "
            f"    : {self.moon_distance_deg} deg\nJupiter distance            "
            f"          : {self.jupiter_distance_deg} deg\nLST                "
            f"                   : {self.lst_deg} deg\nLST                    "
            f"               : {self.lst_rad} rad\nHA                         "
            f"           : {self.hour_angle_string} dms\nGrid name            "
            f"                 : {self.grid_name}\nGrid number                "
            f"           : {self.grid_number}\nCreator                        "
            f"       : {self.creator}\nProject ID                            :"
            f" {self.project_id}\nObservation Name                      :"
            f" {self.obs_name}\nMode                                  :"
            f" {self.mode}\ngeometric_delays_applied              :"
            f" {self.geometric_delays_applied}\ncable_delays_applied          "
            "        :"
            f" {self.cable_delays_applied}\ncalibration_delays_and_gains_applied"
            f"  : {self.calibration_delays_and_gains_applied}\nCorrelator fine"
            " channel width (Hz)    :"
            f" {self.corr_fine_chan_width_hz}\nCorrelator int. time (ms)      "
            f"       : {self.corr_int_time_ms}\nCorrelator fine channels per"
            f" coarse   : {self.num_corr_fine_chans_per_coarse}\nReceivers    "
            f"                         : {self.receivers}\nDelays             "
            f"                   : {self.delays}\nCalibrator                  "
            f"          : {self.calibrator}\nCalibrator Source                "
            f"     : {self.calibrator_source}\nScheduled Start (UTC)          "
            f"       : {self.sched_start_utc}\nScheduled End (UTC)            "
            f"       : {self.sched_end_utc}\nScheduled Start (UNIX)           "
            "     :"
            f" {float(self.sched_start_unix_time_ms) / 1000.} UNIX\nScheduled"
            " End (UNIX)                  :"
            f" {float(self.sched_end_unix_time_ms) / 1000.} UNIX\nScheduled"
            " Start (MJD)                 :"
            f" {self.sched_start_mjd} MJD\nScheduled End (MJD)                "
            f"   : {self.sched_end_mjd} MJD\nScheduled Duration               "
            f"     : {float(self.sched_duration_ms) / 1000.} s\nQuack time"
            " (ms)                       :"
            f" {float(self.quack_time_duration_ms) / 1000.} s\nGood start time"
            " (UNIX)                :"
            f" {float(self.good_time_unix_ms) / 1000.} UNIX\nGood start time"
            " (GPS)                 :"
            f" {float(self.good_time_gps_ms) / 1000.} GPS\nnum antennas       "
            f"                   : {self.num_ants}\nnum rf_inputs             "
            f"            : {self.num_rf_inputs}\nBaselines                   "
            f"          : {self.num_baselines}\nVisibility pols               "
            f"        : {self.num_visibility_pols}\nnum antenna pols          "
            f"            : {self.num_ant_pols}\nnum metafits timesteps       "
            f"         : {self.num_metafits_timesteps}\nnum metafits coarse"
            f" channels          : {self.num_metafits_coarse_chans}\nnum"
            " metafits fine channels            :"
            f" {self.num_metafits_fine_chan_freqs}\nObservation bandwidth     "
            "            :"
            f" {float(self.obs_bandwidth_hz) / 1000000.} MHz\nCoarse channel"
            " width                  :"
            f" {float(self.coarse_chan_width_hz) / 1000000.} MHz\n)\n"
        )
