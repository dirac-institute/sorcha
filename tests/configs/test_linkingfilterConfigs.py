import pytest
from sorcha.configs.linkingfilterConfigs import linkingfilterConfigs

correct_linkingfilter = {
    "discovery_filter_on": True,
    "ssp_linking_on": True,
    "drop_unlinked": True,
    "ssp_detection_efficiency": 0.95,
    "ssp_number_observations": 2,
    "ssp_separation_threshold": 0.5,
    "ssp_maximum_time": 0.0625,
    "ssp_number_tracklets": 3,
    "ssp_track_window": 15,
    "ssp_night_start_utc": 16.0,
    "des_distance_cut_on": None,
    "des_distance_cut_upper": None,
    "des_distance_cut_lower": None,
    "des_motion_cut_on": None,
    "des_motion_cut_upper": None,
    "des_motion_cut_lower": None,
    "des_discovery_on": None,
}

correct_linkingfilter_des = {
    "discovery_filter_on": True,
    "ssp_linking_on": None,
    "drop_unlinked": None,
    "ssp_detection_efficiency": None,
    "ssp_number_observations": None,
    "ssp_separation_threshold": None,
    "ssp_maximum_time": None,
    "ssp_number_tracklets": None,
    "ssp_track_window": None,
    "ssp_night_start_utc": None,
    "des_distance_cut_on": None,
    "des_distance_cut_upper": None,
    "des_distance_cut_lower": None,
    "des_motion_cut_on": None,
    "des_motion_cut_upper": None,
    "des_motion_cut_lower": None,
    "des_discovery_on": None,
}


# linkingfilter tests


@pytest.mark.parametrize(
    "key_name",
    ["ssp_detection_efficiency", "ssp_separation_threshold", "ssp_maximum_time", "ssp_night_start_utc"],
)
def test_linkingfilterConfigs_float(key_name):
    """
    Tests that wrong inputs for linkingfilterConfigs float attributes is caught correctly
    """

    linkingfilter_configs = correct_linkingfilter.copy()
    test_configs = linkingfilterConfigs(**linkingfilter_configs)
    assert test_configs.__dict__ == linkingfilter_configs

    linkingfilter_configs[key_name] = "one"

    with pytest.raises(SystemExit) as error_text:
        test_configs = linkingfilterConfigs(**linkingfilter_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a float for config parameter {key_name}. Check value in config file."
    )


@pytest.mark.parametrize("key_name", ["ssp_number_observations", "ssp_number_tracklets", "ssp_track_window"])
def test_linking_filter_int(key_name):
    """
    Tests that wrong inputs for linkingfilterConfigs int attributes is caught correctly
    """

    linkingfilter_configs = correct_linkingfilter.copy()
    test_configs = linkingfilterConfigs(**linkingfilter_configs)
    assert test_configs.__dict__ == linkingfilter_configs

    linkingfilter_configs[key_name] = "one"

    with pytest.raises(SystemExit) as error_text:
        test_configs = linkingfilterConfigs(**linkingfilter_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected an int for config parameter {key_name}. Check value in config file."
    )


