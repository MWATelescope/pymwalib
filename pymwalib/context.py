#!/usr/bin/env python
#
# pymwalib
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
import ctypes as ct
import os
import sys

ERROR_MESSAGE_LEN = 1024


class MwalibContextS(ct.Structure):
    pass


prefix = {"win32": ""}.get(sys.platform, "lib")
extension = {"darwin": ".dylib", "win32": ".dll"}.get(sys.platform, ".so")
path_to_mwalib = os.path.abspath("../mwalib/target/release/" + prefix + "mwalib" + extension)
mwalib = ct.cdll.LoadLibrary(path_to_mwalib)

mwalib.mwalibContext_get.argtypes = \
    (ct.c_char_p,              # metafits
     ct.POINTER(ct.c_char_p),  # gpuboxes
     ct.c_size_t,              # gpubox count
     ct.c_char_p,              # error message
     ct.c_size_t)              # length of error message
mwalib.mwalibContext_get.restype = ct.POINTER(MwalibContextS)

mwalib.mwalibContext_free.argtypes = (ct.POINTER(MwalibContextS), )

mwalib.mwalibContext_display.argtypes = (ct.POINTER(MwalibContextS), )
mwalib.mwalibContext_display.restype = ct.c_uint32


class Context:
    def __init__(self, metafits_filename, gpubox_filenames):
        # Encode all inputs as UTF-8.
        m = ct.c_char_p(metafits_filename.encode("utf-8"))

        # https://stackoverflow.com/questions/4145775/how-do-i-convert-a-python-list-into-a-c-array-by-using-ctypes
        encoded = []
        for g in gpubox_filenames:
            encoded.append(ct.c_char_p(g.encode("utf-8")))
        seq = ct.c_char_p * len(encoded)
        g = seq(*encoded)
        error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN
        self.obj = mwalib.mwalibContext_get(
            m, g, len(encoded), error_message, ERROR_MESSAGE_LEN)

        if not self.obj:
            raise Exception(f"Error creating context: {error_message.decode('utf-8').rstrip()}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        mwalib.mwalibContext_free(self.obj)

    def display(self):
        error_message = " ".encode("utf-8") * ERROR_MESSAGE_LEN

        if mwalib.mwalibContext_display(self.obj, error_message, ERROR_MESSAGE_LEN) != 0:
            raise Exception(f"Error calling mwalibContext_display(): {error_message.decode('utf-8').rstrip()}")
