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
import numpy as np
import os
from pymwalib.voltage_context import VoltageContext
from pymwalib.version import check_mwalib_version
from pymwalib.errors import PymwalibNoDataForTimestepAndCoarseChannelError
import time


def sum_task_by_file(context: VoltageContext, coarse_chan_index: int) -> int:
    total_sum = 0

    print(f"sum_task_by_file: Summing {context.num_timesteps} timesteps "
          f"and coarse channel index {coarse_chan_index}...")

    for t in range(0, context.num_timesteps):
        try:
            print(f"summing t:{t} c:{coarse_chan_index}")
            data = context.read_file(t, coarse_chan_index)
            total_sum += np.sum(data, dtype=np.long)

        except PymwalibNoDataForTimestepAndCoarseChannelError:
            pass

        except Exception as e:
            print(f"Error: {e}")
            exit(-1)

    return total_sum


def sum_by_gps_second(metafits_filename: str, voltage_filenames: list) -> int:
    total_sum = 0

    with VoltageContext(metafits_filename, voltage_filenames) as context:
        for coarse_chan_index in range(0, context.num_coarse_chans):
            print(f"sum_by_gps_second: Summing {context.num_timesteps} timesteps "
                  f"and coarse channel index {coarse_chan_index}...")
            for gps_second in range(context.timesteps[0].gps_time_ms / 1000,
                                    context.timesteps[context.num_timesteps-1].gps_time_ms):
                try:
                    data = context.read_second(gps_second, 1, coarse_chan_index)
                    total_sum += np.sum(data, dtype=np.long)

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
        check_mwalib_version()
    except Exception as e:
        print(e)
        exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--metafits", required=True,
                        help="Path to the metafits file.")
    parser.add_argument("datafiles", nargs='*',
                        help="Paths to the vcs data files.")
    args = parser.parse_args()

    # fast sum using all cores
    num_cores = len(os.sched_getaffinity(0)) - 1
    print(f"Using {num_cores} cores to fast sum all data files...")

    context = VoltageContext(args.metafits, args.datafiles)
    total_sum = 0
    start_time = time.time()
    for c in context.provided_coarse_chans:
        total_sum += np.sum(sum_task_by_file(context, c))
    stop_time = time.time()
    print(f"Sum is: {total_sum} in {stop_time - start_time} seconds.\n")

    # slow sum restricted to one python process
    #start_time_slow = time.time()
    #slow_sum = sum_by_gps_second(args.metafits, args.gpuboxes)
    #stop_time_slow = time.time()
    #print(f"Sum is: {slow_sum} in {stop_time_slow - start_time_slow} seconds.")


