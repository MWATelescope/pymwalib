from pymwalib.correlator_context import CorrelatorContext
import pytest
from os.path import join as path_join, dirname

def prefix_test_data(path):
    return path_join(dirname(__file__), "data", path)

@pytest.fixture
def mwax_context():
    return CorrelatorContext(
        prefix_test_data("1297526432_mwax/1297526432.metafits"),
        map(
            prefix_test_data,
            [
                "1297526432_mwax/1297526432_20210216160014_ch117_000.fits",
                "1297526432_mwax/1297526432_20210216160014_ch117_001.fits",
                "1297526432_mwax/1297526432_20210216160014_ch118_000.fits",
                "1297526432_mwax/1297526432_20210216160014_ch118_001.fits"
            ]
        )
    )

def test_mwax_antennas(mwax_context):
    assert len(mwax_context.antennas) == 2
    assert mwax_context.antennas[0].tile_id == 51
    assert mwax_context.antennas[1].tile_id == 52
