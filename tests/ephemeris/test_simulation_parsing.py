import pytest
import numpy as np
import sorcha.ephemeris.simulation_parsing as sp


def test_convert_mpc_epoch():
    """test a range of valid epochs."""
    epoch0 = "I969U"
    epoch1 = "J9611"
    epoch2 = "K01AM"

    convert0 = sp.convert_mpc_epoch(epoch0)
    assert convert0 == (1896, 9, 30)

    convert1 = sp.convert_mpc_epoch(epoch1)
    assert convert1 == (1996, 1, 1)

    convert2 = sp.convert_mpc_epoch(epoch2)
    assert convert2 == (2001, 10, 22)


def test_convert_mpc_epoch_exceptions():
    """test a range of bad epochs."""
    bad_epochs = [
        "I969UU",
        "Q969U",
        "J9601",
        "J96D1",
        "J96DQ",
    ]

    for bad in bad_epochs:
        with pytest.raises(ValueError):
            sp.convert_mpc_epoch(bad)


def test_observatory_compared_to_original():
    observatory = sp.Observatory()
    obs = observatory.ObservatoryXYZ

    # Reference tuples were taken from Matt Holman's original notebook
    reference_tuple_1 = (0.8352498991871398, -0.26942906823108936, 0.4785)
    reference_tuple_2 = (-0.37388143680631203, 0.762042035331154, -0.52703)

    assert np.all(np.isclose(reference_tuple_1, obs["Z20"]))
    assert np.all(np.isclose(reference_tuple_2, obs["322"]))


def test_observatory_for_moving_observatories():
    observatory = sp.Observatory()
    obs = observatory.ObservatoryXYZ

    assert obs["250"] == (None, None, None)
