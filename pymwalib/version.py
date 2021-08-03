#!/usr/bin/env python
#
# Version handling for pymwalib
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from .mwalib import mwalib_library
from .errors import PymwalibMwalibVersionNotCompatibleError

"""Returns the major, minor and patch version of pymwalib as a string"""


def get_pymwalib_version_string() -> str:
    import pkg_resources  # part of setuptools
    package_version = pkg_resources.require("pymwalib")[0].version
    return package_version


"""Returns the major, minor and patch version of mwalib as a string"""


def get_mwalib_version_string() -> str:
    mwalib_major = mwalib_library.mwalib_get_version_major()
    mwalib_minor = mwalib_library.mwalib_get_version_minor()
    mwalib_patch = mwalib_library.mwalib_get_version_patch()

    return f"{mwalib_major}.{mwalib_minor}.{mwalib_patch}"


"""Returns a the major, minor and patch version of pymwalib"""


def get_pymwalib_version_number() -> (int, int, int):
    version = get_pymwalib_version_string()
    try:
        return int(version.split(".")[0]), int(version.split(".")[1]), int(version.split(".")[2])
    except Exception as e:
        raise Exception(f"Unabled to determine pymwalib version: Got {version} which could not be parsed. Error: {e}")


"""Checks, using semantic versioning, that mwalib is compatible with pymwalib. If so, returns, otherwise raises an execption"""


def check_mwalib_version():
    # Perform a version check before going too far
    mwalib_major = mwalib_library.mwalib_get_version_major()
    mwalib_minor = mwalib_library.mwalib_get_version_minor()
    mwalib_patch = mwalib_library.mwalib_get_version_patch()

    pymwalib_version = get_pymwalib_version_number()
    pymwalib_major = pymwalib_version[0]
    pymwalib_minor = pymwalib_version[1]
    pymwalib_patch = pymwalib_version[2]

    # Use semantic rules to determine compatibility
    # if major versions don't match then we are not compatible
    if mwalib_major != pymwalib_major:
        raise PymwalibMwalibVersionNotCompatibleError(f"pymwalib version {pymwalib_major}.{pymwalib_minor}.* is not "
                                                      f"compatible with mwalib {mwalib_major}.{mwalib_minor}.*")

    # pre release rules also apply to major version 0
    # if ANY part of versions don't match then we are not compatible
    if mwalib_major == 0:
        if mwalib_minor != pymwalib_minor:
            raise PymwalibMwalibVersionNotCompatibleError(f"pymwalib version "
                                                          f"{pymwalib_major}.{pymwalib_minor}.{pymwalib_patch} is not "
                                                          f"compatible with mwalib "
                                                          f"{mwalib_major}.{mwalib_minor}.{mwalib_patch}")
