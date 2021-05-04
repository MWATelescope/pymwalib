from pymwalib.correlator_context import CorrelatorContext
import pytest
import numpy as np
from os.path import join as path_join, dirname

def prefix_test_data(path):
    return path_join(dirname(__file__), "data", path)

@pytest.fixture
def mwax_context():
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

def test_mwax_antennas(mwax_context):
    assert len(mwax_context.antennas) == 2
    assert mwax_context.antennas[0].tile_id == 51
    assert mwax_context.antennas[1].tile_id == 52

def test_mwax_rfinputs(mwax_context):
    assert len(mwax_context.rfinputs) == 4
    assert mwax_context.rfinputs[0].tile_id == 51
    assert mwax_context.rfinputs[0].pol == "X"
    assert mwax_context.rfinputs[1].tile_id == 51
    assert mwax_context.rfinputs[1].pol == "Y"
    assert mwax_context.rfinputs[2].tile_id == 52
    assert mwax_context.rfinputs[2].pol == "X"
    assert mwax_context.rfinputs[3].tile_id == 52
    assert mwax_context.rfinputs[3].pol == "Y"

def test_mwax_coarse_channels(mwax_context):
    assert len(mwax_context.coarse_channels) == 2
    assert mwax_context.coarse_channels[0].rec_chan_number == 117
    assert mwax_context.coarse_channels[1].rec_chan_number == 118

    #
    # NOTE due to this being a modified metafits, the below is true.
    # With the "real" metafits the corr_chan_numbers would be 8 and 9 respectively
    #
    assert mwax_context.coarse_channels[0].corr_chan_number == 0
    assert mwax_context.coarse_channels[1].corr_chan_number == 1

def test_mwax_timesteps(mwax_context):
    assert len(mwax_context.timesteps) == 4
    assert mwax_context.timesteps[0].unix_time_ms == 1613491214000
    assert mwax_context.timesteps[1].unix_time_ms == 1613491214500
    assert mwax_context.timesteps[2].unix_time_ms == 1613491294000
    assert mwax_context.timesteps[3].unix_time_ms == 1613491294500

def test_visibility_pols(mwax_context):
    assert len(mwax_context.visibility_pols) == 4
    assert mwax_context.visibility_pols[0].polarisation == "XX"
    assert mwax_context.visibility_pols[1].polarisation == "XY"
    assert mwax_context.visibility_pols[2].polarisation == "YX"
    assert mwax_context.visibility_pols[3].polarisation == "YY"

def test_baselines(mwax_context):
    assert len(mwax_context.baselines) == 3
    assert mwax_context.baselines[0].ant1_index == 0
    assert mwax_context.baselines[0].ant2_index == 0
    assert mwax_context.baselines[1].ant1_index == 0
    assert mwax_context.baselines[1].ant2_index == 1
    assert mwax_context.baselines[2].ant1_index == 1
    assert mwax_context.baselines[2].ant2_index == 1

def test_read_by_baseline(mwax_context):
    ts = 0
    chan = 0
    data_by_bl = mwax_context.read_by_baseline(ts, chan)
    data_by_f = mwax_context.read_by_frequency(ts, chan)

    # Test length
    assert len(data_by_bl) == mwax_context.correlator_metadata.num_timestep_coarse_chan_floats
    assert len(data_by_f) == mwax_context.correlator_metadata.num_timestep_coarse_chan_floats

    # Sum them and compare
    sum_bl = np.sum(data_by_bl)
    sum_f = np.sum(data_by_f)
    assert sum_bl == sum_f
    print(f"\nCorrelator Sum by baseline  == {sum_bl}")
    print(f"Correlator Sum by frequency == {sum_f}")