@pytest.mark.parametrize(
    "key_name",
    [
        "ssp_detection_efficiency",
        "ssp_separation_threshold",
        "ssp_maximum_time",
        "ssp_night_start_utc",
        "ssp_number_observations",
        "ssp_number_tracklets",
        "ssp_track_window",
    ],
)
def test_linkingfilter_bounds(key_name):
    """
    Tests that values in linkingfilterConfigs are creating error messages when out of bounds
    """

    linkingfilter_configs = correct_linkingfilter.copy()

    if key_name == "ssp_maximum_time" or key_name == "ssp_track_window":
        linkingfilter_configs[key_name] = -5
        with pytest.raises(SystemExit) as error_text:
            test_configs = linkingfilterConfigs(**linkingfilter_configs)

        assert error_text.value.code == f"ERROR: {key_name} is negative."
    elif key_name == "ssp_number_observations":
        linkingfilter_configs[key_name] = -5
        with pytest.raises(SystemExit) as error_text:
            test_configs = linkingfilterConfigs(**linkingfilter_configs)

        assert error_text.value.code == f"ERROR: {key_name} is zero or negative."
    elif key_name == "ssp_separation_threshold":
        linkingfilter_configs[key_name] = -5
        with pytest.raises(SystemExit) as error_text:
            test_configs = linkingfilterConfigs(**linkingfilter_configs)
        assert error_text.value.code == f"ERROR: {key_name} is negative."

        linkingfilter_configs[key_name] = 0
        with pytest.raises(SystemExit) as error_text:
            test_configs = linkingfilterConfigs(**linkingfilter_configs)
        assert error_text.value.code == f"ERROR: {key_name} is zero."

    elif key_name == "ssp_number_tracklets":
        linkingfilter_configs[key_name] = -5
        with pytest.raises(SystemExit) as error_text:
            test_configs = linkingfilterConfigs(**linkingfilter_configs)

        assert error_text.value.code == "ERROR: ssp_number_tracklets is zero or less."
    elif key_name == "ssp_detection_efficiency":
        linkingfilter_configs[key_name] = -5
        with pytest.raises(SystemExit) as error_text:
            test_configs = linkingfilterConfigs(**linkingfilter_configs)

        assert (
            error_text.value.code
            == "ERROR: ssp_detection_efficiency out of bounds (should be between 0 and 1)."
        )
    elif key_name == "ssp_night_start_utc":
        linkingfilter_configs[key_name] = -5
        with pytest.raises(SystemExit) as error_text:
            test_configs = linkingfilterConfigs(**linkingfilter_configs)

        assert (
            error_text.value.code == "ERROR: ssp_night_start_utc must be a valid time between 0 and 24 hours."
        )


def test_linkingfilter_only_some_sspvar():
    """
    Males sure error message shows when only some SSP variables are provided
    """
    linkingfilter_configs = correct_linkingfilter.copy()

    linkingfilter_configs["ssp_separation_threshold"] = None

    with pytest.raises(SystemExit) as error_text:
        test_configs = linkingfilterConfigs(**linkingfilter_configs)

    assert (
        error_text.value.code
        == "ERROR: only some ssp linking variables supplied. Supply all five required variables for ssp linking filter, or none to turn filter off."
    )


def test_linkingfilter_bool():
    """
    Tests that wrong inputs for linkingfilterConfigs bool attributes is caught correctly
    """

    linkingfilter_configs = correct_linkingfilter.copy()

    linkingfilter_configs["drop_unlinked"] = "fake"

    with pytest.raises(SystemExit) as error_text:
        test_configs = linkingfilterConfigs(**linkingfilter_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a bool for config parameter drop_unlinked. Check value in config file."
    )


# DES discovery
@pytest.mark.parametrize(
    "key_name, prob_name",
    [
        ("des_distance_cut_upper", "des_distance_cut_lower"),
        ("des_distance_cut_lower", "des_distance_cut_upper"),
        ("des_motion_cut_upper", "des_motion_cut_lower"),
        ("des_motion_cut_lower", "des_motion_cut_upper"),
    ],
)
def test_linkingfilter_descuts_exists(key_name, prob_name):
    """
    tests the descut inputs in the linkingfilter
    """

    linkingfilter_configs = correct_linkingfilter_des.copy()

    linkingfilter_configs[key_name] = 10

    with pytest.raises(SystemExit) as error_text:
        test_configs = linkingfilterConfigs(**linkingfilter_configs)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {prob_name} in config file. Please check the file and try again."
    )


@pytest.mark.parametrize(
    "key_name, prob_name",
    [
        ("des_distance_cut_upper", "des_distance_cut_lower"),
        ("des_distance_cut_lower", "des_distance_cut_upper"),
        ("des_motion_cut_upper", "des_motion_cut_lower"),
        ("des_motion_cut_lower", "des_motion_cut_upper"),
    ],
)
def test_linkingfilter_descuts_float(key_name, prob_name):
    """
    tests that the descut inputs are float in the linkingfilter
    """

    linkingfilter_configs = correct_linkingfilter_des.copy()

    linkingfilter_configs[key_name] = 10.0
    linkingfilter_configs[prob_name] = "str"

    with pytest.raises(SystemExit) as error_text:
        test_configs = linkingfilterConfigs(**linkingfilter_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a float for config parameter {prob_name}. Check value in config file."
    )
