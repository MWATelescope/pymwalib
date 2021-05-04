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
mwalib = None

try:
    mwalib = ct.cdll.LoadLibrary(mwalib_filename)
except Exception as library_load_err:
    print(f"Error loading {mwalib_filename}. Please check that it is in your system path or in your LD_LIBRARY_PATH "
          f"environment variable. {library_load_err}")

#
# Define the Library functions if the library was loaded
#
if mwalib:
    #
    # mwalib_metafits_context_new()
    #
    mwalib.mwalib_metafits_context_new.argtypes = \
        (ct.c_char_p,                               # metafits
         ct.POINTER(ct.POINTER(CMetafitsContextS)), # Pointer to pointer to CorrelatorContext
         ct.c_char_p,                               # error message
         ct.c_size_t)                               # length of error message

    #
    # mwalib_metafits_context_free()
    #
    mwalib.mwalib_metafits_context_free.argtypes = (ct.POINTER(CMetafitsContextS),)
    mwalib.mwalib_metafits_context_free.restype = ct.c_int32

    #
    # mwalib_metafits_context_display()
    #
    mwalib.mwalib_metafits_context_display.argtypes = (ct.POINTER(CCorrelatorContextS),)
    mwalib.mwalib_metafits_context_display.restype = ct.c_int32


    #
    # C MetafitsMetadata struct
    #
    class CMetafitsMetadataS(ct.Structure):
        _fields_ = [('obs_id', ct.c_uint32),
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
                    ('mode', ct.c_char_p),
                    ('corr_fine_chan_width_hz', ct.c_uint32),
                    ('corr_int_time_ms', ct.c_uint64),
                    ('num_corr_fine_chans_per_coarse', ct.c_size_t),
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
                    ('num_rf_inputs', ct.c_size_t),
                    ('num_ant_pols', ct.c_size_t),
                    ('num_baselines', ct.c_size_t),
                    ('num_visibility_pols', ct.c_size_t),
                    ('num_coarse_chans', ct.c_size_t),
                    ('obs_bandwidth_hz', ct.c_uint32),
                    ('coarse_chan_width_hz', ct.c_uint32),
                    ('centre_freq_hz', ct.c_uint32),
                    ('metafits_filename', ct.c_char_p)
                    ]

    #
    # mwalib_metafits_metadata_get()
    #
    mwalib.mwalib_metafits_metadata_get.argtypes = \
        (ct.POINTER(CMetafitsContextS),                 # metafits context pointer OR
         ct.POINTER(CCorrelatorContextS),               # correlator context pointer OR
         ct.POINTER(CVoltageContextS),                  # voltage context pointer
         ct.POINTER(ct.POINTER(CMetafitsMetadataS)),    # Pointer to pointer to CMetafitsMetadataS
         ct.c_char_p,                                   # error message
         ct.c_size_t)                                   # length of error message
    mwalib.mwalib_metafits_metadata_get.restype = ct.c_int32

    #
    # mwalib_metafits_metadata_free()
    #
    mwalib.mwalib_metafits_metadata_free.argtypes = (ct.POINTER(CMetafitsMetadataS),)
    mwalib.mwalib_metafits_metadata_free.restype = ct.c_int32

    #
    # mwalib_correlator_context_new()
    #
    mwalib.mwalib_correlator_context_new.argtypes = \
        (ct.c_char_p,                                   # metafits
         ct.POINTER(ct.c_char_p),                       # gpuboxes files array
         ct.c_size_t,                                   # gpubox count
         ct.POINTER(ct.POINTER(CCorrelatorContextS)),   # Pointer to pointer to CorrelatorContext
         ct.c_char_p,                                   # error message
         ct.c_size_t)                                   # length of error message
    mwalib.mwalib_correlator_context_new.restype = ct.c_int32

    #
    # mwalib_correlator_context_free()
    #
    mwalib.mwalib_correlator_context_free.argtypes = (ct.POINTER(CCorrelatorContextS),)
    mwalib.mwalib_correlator_context_free.restype = ct.c_int32

    #
    # mwalib_correlator_context_display()
    #
    mwalib.mwalib_correlator_context_display.argtypes = (ct.POINTER(CCorrelatorContextS),)
    mwalib.mwalib_correlator_context_display.restype = ct.c_int32

    #
    # mwalib_correlator_context_read_by_baseline()
    #
    mwalib.mwalib_correlator_context_read_by_baseline.argtypes = \
        (ct.POINTER(CCorrelatorContextS),   # context
         ct.c_size_t,                       # input timestep_index
         ct.c_size_t,                       # input coarse_chan_index
         ct.POINTER(ct.c_float),            # buffer_ptr
         ct.c_size_t,                       # buffer_len
         ct.c_char_p,                       # error message
         ct.c_size_t)                        # length of error message
    mwalib.mwalib_correlator_context_read_by_baseline.restype = ct.c_int32

    #
    # mwalib_correlator_context_read_by_frequency()
    #
    mwalib.mwalib_correlator_context_read_by_frequency.argtypes = \
        (ct.POINTER(CCorrelatorContextS),   # context
         ct.c_size_t,                       # input timestep_index
         ct.c_size_t,                       # input coarse_chan_index
         ct.POINTER(ct.c_float),            # buffer_ptr
         ct.c_size_t,                       # buffer_len
         ct.c_char_p,                       # error message
         ct.c_size_t)                       # length of error message
    mwalib.mwalib_correlator_context_read_by_frequency.restype = ct.c_int32

    #
    # C CorrelatorMetadata struct
    #
    class CCorrelatorMetadataS(ct.Structure):
        _fields_ = [('corr_version', ct.c_uint32),
                    ('start_unix_time_ms', ct.c_uint64),
                    ('end_unix_time_ms', ct.c_uint64),
                    ('start_gps_time_ms', ct.c_uint64),
                    ('end_gps_time_ms', ct.c_uint64),
                    ('duration_ms', ct.c_uint64),
                    ('num_timesteps', ct.c_size_t),
                    ('num_coarse_chans', ct.c_size_t),
                    ('bandwidth_hz', ct.c_uint32),
                    ('num_timestep_coarse_chan_bytes', ct.c_size_t),
                    ('num_timestep_coarse_chan_floats', ct.c_size_t),
                    ('num_gpubox_files', ct.c_size_t)
                    ]
    #
    # mwalib_correlator_metadata_get()
    #
    mwalib.mwalib_correlator_metadata_get.argtypes = \
        (ct.POINTER(CCorrelatorContextS),               # correlator context pointer
         ct.POINTER(ct.POINTER(CCorrelatorMetadataS)),  # Pointer to pointer to CCorrelatorMetadataS
         ct.c_char_p,                                   # error message
         ct.c_size_t)                                   # length of error message
    mwalib.mwalib_correlator_metadata_get.restype = ct.c_int32

    #
    # mwalib_correlator_metadata_free()
    #
    mwalib.mwalib_correlator_metadata_free.argtypes = (ct.POINTER(CCorrelatorMetadataS),)
    mwalib.mwalib_correlator_metadata_free.restype = ct.c_int32

    #
    # C VoltageMetadata struct
    #
    class CVoltageMetadataS(ct.Structure):
        _fields_ = [('corr_version', ct.c_uint32),
                    ('start_gps_time_ms', ct.c_uint64),
                    ('end_gps_time_ms', ct.c_uint64),
                    ('start_unix_time_ms', ct.c_uint64),
                    ('end_unix_time_ms', ct.c_uint64),
                    ('duration_ms', ct.c_uint64),
                    ('num_timesteps', ct.c_size_t),
                    ('timestep_duration_ms', ct.c_uint64),
                    ('num_coarse_chans', ct.c_size_t),
                    ('bandwidth_hz', ct.c_uint32),
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
    mwalib.mwalib_voltage_metadata_get.argtypes = \
        (ct.POINTER(CVoltageContextS),              # voltage context pointer
         ct.POINTER(ct.POINTER(CVoltageMetadataS)), # Pointer to pointer to CVoltageMetadata
         ct.c_char_p,                               # error message
         ct.c_size_t)                               # length of error message
    mwalib.mwalib_voltage_metadata_get.restype = ct.c_int32

    #
    # mwalib_voltage_metadata_free()
    #
    mwalib.mwalib_voltage_metadata_free.argtypes = (ct.POINTER(CVoltageMetadataS),)
    mwalib.mwalib_voltage_metadata_free.restype = ct.c_int32

    #
    # mwalib_voltage_context_read_file()
    #
    mwalib.mwalib_voltage_context_read_file.argtypes = \
        (ct.POINTER(CVoltageContextS),  # context
         ct.c_size_t,  # input timestep_index
         ct.c_size_t,  # input coarse_chan_index
         ct.POINTER(ct.c_byte),  # buffer_ptr
         ct.c_size_t,  # buffer_len
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib.mwalib_voltage_context_read_file.restype = ct.c_int32

    #
    # mwalib_voltage_context_read_second()
    #
    mwalib.mwalib_voltage_context_read_second.argtypes = \
        (ct.POINTER(CVoltageContextS),  # context
         ct.c_ulong,   # input gps second start
         ct.c_size_t,  # input gps second count
         ct.c_size_t,  # input coarse_chan_index
         ct.POINTER(ct.c_byte),  # buffer_ptr
         ct.c_size_t,  # buffer_len
         ct.c_char_p,  # error message
         ct.c_size_t)  # length of error message
    mwalib.mwalib_voltage_context_read_second.restype = ct.c_int32

    #
    # C Antenna struct
    #
    class CAntennaS(ct.Structure):
        _fields_ = [('ant', ct.c_uint32),
                    ('tile_id', ct.c_uint32),
                    ('tile_name', ct.c_char_p),
                    ('rfinput_x', ct.c_size_t),
                    ('rfinput_y', ct.c_size_t),]


    #
    # mwalib_antennas_get()
    #
    mwalib.mwalib_antennas_get.argtypes = \
        (ct.POINTER(CMetafitsContextS),     # metafits context pointer OR
         ct.POINTER(CCorrelatorContextS),   # correlator context pointer OR
         ct.POINTER(CVoltageContextS),      # voltage context pointer
         ct.POINTER(ct.POINTER(CAntennaS)), # out pointer to array of antennas
         ct.POINTER(ct.c_size_t),           # out number of antennas in out array
         ct.c_char_p,                       # error message
         ct.c_size_t)                       # length of error message
    mwalib.mwalib_antennas_get.restype = ct.c_int32

    #
    # mwalib_antennas_free()
    #
    mwalib.mwalib_antennas_free.argtypes = (ct.POINTER(CAntennaS),
                                            ct.c_size_t)  # number of array elements
    mwalib.mwalib_antennas_get.restype = ct.c_int32

    #
    # C Baseline struct
    #
    class CBaselineS(ct.Structure):
        _fields_ = [('ant1_index', ct.c_size_t),
                    ('ant2_index', ct.c_size_t), ]


    #
    # mwalib_baselines_get()
    #
    mwalib.mwalib_baselines_get.argtypes = \
        (ct.POINTER(CMetafitsContextS),         # metafits context pointer OR
         ct.POINTER(CCorrelatorContextS),       # correlator context pointer OR
         ct.POINTER(CVoltageContextS),          # voltage context pointer
         ct.POINTER(ct.POINTER(CBaselineS)),    # out pointer to array of baselines
         ct.POINTER(ct.c_size_t),               # out number of baselines in out array
         ct.c_char_p,                           # error message
         ct.c_size_t)                           # length of error message
    mwalib.mwalib_baselines_get.restype = ct.c_int32

    #
    # mwalib_correlator_baselines_free()
    #
    mwalib.mwalib_baselines_free.argtypes = (ct.POINTER(CBaselineS),
                                                        ct.c_size_t)  # number of array elements
    mwalib.mwalib_baselines_free.restype = ct.c_int32

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
    # mwalib_correlator_coarse_channels_get()
    #
    mwalib.mwalib_correlator_coarse_channels_get.argtypes = \
        (ct.POINTER(CCorrelatorContextS),           # context_ptr
         ct.POINTER(ct.POINTER(CCoarseChannelS)),   # out pointer to array of coarse channels
         ct.POINTER(ct.c_size_t),                   # out number of coarse channels in out array
         ct.c_char_p,                               # error message
         ct.c_size_t)                               # length of error message
    mwalib.mwalib_correlator_coarse_channels_get.restype = ct.c_int32

    #
    # mwalib_voltage_coarse_channels_get()
    #
    mwalib.mwalib_voltage_coarse_channels_get.argtypes = \
        (ct.POINTER(CCorrelatorContextS),           # context_ptr
         ct.POINTER(ct.POINTER(CCoarseChannelS)),   # out pointer to array of coarse channels
         ct.POINTER(ct.c_size_t),                   # out number of coarse channels in out array
         ct.c_char_p,                               # error message
         ct.c_size_t)                               # length of error message
    mwalib.mwalib_voltage_coarse_channels_get.restype = ct.c_int32

    #
    # mwalib_coarse_channels_free()
    #
    mwalib.mwalib_coarse_channels_free.argtypes = (ct.POINTER(CCoarseChannelS),
                                                   ct.c_size_t)  # number of array elements
    mwalib.mwalib_coarse_channels_free.restype = ct.c_int32

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
                    ('rec_number', ct.c_uint32),
                    ('rec_slot_number', ct.c_uint32)]

    #
    # mwalib_rfinputs_get()
    #
    mwalib.mwalib_rfinputs_get.argtypes = \
        (ct.POINTER(CMetafitsContextS),     # metafits context pointer OR
         ct.POINTER(CCorrelatorContextS),   # correlator context pointer OR
         ct.POINTER(CVoltageContextS),      # voltage context pointer
         ct.POINTER(ct.POINTER(CRFInputS)), # out pointer to array of rfinputs
         ct.POINTER(ct.c_size_t),           # out number of rfinputs in out array
         ct.c_char_p,                       # error message
         ct.c_size_t)                       # length of error message
    mwalib.mwalib_rfinputs_get.restype = ct.c_int32

    #
    # mwalib_rfinputs_free()
    #
    mwalib.mwalib_rfinputs_free.argtypes = (ct.POINTER(CRFInputS),
                                            ct.c_size_t)             # number of array elements
    mwalib.mwalib_rfinputs_free.restype = ct.c_int32


    #
    # C TimeStep struct
    #
    class CTimeStepS(ct.Structure):
        _fields_ = [('unix_time_ms', ct.c_uint64),
                    ('gps_time_ms', ct.c_uint64),]

    #
    # mwalib_correlator_timesteps_get()
    #
    mwalib.mwalib_correlator_timesteps_get.argtypes = \
        (ct.POINTER(CCorrelatorContextS),       # correlator context pointer
         ct.POINTER(ct.POINTER(CTimeStepS)),    # out pointer to array of timesteps
         ct.POINTER(ct.c_size_t),               # out number of timesteps in out array
         ct.c_char_p,                           # error message
         ct.c_size_t)                           # length of error message
    mwalib.mwalib_correlator_timesteps_get.restype = ct.c_int32

    #
    # mwalib_voltage_timesteps_get()
    #
    mwalib.mwalib_voltage_timesteps_get.argtypes = \
        (ct.POINTER(CVoltageContextS),          # voltage context pointer
         ct.POINTER(ct.POINTER(CTimeStepS)),    # out pointer to array of timesteps
         ct.POINTER(ct.c_size_t),                 # out number of timesteps in out array
         ct.c_char_p,                           # error message
         ct.c_size_t)                           # length of error message
    mwalib.mwalib_voltage_timesteps_get.restype = ct.c_int32

    #
    # mwalib_timesteps_free()
    #
    mwalib.mwalib_timesteps_free.argtypes = (ct.POINTER(CTimeStepS),
                                             ct.c_size_t)             # number of array elements
    mwalib.mwalib_timesteps_free.restype = ct.c_int32

    #
    # C VisibilityPol struct
    #
    class CVisibilityPolS(ct.Structure):
        _fields_ = [('polarisation', ct.c_char_p), ]

    #
    # mwalib_visibility_pols_get()
    #
    mwalib.mwalib_visibility_pols_get.argtypes = \
        (ct.POINTER(CMetafitsContextS),             # metafits context pointer OR
         ct.POINTER(CCorrelatorContextS),           # correlator context pointer OR
         ct.POINTER(CVoltageContextS),              # voltage context pointer
         ct.POINTER(ct.POINTER(CVisibilityPolS)),   # out pointer to array of timesteps
         ct.POINTER(ct.c_size_t),                   # out number of timesteps in out array
         ct.c_char_p,                               # error message
         ct.c_size_t)                               # length of error message
    mwalib.mwalib_visibility_pols_get.restype = ct.c_int32

    #
    # mwalibVisibilityPol.free()
    #
    mwalib.mwalib_visibility_pols_free.argtypes = (ct.POINTER(CVisibilityPolS),
                                                   ct.c_size_t)  # number of array elements
    mwalib.mwalib_visibility_pols_free.restype = ct.c_int32
