#!/usr/bin/env python
#
# mwalib.py: C wrappers
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import ctypes as ct
import sys

MWALIB_SUCCESS = 0
MWALIB_FAILURE = 1
MWALIB_NO_DATA_FOR_TIMESTEP_COARSECHAN = -1


#
# Creates a string buffer for interacting with C strings
#
def create_string_buffer(length: int) -> bytes:
    return " ".encode("utf-8") * length


#
# C MetafitsContext struct
#
class CMetafitsContextS(ct.Structure):
    pass


#
# C CorrelatorContext struct
#
class CCorrelatorContextS(ct.Structure):
    pass


#
# C VoltageContext struct
#
class CVoltageContextS(ct.Structure):
    pass


#
# mwalib: setup linking to the mwalib library
#
prefix = {"win32": ""}.get(sys.platform, "lib")
extension = {"darwin": ".dylib", "win32": ".dll"}.get(sys.platform, ".so")
mwalib_filename = prefix + "mwalib" + extension
mwalib_library = None

try:
    mwalib_library = ct.cdll.LoadLibrary(mwalib_filename)
except Exception as library_load_err:
    print(
        f"Error loading {mwalib_filename}. Please check that it is in your system library path or in your LD_LIBRARY_PATH "
        f"environment variable.\n\nError was: {library_load_err}")
    exit(1)

