from pymwalib.correlator_context import CorrelatorContext
import pytest
import numpy as np
from os.path import join as path_join, dirname

def prefix_test_data(path):
    return path_join(dirname(__file__), "data", path)

@pytest.fixture
def mwax_corr_context() -> CorrelatorContext:
    return CorrelatorContext(
        prefix_test_data("1297526432_mwax/1297526432.metafits"),
        list(map(
            prefix_test_data,
            [
                "1297526432_mwax/1297526432_20210216160014_ch117_000.fits",
                "1297526432_mwax/1297526432_20210216160014_ch117_001.fits",
                "1297526432_mwax/1297526432_20210216160014_ch118_000.fits",
                "1297526432_mwax/1297526432_20210216160014_ch118_001.fits"
            ]
        ))
    )

def test_mwax_antennas(mwax_corr_context: CorrelatorContext):
    assert len(mwax_corr_context.metafits_context.antennas) == 2
    assert mwax_corr_context.metafits_context.antennas[0].tile_id == 51
    assert mwax_corr_context.metafits_context.antennas[1].tile_id == 52

def test_baselines(mwax_corr_context: CorrelatorContext):
    assert len(mwax_corr_context.metafits_context.baselines) == 3
    assert mwax_corr_context.metafits_context.baselines[0].ant1_index == 0
    assert mwax_corr_context.metafits_context.baselines[0].ant2_index == 0
    assert mwax_corr_context.metafits_context.baselines[1].ant1_index == 0
    assert mwax_corr_context.metafits_context.baselines[1].ant2_index == 1
    assert mwax_corr_context.metafits_context.baselines[2].ant1_index == 1
    assert mwax_corr_context.metafits_context.baselines[2].ant2_index == 1

def test_mwax_rfinputs(mwax_corr_context: CorrelatorContext):
    assert len(mwax_corr_context.metafits_context.rf_inputs) == 4
    assert mwax_corr_context.metafits_context.rf_inputs[0].tile_id == 51
    assert mwax_corr_context.metafits_context.rf_inputs[0].pol == "X"
    assert mwax_corr_context.metafits_context.rf_inputs[1].tile_id == 51
    assert mwax_corr_context.metafits_context.rf_inputs[1].pol == "Y"
    assert mwax_corr_context.metafits_context.rf_inputs[2].tile_id == 52
    assert mwax_corr_context.metafits_context.rf_inputs[2].pol == "X"
    assert mwax_corr_context.metafits_context.rf_inputs[3].tile_id == 52
    assert mwax_corr_context.metafits_context.rf_inputs[3].pol == "Y"

def test_mwax_coarse_channels(mwax_corr_context: CorrelatorContext):
    assert len(mwax_corr_context.coarse_channels) == 2
    assert mwax_corr_context.coarse_channels[0].rec_chan_number == 117
    assert mwax_corr_context.coarse_channels[1].rec_chan_number == 118

    #
    # NOTE due to this being a modified metafits, the below is true.
    # With the "real" metafits the corr_chan_numbers would be 8 and 9 respectively
    #
    assert mwax_corr_context.coarse_channels[0].corr_chan_number == 0
    assert mwax_corr_context.coarse_channels[1].corr_chan_number == 1

def test_mwax_timesteps(mwax_corr_context: CorrelatorContext):
    assert len(mwax_corr_context.timesteps) == 592
    assert mwax_corr_context.timesteps[0].unix_time_ms == 1613491214000
    assert mwax_corr_context.timesteps[1].unix_time_ms == 1613491214500
    assert mwax_corr_context.timesteps[590].unix_time_ms == 1613491509000
    assert mwax_corr_context.timesteps[591].unix_time_ms == 1613491509500

def test_read_by_baseline(mwax_corr_context: CorrelatorContext):
    ts = 0
    chan = 0
    data_by_bl = mwax_corr_context.read_by_baseline(ts, chan)
    data_by_f = mwax_corr_context.read_by_frequency(ts, chan)

    # Test length
    assert len(data_by_bl) == mwax_corr_context.num_timestep_coarse_chan_floats
    assert len(data_by_f) == mwax_corr_context.num_timestep_coarse_chan_floats

    # Sum them and compare
    sum_bl = np.sum(data_by_bl)
    sum_f = np.sum(data_by_f)
    assert sum_bl == sum_f
    print(f"\nCorrelator Sum by baseline  == {sum_bl}")
    print(f"Correlator Sum by frequency == {sum_f}")

def test_common_timestep_indices(mwax_corr_context: CorrelatorContext):
    assert len(mwax_corr_context.common_timestep_indices) == mwax_corr_context.num_common_timesteps
    assert len(mwax_corr_context.common_timestep_indices) == 2
    assert mwax_corr_context.common_timestep_indices[0] == 0
    assert mwax_corr_context.common_timestep_indices[1] == 1

def test_common_good_timestep_indices(mwax_corr_context: CorrelatorContext):
    assert len(mwax_corr_context.common_good_timestep_indices) == mwax_corr_context.num_common_good_timesteps
    assert len(mwax_corr_context.common_good_timestep_indices) == 1
    assert mwax_corr_context.common_good_timestep_indices[0] == 1

def test_provided_timestep_indices(mwax_corr_context: CorrelatorContext):
    assert len(mwax_corr_context.provided_timestep_indices) == mwax_corr_context.num_provided_timesteps
    assert len(mwax_corr_context.provided_timestep_indices) == 4
    assert mwax_corr_context.provided_timestep_indices[0] == 0
    assert mwax_corr_context.provided_timestep_indices[1] == 1
    assert mwax_corr_context.provided_timestep_indices[2] == 160
    assert mwax_corr_context.provided_timestep_indices[3] == 161

def test_common_coarse_chan_indices(mwax_corr_context: CorrelatorContext):
    assert len(mwax_corr_context.common_coarse_chan_indices) == mwax_corr_context.num_common_coarse_chans
    assert len(mwax_corr_context.common_coarse_chan_indices) == 2
    assert mwax_corr_context.common_coarse_chan_indices[0] == 0
    assert mwax_corr_context.common_coarse_chan_indices[1] == 1

def test_common_good_coarse_chan_indices(mwax_corr_context: CorrelatorContext):
    assert len(mwax_corr_context.common_good_coarse_chan_indices) == mwax_corr_context.num_common_good_coarse_chans
    assert len(mwax_corr_context.common_good_coarse_chan_indices) == 2
    assert mwax_corr_context.common_good_coarse_chan_indices[0] == 0
    assert mwax_corr_context.common_good_coarse_chan_indices[1] == 1

def test_provided_coarse_chan_indices(mwax_corr_context: CorrelatorContext):
    assert len(mwax_corr_context.provided_coarse_chan_indices) == mwax_corr_context.num_provided_coarse_chans
    assert len(mwax_corr_context.provided_coarse_chan_indices) == 2
    assert mwax_corr_context.provided_coarse_chan_indices[0] == 0
    assert mwax_corr_context.provided_coarse_chan_indices[1] == 1
