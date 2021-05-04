# Change Log

Changes in each release are listed below. Please see MWATelescope/mwalib CHANGELOG for more detailed changes to the underlying mwalib library.

## 0.7.0 04-May-2021 (Pre-release)

* Requires mwalib 0.7.*.
* Added read methods for VoltageContext (to match 0.7.* of mwalib)
* Updated voltage context to match latest 0.7.* mwalib (removed num_samples_per_timestep and added many new descriptive attributes)
* Added paramter type hints to the correlator context read methods
* Added more tests for correlator context
* Updated CI to pip install numpy as some tests now require numpy

## 0.6.0 05-Mar-2021 (Pre-release)

* Requires mwalib 0.6.*.
* Moved coax_v_factor, mwa_lat_radians, mwa_long_radians and mwa_alt_meters out of metafits_metadata and are now constants.

## 0.5.0 04-Mar-2021 (Pre-release)

* Requires mwalib 0.5.1.
* Major refactor to match major refactor in mwalib 0.5.0. This will break compatibility with previous pymwalib versions.
    * Context top level object now split into:
        * MetafitsContext (when you only provide a metafits file)
        * CorrelatorContext (when you provide a metafits and 1 or more gpubox files)
        * VoltageContext (when you provide a metafits and 1 or more voltage files)
* Many new class members added to various classes.

## 0.4.4 08-Jan-2021 (Pre-release)

* Requires mwalib 0.4.4.
* Added receiver_number and receiver_slot_number to rfinput struct.

## 0.3.0 14-May-2020 (Pre-release)

* Requires mwalib 0.3.0.
* Added baseline array.
* Added visibility pol(arisations) array.
* Added extra fields for scheduled end MJD, UTC and Unix times.

## 0.2.0 20-Mar-2020 (Pre-release)

* Requires mwalib 0.2.0.
* Initial pre-release.
