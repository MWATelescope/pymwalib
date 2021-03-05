#!/usr/bin/env python
#
# Common classes and functions
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import enum

ERROR_MESSAGE_LEN = 1024

class CorrelatorVersion(enum.Enum):
    """Enum for Correlator version"""
    # MWAX correlator(v2)
    V2 = 0
    # MWA Legacy correlator(v1), having data files with "gpubox" and batch numbers in their names.
    Legacy = 1
    # MWA Old Legacy correlator(v1), having data files without any batch numbers.
    OldLegacy = 2