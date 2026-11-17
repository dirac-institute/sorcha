import pytest
from sorcha.configs.saturationConfigs import saturationConfigs


correct_saturation = {
    "bright_limit_on": True,
    "bright_limit": [16.0, 16.0, 16.0, 16.0, 16.0, 16.0],
    "_observing_filters": ["r", "g", "i", "z", "u", "y"],
}
correct_saturation_read = {"bright_limit": "16.0", "_observing_filters": ["r", "g", "i", "z", "u", "y"]}


# saturation configs test


def test_saturationConfigs():
    """
    Tests that error occurs when list of saturation limits is not the same length as list of observing filters.
    Also tests that error occurs when brightness limits can't be parsed.
    """

    saturation_configs = correct_saturation_read.copy()

    # make sure everything populated correctly
    test_configs = saturationConfigs(**saturation_configs)
    assert test_configs.__dict__ == correct_saturation

    saturation_configs["bright_limit"] = "10,2"

    with pytest.raises(SystemExit) as error_text:
        test_configs = saturationConfigs(**saturation_configs)

    assert (
        error_text.value.code
        == "ERROR: list of saturation limits is not the same length as list of observing filters."
    )
    saturation_configs["bright_limit"] = "10;2"

    with pytest.raises(SystemExit) as error_text:
        test_configs = saturationConfigs(**saturation_configs)

    assert (
        error_text.value.code == "ERROR: could not parse brightness limits. Check formatting and try again."
    )

    # Make sure it can take a simple float
    bright_limit = 2.0
    manual_saturation_config = saturationConfigs(bright_limit=bright_limit, _observing_filters=["g"])
    assert manual_saturation_config.bright_limit[0] == bright_limit

    # Cast float to a list if there are multiple filters
    manual_saturation_config = saturationConfigs(bright_limit=bright_limit, _observing_filters=["g", "r"])
    assert len(manual_saturation_config.bright_limit) == 2


@pytest.mark.parametrize("key_name", ["_observing_filters"])
def test_saturationConfigs_mandatory(key_name):
    """
    this loops through the mandatory keys and makes sure the code fails correctly when each is missing
    """

    saturation_configs = correct_saturation_read.copy()

    del saturation_configs[key_name]

    with pytest.raises(SystemExit) as error_text:
        test_configs = saturationConfigs(**saturation_configs)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
    )
