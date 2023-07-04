#!/usr/bin/env python
#
# pymwalib examples/sum-vcs - utilise all cores to sum the vcs data files and compare against single threaded
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# NOTE: this example requires numpy and joblib packages. These can be installed via pip.
# e.g. pip install numpy
#      pip install joblib
#
import argparse
import time

import numpy as np

from pymwalib.errors import PymwalibNoDataForTimestepAndCoarseChannelError
from pymwalib.version import (
    check_mwalib_version,
    get_mwalib_version_string,
    get_pymwalib_version_string,
)
from pymwalib.voltage_context import VoltageContext


def sum_by_file(
    context: VoltageContext, timestep_index: int, coarse_chan_index: int
) -> int:
    total_sum = 0

    freq = context.coarse_channels[coarse_chan_index].chan_centre_hz / 10**6
    rec_chan = context.coarse_channels[coarse_chan_index].rec_chan_number

    try:
        ndarray_i8 = context.read_file(timestep_index, coarse_chan_index)
        total_sum = ndarray_i8.sum(dtype=np.longlong)
        print(
            f"coarse chan: {coarse_chan_index} @ {freq} MHz (ch{rec_chan});"
            " time:"
            f" {int(context.timesteps[timestep_index].gps_time_ms/1000)} ="
            f" {total_sum}"
        )

    except PymwalibNoDataForTimestepAndCoarseChannelError:
        pass

    except Exception as e:
        print(f"Error: {e}")
        exit(-1)

    return total_sum


def sum_by_gps_second(
    context: VoltageContext,
    gps_start_sec: int,
    gps_end_sec: int,
    gps_seconds_count: int,
    coarse_chan_index: int,
) -> int:
    total_sum = 0

    freq = context.coarse_channels[coarse_chan_index].chan_centre_hz / 10**6
    rec_chan = context.coarse_channels[coarse_chan_index].rec_chan_number

    try:
        ndarray_i8 = context.read_second(
            gps_start_sec, gps_seconds_count, coarse_chan_index
        )
        total_sum = ndarray_i8.sum(dtype=np.longlong)
        print(
            f"coarse chan: {coarse_chan_index} @ {freq} MHz (ch{rec_chan});"
            f" time: {gps_start_sec} = {total_sum}"
        )

    except PymwalibNoDataForTimestepAndCoarseChannelError:
        pass

    except Exception as e:
        print(f"Error: {e}")
        exit(-1)

    return total_sum


if __name__ == "__main__":
    # ensure we have a compatible mwalib first
    # You can skip this if you want, but your first pymwalib call will raise an error. Best trap it here
    # and provide a nice user message
    try:
        print(
            f"sum_vcs.py:\nUsing mwalib: v{get_mwalib_version_string()} and"
            f" pymwalib: v{get_pymwalib_version_string()}\n"
        )
        check_mwalib_version()
    except Exception as e:
        print(e)
        exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--metafits", required=True, help="Path to the metafits file."
    )
    parser.add_argument(
        "datafiles", nargs="*", help="Paths to the vcs data files."
    )
    args = parser.parse_args()

    context = VoltageContext(args.metafits, args.datafiles)

    # Quick sanity check
    print(f"Obs Id: {context.metafits_context.obs_id}")
    print(f"Provided Timesteps: {context.num_provided_timesteps}")
    print(f"Provided Coarse Channles: {context.num_provided_coarse_chans}")

    if context.num_provided_timesteps == 0:
        print("Error no timestemps to sum!")
        exit(-1)

    if context.num_provided_coarse_chans == 0:
        print("Error no coarse channels to sum!")
        exit(-1)

    # Get the gpstime of the first timestep (based on files provided)
    start_gpstime_sec = int(
        context.timesteps[context.provided_timestep_indices[0]].gps_time_ms
        / 1000
    )

    # Get the gpstime of the last timestep (based on files provided)
    end_gpstime_sec = (
        int(
            (
                context.timesteps[
                    context.provided_timestep_indices[
                        context.num_provided_timesteps - 1
                    ]
                ].gps_time_ms
                + context.timestep_duration_ms
            )
            / 1000
        )
        - 1
    )

    # Calculate the number of GPS seconds provided
    gps_seconds_count = context.num_provided_timesteps * int(
        context.timestep_duration_ms / 1000
    )

    print(
        f"Summing {start_gpstime_sec} to"
        f" {end_gpstime_sec} ({gps_seconds_count} seconds)"
    )

    #
    # pymwalib provides 2 methods for getting to the data- we'll test both
    #

    # sum by file
    print("Sum_by_file...")
    total_sum_by_file = 0
    start_time = time.time()
    for t in range(0, len(context.provided_timestep_indices)):
        for c in range(0, len(context.provided_coarse_chan_indices)):
            total_sum_by_file += np.sum(
                sum_by_file(
                    context,
                    context.provided_timestep_indices[t],
                    context.provided_coarse_chan_indices[c],
                )
            )
    stop_time = time.time()
    print(
        f"Sum is: {total_sum_by_file} in {stop_time - start_time} seconds.\n"
    )

    # sum by gps second
    print("Sum_by_gps_second")
    total_sum_by_gps = 0
    start_time = time.time()

    for t in range(0, len(context.provided_timestep_indices)):
        for c in range(0, len(context.provided_coarse_chan_indices)):
            this_gpstime = int(
                context.timesteps[
                    context.provided_timestep_indices[t]
                ].gps_time_ms
                / 1000
            )

            total_sum_by_gps += sum_by_gps_second(
                context,
                this_gpstime,
                this_gpstime + int(context.timestep_duration_ms / 1000),
                int(context.timestep_duration_ms / 1000),
                context.provided_coarse_chan_indices[c],
            )
    stop_time = time.time()
    print(f"Sum is: {total_sum_by_gps} in {stop_time - start_time} seconds.")

    if total_sum_by_gps == total_sum_by_file:
        print("\nSUMS MATCH OK")
    else:
        print("\nWARNING: Sums do not match!")
