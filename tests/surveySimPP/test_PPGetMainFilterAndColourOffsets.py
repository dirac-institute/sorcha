from surveySimPP.utilities.test_data_utilities import get_test_filepath


def test_PPGetMainFilterAndColourOffsets():
    from surveySimPP.modules.PPGetMainFilterAndColourOffsets import PPGetMainFilterAndColourOffsets

    colour_fn = get_test_filepath("testcolour.txt")
    observing_filters = ["r", "g", "i", "z"]

    mainfilter, othercolours = PPGetMainFilterAndColourOffsets(colour_fn, observing_filters, "whitespace")

    assert mainfilter == "r"
    assert othercolours == ["g-r", "i-r", "z-r"]
