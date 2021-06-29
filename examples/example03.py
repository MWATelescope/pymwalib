#!/usr/bin/env python
#
# pymwalib examples/example03 - run through all of pymwalib's objects for a metafits context
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import argparse
from pymwalib.common import MWAVersion
from pymwalib.metafits_context import MetafitsContext
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
    args = parser.parse_args()

    #
    # Create a context and use it for all the examples below
    #
    # The context object will validate the input args and
    # metadata of the observation matches the contents of
    # the gpubox files passed in.
    #
    with MetafitsContext(args.metafits, MWAVersion.CorrLegacy.value) as context:
        # Test the debug "display" method
        print("\n\n\nTesting Display method:")
        context.display()

        # Test printing via repr(context)
        print("\n\n\nTesting metafits context:")
        print(f"{repr(context)}")

        # Test antennas
        print("\n\n\nTesting Antennas:")
        for a in context.antennas:
            print(repr(a))

        # Test baselines
        print("\n\n\nTesting first 5 baselines:")
        for c in range(0, 5):
             print(repr(context.baselines[c]))

        # Test rfinputs
        print("\n\n\nTesting RF Inputs:")
        for r in context.rf_inputs:
            print(repr(r))

        # Test coarse channels
        print("\n\n\nTesting Coarse channels:")
        for c in context.metafits_coarse_chans:
            print(repr(c))

        # Test timesteps
        print("\n\n\nTesting Timesteps:")
        for t in context.metafits_timesteps:
            print(repr(t))
