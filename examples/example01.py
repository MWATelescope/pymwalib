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

if __name__ == "__main__":
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

        print("\n\n\nTesting Context correlator metadata:")
        print(f"{repr(context.correlator_metadata)}")

        # Test antennas
        print("\n\n\nTesting Antennas:")
        for a in context.antennas:
            print(repr(a))

        # Test baselines
        print("\n\n\nTesting first 5 baselines:")
        for c in range(0, 5):
             print(repr(context.baselines[c]))

        # Test coarse channels
        print("\n\n\nTesting Coarse channels:")
        for c in context.coarse_channels:
            print(repr(c))

        # Test rfinputs
        print("\n\n\nTesting RF Inputs:")
        for r in context.rfinputs:
            print(repr(r))

        # Test timesteps
        print("\n\n\nTesting Timesteps:")
        for t in context.timesteps:
            print(repr(t))

        # Test visibility pols
        print("\n\n\nTesting visibility pols:")
        for c in context.visibility_pols:
            print(repr(c))

        # Test the debug "display" method
        print("\n\n\nTesting Display method:")
        context.display()

        # Sum the data by baseline
        print(f"\n\n\nSumming {context.correlator_metadata.num_timesteps} timesteps "
              f"and {context.correlator_metadata.num_coarse_chans} coarse channels...")

        total_sum = 0
        for timestep_index in range(0, context.correlator_metadata.num_timesteps):
             this_sum = 0

             for coarse_chan_index in range(0, context.correlator_metadata.num_coarse_chans):
                 try:
                     data = context.read_by_baseline(timestep_index,
                                                     coarse_chan_index)
                 except Exception as e:
                     print(f"Error: {e}")
                     exit(-1)

                 this_sum = np.sum(data, dtype=np.float64)

                 total_sum += this_sum
        print("Total sum by baseline:  {}".format(total_sum))

        # Sum the data by frequency
        total_sum = 0
        for timestep_index in range(0, context.correlator_metadata.num_timesteps):
             this_sum = 0

             for coarse_chan_index in range(0, context.correlator_metadata.num_coarse_chans):
                 try:
                     data = context.read_by_frequency(timestep_index,
                                                      coarse_chan_index)
                 except Exception as e:
                     print(f"Error: {e}")
                     exit(-1)

                 this_sum = np.sum(data, dtype=np.float64)

                 total_sum += this_sum
        print("Total sum by frequency: {}".format(total_sum))
