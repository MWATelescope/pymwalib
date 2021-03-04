# Change Log

Changes in each release are listed below. Please see MWATelescope/mwalib CHANGELOG for more detailed changes to the underlying mwalib library.

## 0.5.0 04-Mar-2021 (Pre-release)

* Requires mwalib 0.5.0.
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
