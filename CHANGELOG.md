# Change Log

Changes in each release are listed below. Please see MWATelescope/mwalib CHANGELOG for more detailed changes to the underlying mwalib library.

## 0.11.0 28-Oct-2021 (Pre-release)

* Requires mwalib 0.11.*.
* Added corr_raw_scale_factor to metafits metadata.

## 0.9.1 11-Aug-2021 (Pre-release)

* Requires mwalib 0.9.*.
* Added mwa_version to MetafitsContext.
* When working only with a MetafitsContext, None can be passed in lieu of an MWAVersion, and mwalib will attempt to determine the correct MWAVersion based on the MODE keyword from the metafits file.
* Added method get_expected_volt_filename() function to MetafitsContext.
* Added digital_gains, dipole_gains and dipole_delays Rfinput.
* Added receivers, delays to MetafitsContext.

## 0.8.8 03-Aug-2021 (Pre-release)

* Requires mwalib 0.8.7.
* Release to fix issue with pypi deployment.
* Pymwalib now only has to match mwalib major and minor version, not patch version. This allows more flexibility in releases.
* No other changes.

## 0.8.7 03-Aug-2021 (Pre-release)

* Requires mwalib 0.8.7.
* Updated API to match mwalib v0.8.7.
* Added helper function get_fine_chan_freqs_hz_array to correlator context and voltage context.
* Added metafits_context.num_metafits_fine_chan_freqs & metafits_context.metafits_fine_chan_freqs_hz, providing a list of sky frequencies for all fine channels.
* Added metafits_context.volt_fine_chan_width_hz & metafits_context.num_volt_fine_chans_per_coarse to describe the voltage fine channel configuration.

## 0.8.4 15-Jul-2021 (Pre-release)

* Requires mwalib 0.8.4.
* Bumped version for new mwalib version compatibility.

## 0.8.3 01-Jul-2021 (Pre-release)

* Requires mwalib 0.8.3.
* Major refactoring of classes to be more consisten with mwalib, please see mwalib release notes for changes in the base library.
  * `CorrelatorContext` and `VoltageContext` classes now have a metafits_context attribute containing the metafits attributes.
  * Thus lists such as `rf_inputs`, `baselines`, `antennas` are now accessed via the metafits_context.
  * MetafitsContext now has `metafits_timesteps` and `metafits_coarse_chans` which reflect those provided by the metafits file.
  * In order to assist users make sense of the data files provided, CorrelatorContext and VoltageContext have `common`, `common_good` and `provided` lists of indices. See [mwalib wiki: Key Concepts](https://github.com/MWATelescope/mwalib/wiki/Key-Concepts) for an explanation of these terms.

## 0.8.2 14-Jun-2021 (Pre-release)

* Requires mwalib 0.8.2.
* mwalib version is now checked upon creating an instance of MetafitsContext, CorrelatorContext or VoltageContext
* pymwalib.version.check_mwalib_version() is exposed so callers can check and handle version incompatibility before using a context object.  
* Antenna now includes electrical length and north,east,height attributes
* MetafitsContext now has metafits_timesteps and metafits_coarse channels based on the metafits file only
* CorrelatorContext and VoltageContext now have timesteps and coarse channels based on a superset of data files provided and the metafits file
* CorrelatorContext and VoltageContext now have 'common' and 'common good' attributes describing the data files provided. 'Common' refers to timesteps and coarse channels which are common to all data files provided 'Common Good' determines 'Common' based on times after the quacktime.
* In CorrelatorContext read_by_baseline() and read_by_frequency(), the timestep index and coarse channel index are based on the indices of the CorrelatorContext.timesteps and coarse_channels lists
* In VoltageContext read_file() and read_second(), the timestep index and coarse channel index are based on the indices of the VoltageContext.timesteps and coarse_channels lists
* For all read methods If no data exists for a timestep index or coarse channel index, then a `PymwalibNoDataForTimestepAndCoarseChannel` exception is raised

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
