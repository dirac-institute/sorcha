import pytest
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