#
# Define the Library functions if the library was loaded
#
if mwalib_library:
    #
    # mwalib_get_version_major
    #
    mwalib_library.mwalib_get_version_major.argtypes = None
    mwalib_library.mwalib_get_version_major.restype = ct.c_uint32

    #
    # mwalib_get_version_minor
    #
    mwalib_library.mwalib_get_version_minor.argtypes = None
    mwalib_library.mwalib_get_version_minor.restype = ct.c_uint32

    #
    # mwalib_get_version_patch
    #
    mwalib_library.mwalib_get_version_patch.argtypes = None
    mwalib_library.mwalib_get_version_patch.restype = ct.c_uint32

    #
    # mwalib_metafits_context_new()
    #
    mwalib_library.mwalib_metafits_context_new.argtypes = \
        (ct.c_char_p,  # metafits
         ct.c_uint,  # MWAVersion
         ct.POINTER(ct.POINTER(CMetafitsContextS)),  # Pointer to pointer to CorrelatorContext
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_metafits_context_new.restype = ct.c_int32

    #
    # mwalib_metafits_context_new2()
    #
    mwalib_library.mwalib_metafits_context_new2.argtypes = \
        (ct.c_char_p,  # metafits
         ct.POINTER(ct.POINTER(CMetafitsContextS)),  # Pointer to pointer to CorrelatorContext
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_metafits_context_new2.restype = ct.c_int32

    #
    # mwalib_metafits_context_free()
    #
    mwalib_library.mwalib_metafits_context_free.argtypes = (ct.POINTER(CMetafitsContextS),)
    mwalib_library.mwalib_metafits_context_free.restype = ct.c_int32

    #
    # mwalib_metafits_context_display()
    #
    mwalib_library.mwalib_metafits_context_display.argtypes = (ct.POINTER(CMetafitsContextS),)
    mwalib_library.mwalib_metafits_context_display.restype = ct.c_int32

    #
    # mwalib_metafits_get_expected_volt_filename
    #
    mwalib_library.mwalib_metafits_get_expected_volt_filename.argtypes = \
        (ct.POINTER(CMetafitsContextS),  # metafits context
         ct.c_size_t,  # timestep_index
         ct.c_size_t,  # coarse_chan_index
         ct.c_char_p,  # filename buffer
         ct.c_size_t,  # length of filename buffer
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_metafits_get_expected_volt_filename.restype = ct.c_int32

    #
    # C Antenna struct
    #
    class CAntennaS(ct.Structure):
        _fields_ = [('ant', ct.c_uint32),
                    ('tile_id', ct.c_uint32),
                    ('tile_name', ct.c_char_p),
                    ('rfinput_x', ct.c_size_t),
                    ('rfinput_y', ct.c_size_t),
                    ('electrical_length_m', ct.c_double),
                    ('north_m', ct.c_double),
                    ('east_m', ct.c_double),
                    ('height_m', ct.c_double),
                    ]

    #
    # C Baseline struct
    #
    class CBaselineS(ct.Structure):
        _fields_ = [('ant1_index', ct.c_size_t),
                    ('ant2_index', ct.c_size_t), ]

    #
    # C CoarseChannel struct
    #
    class CCoarseChannelS(ct.Structure):
        _fields_ = [('corr_chan_number', ct.c_size_t),
                    ('rec_chan_number', ct.c_size_t),
                    ('gpubox_number', ct.c_size_t),
                    ('chan_width_hz', ct.c_uint32),
                    ('chan_start_hz', ct.c_uint32),
                    ('chan_centre_hz', ct.c_uint32),
                    ('chan_end_hz', ct.c_uint32), ]

    #
    # C RFInput struct
    #
    class CRFInputS(ct.Structure):
        _fields_ = [('input', ct.c_uint32),
                    ('ant', ct.c_uint32),
                    ('tile_id', ct.c_uint32),
                    ('tile_name', ct.c_char_p),
                    ('pol', ct.c_char_p),
                    ('electrical_length_m', ct.c_double),
                    ('north_m', ct.c_double),
                    ('east_m', ct.c_double),
                    ('height_m', ct.c_double),
                    ('vcs_order', ct.c_uint32),
                    ('subfile_order', ct.c_uint32),
                    ('flagged', ct.c_bool),
                    ('digital_gains', ct.POINTER(ct.c_uint32)),
                    ('num_digital_gains', ct.c_size_t),
                    ('dipole_delays', ct.POINTER(ct.c_uint32)),
                    ('num_dipole_delays', ct.c_size_t),
                    ('dipole_gains', ct.POINTER(ct.c_double)),
                    ('num_dipole_gains', ct.c_size_t),
                    ('rec_number', ct.c_uint32),
                    ('rec_slot_number', ct.c_uint32), ]

    #
    # C TimeStep struct
    #
    class CTimeStepS(ct.Structure):
        _fields_ = [('unix_time_ms', ct.c_uint64),
                    ('gps_time_ms', ct.c_uint64), ]

    #
    # C MetafitsMetadata struct
    #
    class CMetafitsMetadataS(ct.Structure):
        _fields_ = [('mwa_version', ct.c_uint32),
                    ('obs_id', ct.c_uint32),
                    ('global_analogue_attenuation_db', ct.c_double),
                    ('ra_tile_pointing_deg', ct.c_double),
                    ('dec_tile_pointing_deg', ct.c_double),
                    ('ra_phase_center_deg', ct.c_double),
                    ('dec_phase_center_deg', ct.c_double),
                    ('az_deg', ct.c_double),
                    ('alt_deg', ct.c_double),
                    ('za_deg', ct.c_double),
                    ('az_rad', ct.c_double),
                    ('alt_rad', ct.c_double),
                    ('za_rad', ct.c_double),
                    ('sun_alt_deg', ct.c_double),
                    ('sun_distance_deg', ct.c_double),
                    ('moon_distance_deg', ct.c_double),
                    ('jupiter_distance_deg', ct.c_double),
                    ('lst_deg', ct.c_double),
                    ('lst_rad', ct.c_double),
                    ('hour_angle_string', ct.c_char_p),
                    ('grid_name', ct.c_char_p),
                    ('grid_number', ct.c_int32),
                    ('creator', ct.c_char_p),
                    ('project_id', ct.c_char_p),
                    ('obs_name', ct.c_char_p),
                    ('mode', ct.c_uint32),
                    ('geometric_delays_applied', ct.c_uint32),
                    ('cable_delays_applied', ct.c_bool),
                    ('calibration_delays_and_gains_applied', ct.c_bool),
                    ('corr_fine_chan_width_hz', ct.c_uint32),
                    ('corr_int_time_ms', ct.c_uint64),
                    ('num_corr_fine_chans_per_coarse', ct.c_size_t),
                    ('volt_fine_chan_width_hz', ct.c_int32),
                    ('num_volt_fine_chans_per_coarse', ct.c_size_t),
                    ('receivers', ct.POINTER(ct.c_size_t)),
                    ('num_receivers', ct.c_size_t),
                    ('delays', ct.POINTER(ct.c_uint32)),
                    ('num_delays', ct.c_size_t),
                    ('sched_start_utc', ct.c_uint64),
                    ('sched_end_utc', ct.c_uint64),
                    ('sched_start_mjd', ct.c_double),
                    ('sched_end_mjd', ct.c_double),
                    ('sched_start_unix_time_ms', ct.c_uint64),
                    ('sched_end_unix_time_ms', ct.c_uint64),
                    ('sched_start_gps_time_ms', ct.c_uint64),
                    ('sched_end_gps_time_ms', ct.c_uint64),
                    ('sched_duration_ms', ct.c_uint64),
                    ('quack_time_duration_ms', ct.c_uint64),
                    ('good_time_unix_ms', ct.c_uint64),
                    ('good_time_gps_ms', ct.c_uint64),
                    ('num_ants', ct.c_size_t),
                    ('antennas', ct.POINTER(CAntennaS)),
                    ('num_rf_inputs', ct.c_size_t),
                    ('rf_inputs', ct.POINTER(CRFInputS)),
                    ('num_ant_pols', ct.c_size_t),
                    ('num_baselines', ct.c_size_t),
                    ('baselines', ct.POINTER(CBaselineS)),
                    ('num_visibility_pols', ct.c_size_t),
                    ('num_metafits_coarse_chans', ct.c_size_t),
                    ('metafits_coarse_chans', ct.POINTER(CCoarseChannelS)),
                    ('num_metafits_fine_chan_freqs', ct.c_size_t),
                    ('metafits_fine_chan_freqs_hz', ct.POINTER(ct.c_double)),
                    ('num_metafits_timesteps', ct.c_size_t),
                    ('metafits_timesteps', ct.POINTER(CTimeStepS)),
                    ('obs_bandwidth_hz', ct.c_uint32),
                    ('coarse_chan_width_hz', ct.c_uint32),
                    ('centre_freq_hz', ct.c_uint32),
                    ('metafits_filename', ct.c_char_p)
                    ]

    #
    # mwalib_metafits_metadata_get()
    #
    mwalib_library.mwalib_metafits_metadata_get.argtypes = \
        (ct.POINTER(CMetafitsContextS),  # metafits context pointer OR
         ct.POINTER(CCorrelatorContextS),  # correlator context pointer OR
         ct.POINTER(CVoltageContextS),  # voltage context pointer
         ct.POINTER(ct.POINTER(CMetafitsMetadataS)),  # Pointer to pointer to CMetafitsMetadataS
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_metafits_metadata_get.restype = ct.c_int32

    #
    # mwalib_metafits_metadata_free()
    #
    mwalib_library.mwalib_metafits_metadata_free.argtypes = (ct.POINTER(CMetafitsMetadataS),)
    mwalib_library.mwalib_metafits_metadata_free.restype = ct.c_int32

    #
    # mwalib_correlator_context_new()
    #
    mwalib_library.mwalib_correlator_context_new.argtypes = \
        (ct.c_char_p,  # metafits
         ct.POINTER(ct.c_char_p),  # gpuboxes files array
         ct.c_size_t,  # gpubox count
         ct.POINTER(ct.POINTER(CCorrelatorContextS)),  # Pointer to pointer to CorrelatorContext
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_correlator_context_new.restype = ct.c_int32

    #
    # mwalib_correlator_context_free()
    #
    mwalib_library.mwalib_correlator_context_free.argtypes = (ct.POINTER(CCorrelatorContextS),)
    mwalib_library.mwalib_correlator_context_free.restype = ct.c_int32

    #
    # mwalib_correlator_context_display()
    #
    mwalib_library.mwalib_correlator_context_display.argtypes = (ct.POINTER(CCorrelatorContextS),)
    mwalib_library.mwalib_correlator_context_display.restype = ct.c_int32

    #
    # mwalib_correlator_context_read_by_baseline()
    #
    mwalib_library.mwalib_correlator_context_read_by_baseline.argtypes = \
        (ct.POINTER(CCorrelatorContextS),  # context
         ct.c_size_t,  # input timestep_index
         ct.c_size_t,  # input coarse_chan_index
         ct.POINTER(ct.c_float),  # buffer_ptr
         ct.c_size_t,  # buffer_len
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_correlator_context_read_by_baseline.restype = ct.c_int32

    #
    # mwalib_correlator_context_read_by_frequency()
    #
    mwalib_library.mwalib_correlator_context_read_by_frequency.argtypes = \
        (ct.POINTER(CCorrelatorContextS),  # context
         ct.c_size_t,  # input timestep_index
         ct.c_size_t,  # input coarse_chan_index
         ct.POINTER(ct.c_float),  # buffer_ptr
         ct.c_size_t,  # buffer_len
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_correlator_context_read_by_frequency.restype = ct.c_int32

    #
    # mwalib_correlator_context_get_fine_chan_freqs_hz_array()
    #
    mwalib_library.mwalib_correlator_context_get_fine_chan_freqs_hz_array.argtypes = \
        (ct.POINTER(CCorrelatorContextS),  # context
         ct.POINTER(ct.c_size_t),  # coarse_chan_indices_ptr
         ct.c_size_t,  # coarse_chan_indices_len
         ct.POINTER(ct.c_double),  # buffer_ptr
         ct.c_size_t,  # buffer_len
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_correlator_context_get_fine_chan_freqs_hz_array.restype = ct.c_int32

    #
    # C CorrelatorMetadata struct
    #
    class CCorrelatorMetadataS(ct.Structure):
        _fields_ = [('mwa_version', ct.c_uint32),
                    ('timesteps', ct.POINTER(CTimeStepS)),
                    ('num_timesteps', ct.c_size_t),
                    ('coarse_chans', ct.POINTER(CCoarseChannelS)),
                    ('num_coarse_chans', ct.c_size_t),

                    ('num_common_timesteps', ct.c_size_t),
                    ('common_timestep_indices', ct.POINTER(ct.c_size_t)),
                    ('num_common_coarse_chans', ct.c_size_t),
                    ('common_coarse_chan_indices', ct.POINTER(ct.c_size_t)),
                    ('common_start_unix_time_ms', ct.c_uint64),
                    ('common_end_unix_time_ms', ct.c_uint64),
                    ('common_start_gps_time_ms', ct.c_uint64),
                    ('common_end_gps_time_ms', ct.c_uint64),
                    ('common_duration_ms', ct.c_uint64),
                    ('common_bandwidth_hz', ct.c_uint32),
                    ('num_common_good_timesteps', ct.c_size_t),
                    ('common_good_timestep_indices', ct.POINTER(ct.c_size_t)),
                    ('num_common_good_coarse_chans', ct.c_size_t),
                    ('common_good_coarse_chan_indices', ct.POINTER(ct.c_size_t)),
                    ('common_good_start_unix_time_ms', ct.c_uint64),
                    ('common_good_end_unix_time_ms', ct.c_uint64),
                    ('common_good_start_gps_time_ms', ct.c_uint64),
                    ('common_good_end_gps_time_ms', ct.c_uint64),
                    ('common_good_duration_ms', ct.c_uint64),
                    ('common_good_bandwidth_hz', ct.c_uint32),
                    ('num_provided_timesteps', ct.c_size_t),
                    ('provided_timestep_indices', ct.POINTER(ct.c_size_t)),
                    ('num_provided_coarse_chans', ct.c_size_t),
                    ('provided_coarse_chan_indices', ct.POINTER(ct.c_size_t)),
                    ('num_timestep_coarse_chan_bytes', ct.c_size_t),
                    ('num_timestep_coarse_chan_floats', ct.c_size_t),
                    ('num_gpubox_files', ct.c_size_t)
                    ]

    #
    # mwalib_correlator_metadata_get()
    #
    mwalib_library.mwalib_correlator_metadata_get.argtypes = \
        (ct.POINTER(CCorrelatorContextS),  # correlator context pointer
         ct.POINTER(ct.POINTER(CCorrelatorMetadataS)),  # Pointer to pointer to CCorrelatorMetadataS
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_correlator_metadata_get.restype = ct.c_int32

    #
    # mwalib_correlator_metadata_free()
    #
    mwalib_library.mwalib_correlator_metadata_free.argtypes = (ct.POINTER(CCorrelatorMetadataS),)
    mwalib_library.mwalib_correlator_metadata_free.restype = ct.c_int32

    #
    # C VoltageMetadata struct
    #
    class CVoltageMetadataS(ct.Structure):
        _fields_ = [('mwa_version', ct.c_uint32),
                    ('timesteps', ct.POINTER(CTimeStepS)),
                    ('num_timesteps', ct.c_size_t),
                    ('timestep_duration_ms', ct.c_uint64),
                    ('coarse_chans', ct.POINTER(CCoarseChannelS)),
                    ('num_coarse_chans', ct.c_size_t),
                    ('num_common_timesteps', ct.c_size_t),
                    ('common_timestep_indices', ct.POINTER(ct.c_size_t)),
                    ('num_common_coarse_chans', ct.c_size_t),
                    ('common_coarse_chan_indices', ct.POINTER(ct.c_size_t)),
                    ('common_start_unix_time_ms', ct.c_uint64),
                    ('common_end_unix_time_ms', ct.c_uint64),
                    ('common_start_gps_time_ms', ct.c_uint64),
                    ('common_end_gps_time_ms', ct.c_uint64),
                    ('common_duration_ms', ct.c_uint64),
                    ('common_bandwidth_hz', ct.c_uint32),
                    ('num_common_good_timesteps', ct.c_size_t),
                    ('common_good_timestep_indices', ct.POINTER(ct.c_size_t)),
                    ('num_common_good_coarse_chans', ct.c_size_t),
                    ('common_good_coarse_chan_indices', ct.POINTER(ct.c_size_t)),
                    ('common_good_start_unix_time_ms', ct.c_uint64),
                    ('common_good_end_unix_time_ms', ct.c_uint64),
                    ('common_good_start_gps_time_ms', ct.c_uint64),
                    ('common_good_end_gps_time_ms', ct.c_uint64),
                    ('common_good_duration_ms', ct.c_uint64),
                    ('common_good_bandwidth_hz', ct.c_uint32),
                    ('num_provided_timesteps', ct.c_size_t),
                    ('provided_timestep_indices', ct.POINTER(ct.c_size_t)),
                    ('num_provided_coarse_chans', ct.c_size_t),
                    ('provided_coarse_chan_indices', ct.POINTER(ct.c_size_t)),
                    ('coarse_chan_width_hz', ct.c_uint32),
                    ('fine_chan_width_hz', ct.c_uint32),
                    ('num_fine_chans_per_coarse', ct.c_size_t),
                    ('sample_size_bytes', ct.c_size_t),
                    ('num_voltage_blocks_per_timestep', ct.c_size_t),
                    ('num_voltage_blocks_per_second', ct.c_size_t),
                    ('num_samples_per_voltage_block', ct.c_size_t),
                    ('voltage_block_size_bytes', ct.c_size_t),
                    ('delay_block_size_bytes', ct.c_size_t),
                    ('data_file_header_size_bytes', ct.c_size_t),
                    ('expected_voltage_data_file_size_bytes', ct.c_size_t)
                    ]

    #
    # mwalib_voltage_metadata_get()
    #
    mwalib_library.mwalib_voltage_metadata_get.argtypes = \
        (ct.POINTER(CVoltageContextS),  # voltage context pointer
         ct.POINTER(ct.POINTER(CVoltageMetadataS)),  # Pointer to pointer to CVoltageMetadata
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_voltage_metadata_get.restype = ct.c_int32

    #
    # mwalib_voltage_metadata_free()
    #
    mwalib_library.mwalib_voltage_metadata_free.argtypes = (ct.POINTER(CVoltageMetadataS),)
    mwalib_library.mwalib_voltage_metadata_free.restype = ct.c_int32

    #
    # mwalib_voltage_context_read_file()
    #
    mwalib_library.mwalib_voltage_context_read_file.argtypes = \
        (ct.POINTER(CVoltageContextS),  # context
         ct.c_size_t,  # input timestep_index
         ct.c_size_t,  # input coarse_chan_index
         ct.POINTER(ct.c_byte),  # buffer_ptr
         ct.c_size_t,  # buffer_len
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_voltage_context_read_file.restype = ct.c_int32

    #
    # mwalib_voltage_context_read_second()
    #
    mwalib_library.mwalib_voltage_context_read_second.argtypes = \
        (ct.POINTER(CVoltageContextS),  # context
         ct.c_ulong,  # input gps second start
         ct.c_size_t,  # input gps second count
         ct.c_size_t,  # input coarse_chan_index
         ct.POINTER(ct.c_byte),  # buffer_ptr
         ct.c_size_t,  # buffer_len
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_voltage_context_read_second.restype = ct.c_int32

    #
    # mwalib_voltage_context_get_fine_chan_freqs_hz_array()
    #
    mwalib_library.mwalib_voltage_context_get_fine_chan_freqs_hz_array.argtypes = \
        (ct.POINTER(CVoltageContextS),  # context
         ct.POINTER(ct.c_size_t),  # coarse_chan_indices_ptr
         ct.c_size_t,  # coarse_chan_indices_len
         ct.POINTER(ct.c_double),  # buffer_ptr
         ct.c_size_t,  # buffer_len
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib_library.mwalib_voltage_context_get_fine_chan_freqs_hz_array.restype = ct.c_int32
