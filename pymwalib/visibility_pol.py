#!/usr/bin/env python
#
# visibility_pol: class representing a single visibility_pol in mwalib
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


class VisibilityPol:
    """
    A class representing a single mwalibVisibilityPol

    Attributes
    ----------
    index : int
        Ordinal index of this visibility pol.

    polarisation : str
        The polarisation of this object- e.g. "XX", "XY", "YX" or "YY"

    """

    def __init__(self,
                 index: int,
                 polarisation: str):
        """Initialise the class"""
        self.index: int = index
        self.polarisation: str = polarisation

    def __repr__(self):
        """Returns a representation of the class"""
        return f"{self.__class__.__name__}(" \
               f"Order: {self.index}, " \
               f"UNIX time: {self.polarisation})"
