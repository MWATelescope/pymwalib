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
# CmwalibContextS struct
#
class CmwalibContextS(ct.Structure):
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
    # mwalibContext.get()
    #
    mwalib.mwalibContext_get.argtypes = \
        (ct.c_char_p,              # metafits
         ct.POINTER(ct.c_char_p),  # gpuboxes
         ct.c_size_t,              # gpubox count
         ct.c_char_p,              # error message
         ct.c_size_t)              # length of error message
    mwalib.mwalibContext_get.restype = ct.POINTER(CmwalibContextS)

    mwalib.mwalibContext_free.argtypes = (ct.POINTER(CmwalibContextS), )

    #
    # mwalibContext.display()
    #
    mwalib.mwalibContext_display.argtypes = (ct.POINTER(CmwalibContextS), )
    mwalib.mwalibContext_display.restype = ct.c_uint32

    #
    # mwalibContext.read_by_baseline()
    #
    mwalib.mwalibContext_read_by_baseline.argtypes = \
        (ct.POINTER(CmwalibContextS), # context
         ct.c_size_t,                # input timestep_index
         ct.c_size_t,                # input coarse_channel_index
         ct.POINTER(ct.c_float),     # buffer_ptr
         ct.c_size_t)                # buffer_len
    mwalib.mwalibContext_read_by_baseline.restype = ct.c_int32

    #
    # mwalibContext.read_by_frequency()
    #
    mwalib.mwalibContext_read_by_frequency.argtypes = \
        (ct.POINTER(CmwalibContextS), # context
         ct.c_size_t,                # input timestep_index
         ct.c_size_t,                # input coarse_channel_index
         ct.POINTER(ct.c_float),     # buffer_ptr
         ct.c_size_t)                # buffer_len
    mwalib.mwalibContext_read_by_frequency.restype = ct.c_int32


    #
    # CmwalibMetadata struct
    #
    class CmwalibMetadata(ct.Structure):
        _fields_ = [('obsid', ct.c_uint32),
                    ('corr_version', ct.c_uint32),
                    ('mwa_latitude_radians', ct.c_double),
                    ('mwa_longitude_radians',  ct.c_double),
                    ('mwa_altitude_metres', ct.c_double),
                    ('coax_v_factor', ct.c_double),
                    ('global_analogue_attenuation_db', ct.c_double),
                    ('ra_tile_pointing_degrees', ct.c_double),
                    ('dec_tile_pointing_degrees', ct.c_double),
                    ('ra_phase_center_degrees', ct.c_double),
                    ('dec_phase_center_degrees', ct.c_double),
                    ('azimuth_degrees', ct.c_double),
                    ('altitude_degrees', ct.c_double),
                    ('sun_altitude_degrees', ct.c_double),
                    ('sun_distance_degrees', ct.c_double),
                    ('moon_distance_degrees', ct.c_double),
                    ('jupiter_distance_degrees', ct.c_double),
                    ('lst_degrees', ct.c_double),
                    ('hour_angle_string', ct.c_char_p),
                    ('grid_name', ct.c_char_p),
                    ('grid_number', ct.c_int32),
                    ('creator', ct.c_char_p),
                    ('project_id', ct.c_char_p),
                    ('observation_name', ct.c_char_p),
                    ('mode', ct.c_char_p),
                    ('scheduled_start_utc', ct.c_uint64),
                    ('scheduled_end_utc', ct.c_uint64),
                    ('scheduled_start_mjd', ct.c_double),
                    ('scheduled_end_mjd', ct.c_double),
                    ('scheduled_start_unix_time_milliseconds', ct.c_uint64),
                    ('scheduled_end_unix_time_milliseconds', ct.c_uint64),
                    ('scheduled_duration_milliseconds', ct.c_uint64),
                    ('quack_time_duration_milliseconds', ct.c_uint64),
                    ('good_time_unix_milliseconds', ct.c_uint64),
                    ('start_unix_time_milliseconds', ct.c_uint64),
                    ('end_unix_time_milliseconds', ct.c_uint64),
                    ('duration_milliseconds', ct.c_uint64),
                    ('num_timesteps', ct.c_size_t),
                    ('num_antennas', ct.c_size_t),
                    ('num_baselines', ct.c_size_t),
                    ('num_rf_inputs', ct.c_size_t),
                    ('num_antenna_pols', ct.c_size_t),
                    ('num_visibility_pols', ct.c_size_t),
                    ('num_coarse_channels', ct.c_size_t),
                    ('integration_time_milliseconds', ct.c_uint64),
                    ('fine_channel_width_hz', ct.c_uint32),
                    ('observation_bandwidth_hz', ct.c_uint32),
                    ('coarse_channel_width_hz', ct.c_uint32),
                    ('num_fine_channels_per_coarse', ct.c_size_t),
                    ('num_timestep_coarse_channel_bytes', ct.c_size_t),
                    ('num_timestep_coarse_channel_floats', ct.c_size_t),
                    ('num_gpubox_files', ct.c_size_t)
                    ]


    #
    # mwalibMetadata.get()
    #
    mwalib.mwalibMetadata_get.argtypes = \
        (ct.POINTER(CmwalibContextS),  # context_ptr
         ct.c_char_p,                 # error message
         ct.c_size_t)                 # length of error message
    mwalib.mwalibMetadata_get.restype = ct.c_void_p

    mwalib.mwalibMetadata_free.argtypes = (ct.POINTER(CmwalibMetadata),)


    #
    # CmwalibTimeStep struct
    #
    class CmwalibTimeStep(ct.Structure):
        _fields_ = [('unix_time_ms', ct.c_uint64),]


    #
    # mwalibTimeStep.get()
    #
    mwalib.mwalibTimeStep_get.argtypes = \
        (ct.POINTER(CmwalibContextS),  # context_ptr
         ct.c_size_t,                  # input timestep_index
         ct.c_char_p,                  # error message
         ct.c_size_t)                  # length of error message
    mwalib.mwalibTimeStep_get.restype = ct.c_void_p

    #
    # mwalibTimeStep.free()
    #
    mwalib.mwalibTimeStep_free.argtypes = (ct.POINTER(CmwalibTimeStep),)


    #
    # CmwalibRFInput struct
    #
    class CmwalibRFInput(ct.Structure):
        _fields_ = [('input', ct.c_uint32),
                    ('antenna', ct.c_uint32),
                    ('tile_id', ct.c_uint32),
                    ('tile_name', ct.c_char_p),
                    ('pol', ct.c_char_p),
                    ('electrical_length_m', ct.c_double),
                    ('north_m', ct.c_double),
                    ('east_m', ct.c_double),
                    ('height_m', ct.c_double),
                    ('vcs_order', ct.c_uint32),
                    ('subfile_order', ct.c_uint32),
                    ('flagged', ct.c_bool),]


    #
    # mwalibRFInput.get()
    #
    mwalib.mwalibRFInput_get.argtypes = \
        (ct.POINTER(CmwalibContextS),  # context_ptr
         ct.c_size_t,                  # input rfinput_index
         ct.c_char_p,                  # error message
         ct.c_size_t)                  # length of error message
    mwalib.mwalibRFInput_get.restype = ct.c_void_p

    #
    # mwalibRFInput.free()
    #
    mwalib.mwalibRFInput_free.argtypes = (ct.POINTER(CmwalibRFInput),)


    #
    # CmwalibAntenna struct
    #
    class CmwalibAntenna(ct.Structure):
        _fields_ = [('antenna', ct.c_uint32),
                    ('tile_id', ct.c_uint32),
                    ('tile_name', ct.c_char_p),]


    #
    # mwalibAntenna.get()
    #
    mwalib.mwalibAntenna_get.argtypes = \
        (ct.POINTER(CmwalibContextS),  # context_ptr
         ct.c_size_t,                  # input antenna_index
         ct.c_char_p,                  # error message
         ct.c_size_t)                  # length of error message
    mwalib.mwalibAntenna_get.restype = ct.c_void_p

    #
    # mwalibAntenna.free()
    #
    mwalib.mwalibAntenna_free.argtypes = (ct.POINTER(CmwalibAntenna),)


    #
    # CmwalibCoarseChannel struct
    #
    class CmwalibCoarseChannel(ct.Structure):
        _fields_ = [('correlator_channel_number', ct.c_size_t),
                    ('receiver_channel_number', ct.c_size_t),
                    ('gpubox_number', ct.c_size_t),
                    ('channel_width_hz', ct.c_uint32),
                    ('channel_start_hz', ct.c_uint32),
                    ('channel_centre_hz', ct.c_uint32),
                    ('channel_end_hz', ct.c_uint32),]


    #
    # mwalibCoarseChannel.get()
    #
    mwalib.mwalibCoarseChannel_get.argtypes = \
        (ct.POINTER(CmwalibContextS),  # context_ptr
         ct.c_size_t,                  # input antenna_index
         ct.c_char_p,                  # error message
         ct.c_size_t)                  # length of error message
    mwalib.mwalibCoarseChannel_get.restype = ct.c_void_p

    #
    # mwalibCoarseChannel.free()
    #
    mwalib.mwalibCoarseChannel_free.argtypes = (ct.POINTER(CmwalibCoarseChannel),)


    #
    # CmwalibBaseline struct
    #
    class CmwalibBaseline(ct.Structure):
        _fields_ = [('antenna1_index', ct.c_size_t),
                    ('antenna2_index', ct.c_size_t), ]


    #
    # mwalibBaseline.get()
    #
    mwalib.mwalibBaseline_get.argtypes = \
        (ct.POINTER(CmwalibContextS),  # context_ptr
         ct.c_size_t,                  # input baseline_index
         ct.c_char_p,                  # error message
         ct.c_size_t)                  # length of error message
    mwalib.mwalibBaseline_get.restype = ct.c_void_p

    #
    # mwalibBaseline.free()
    #
    mwalib.mwalibBaseline_free.argtypes = (ct.POINTER(CmwalibBaseline),)

    #
    # CmwalibVisibilityPol struct
    #
    class CmwalibVisibilityPol(ct.Structure):
        _fields_ = [('polarisation', ct.c_char_p), ]


    #
    # mwalibVisibilityPol.get()
    #
    mwalib.mwalibVisibilityPol_get.argtypes = \
        (ct.POINTER(CmwalibContextS),  # context_ptr
         ct.c_size_t,                  # input visibility_pol_index
         ct.c_char_p,                  # error message
         ct.c_size_t)                  # length of error message
    mwalib.mwalibVisibilityPol_get.restype = ct.c_void_p

    #
    # mwalibVisibilityPol.free()
    #
    mwalib.mwalibVisibilityPol_free.argtypes = (ct.POINTER(CmwalibVisibilityPol),)
