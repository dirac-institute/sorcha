import pytest

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_PPGetMainFilterAndColourOffsets():
    from sorcha.modules.PPGetMainFilterAndColourOffsets import PPGetMainFilterAndColourOffsets

    colour_fn = get_test_filepath("testcolour.txt")
    observing_filters = ["r", "g", "i", "z"]

    mainfilter, othercolours = PPGetMainFilterAndColourOffsets(colour_fn, observing_filters, "whitespace")

    assert mainfilter == "r"
    assert othercolours == ["g-r", "i-r", "z-r"]

    # Main filter not part of the observing filters.
    with pytest.raises(SystemExit) as err:
        _, _ = PPGetMainFilterAndColourOffsets(colour_fn, ["g", "i", "z"], "pipe")
    assert (
        err.value.args[0]
        == "ERROR: PPGetMainFilterAndColourOffsets: H is given as r, but r is not listed as a requested observation filter in config file."
    )

    # Test invalid separator
    with pytest.raises(SystemExit) as err:
        _, _ = PPGetMainFilterAndColourOffsets(colour_fn, observing_filters, "pipe")
    assert (
        err.value.args[0]
        == "ERROR: PPGetMainFilterAndColourOffsets: unexpected valye for auxFormat keyword in configs."
    )

    # Test missing colour
    with pytest.raises(SystemExit) as err:
        _, _ = PPGetMainFilterAndColourOffsets(colour_fn, ["r", "g", "i", "z", "u"], "whitespace")
    assert (
        err.value.args[0]
        == "ERROR: PPGetMainFilterAndColourOffsets: colour offset columns in physical parameters file do not match with observing filters specified in config file."
    )
