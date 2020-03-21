#!/usr/bin/env python
#
# context: main interface for pymwalib
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Adapted from:
# http://jakegoulding.com/rust-ffi-omnibus/objects/
#
# Additional documentation:
# https://docs.python.org/3.8/library/ctypes.html#module-ctypes
#


class TimeStep:
    def __init__(self, order: int, unix_time_ms: int):
        self.order = order
        self.unix_time_ms = unix_time_ms

    def __repr__(self):
        return f"Order: {self.order}, UNIX time: {float(self.unix_time_ms) / 1000.}"

    def __str__(self):
        return "pymwalib.TimeStep"
