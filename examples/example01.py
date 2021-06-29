#!/usr/bin/env python
#
# pymwalib examples/example01 - run through all of pymwalib's objects
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import argparse
import numpy as np
from pymwalib.correlator_context import CorrelatorContext
from pymwalib.errors import PymwalibNoDataForTimestepAndCoarseChannel
from pymwalib.version import check_mwalib_version

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
    parser.add_argument("gpuboxes", nargs='*',
                        help="Paths to the gpubox files.")
    args = parser.parse_args()

    #
    # Create a context and use it for all the examples below
    #
    # The context object will validate the input args and
    # metadata of the observation matches the contents of
    # the gpubox files passed in.
    #
    with CorrelatorContext(args.metafits, args.gpuboxes) as context:
        # Test printing via repr(context)
        print("\n\n\nTesting Context metafits metadata:")
        print(f"{repr(context.metafits_metadata)}")

        # Test antennas
        print("\n\n\nTesting Antennas:")
        for a in context.metafits_metadata.antennas:
            print(repr(a))

        # Test baselines
        print("\n\n\nTesting first 5 baselines:")
        for c in range(0, 5):
             print(repr(context.metafits_metadata.baselines[c]))

        # Test rfinputs
        print("\n\n\nTesting RF Inputs:")
        for r in context.metafits_metadata.rf_inputs:
            print(repr(r))

        # Test coarse channels
        print("\n\n\nTesting Coarse channels:")
        for c in context.coarse_channels:
            print(repr(c))

        # Test timesteps
        print("\n\n\nTesting Timesteps:")
        for t in context.timesteps:
            print(repr(t))

        # Test the debug "display" method
        print("\n\n\nTesting Display method:")
        context.display()

        # Sum the data by baseline
        print(f"\n\n\nSumming {context.num_timesteps} timesteps "
              f"and {context.num_coarse_chans} coarse channels...")

        total_sum = 0
        for timestep_index in range(0, context.num_timesteps):
             this_sum = 0

             for coarse_chan_index in range(0, context.num_coarse_chans):
                 try:
                     data = context.read_by_baseline(timestep_index,
                                                     coarse_chan_index)
                     total_sum += np.sum(data, dtype=np.float64)

                 except PymwalibNoDataForTimestepAndCoarseChannel:
                     pass

                 except Exception as e:
                     print(f"Error: {e}")
                     exit(-1)

        print("Total sum by baseline:  {}".format(total_sum))

        # Sum the data by frequency
        total_sum = 0
        for timestep_index in range(0, context.num_timesteps):
             this_sum = 0

             for coarse_chan_index in range(0, context.num_coarse_chans):
                 try:
                     data = context.read_by_frequency(timestep_index,
                                                      coarse_chan_index)
                     total_sum += np.sum(data, dtype=np.float64)

                 except PymwalibNoDataForTimestepAndCoarseChannel:
                     pass

                 except Exception as e:
                     print(f"Error: {e}")
                     exit(-1)

        print("Total sum by frequency: {}".format(total_sum))
