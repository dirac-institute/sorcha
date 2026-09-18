import pytest
from sorcha.configs.expertConfigs import expertConfigs

correct_expert = {
    "snr_limit": None,
    "snr_limit_on": False,
    "mag_limit": None,
    "mag_limit_on": False,
    "trailing_losses_on": True,
    "uncertainties_on": True,
    "default_snr_cut": True,
    "randomization_on": True,
    "vignetting_on": True,
    "brute_force": True,
    "camera_model": None,
    "survey_name": "rubin_sim",
}


# expert config test


@pytest.mark.parametrize("key_name", ["snr_limit", "mag_limit"])
def test_expert_config_float(key_name):
    """
    tests that wrong inputs for expertConfigs float attributes is caught correctly
    """

    expect_configs = correct_expert.copy()
    expect_configs[key_name] = "str"
    with pytest.raises(SystemExit) as error_text:
        test_configs = expertConfigs(**expect_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a float for config parameter {key_name}. Check value in config file."
    )


@pytest.mark.parametrize("key_name, error_name", [("snr_limit", "SNRPSFMag"), ("mag_limit", "magnitude")])
def test_expert_config_bounds(key_name, error_name):
    """
    Tests that values in expertConfigs are creating error messages when out of bounds
    """

    expect_configs = correct_expert.copy()
    expect_configs[key_name] = -5
    with pytest.raises(SystemExit) as error_text:
        test_configs = expertConfigs(**expect_configs)

    assert error_text.value.code == f"ERROR: {error_name} limit is negative."


def test_expert_config_exclusive():
    """
    Makes sure that when both snr limit and magnitude limit are specified that an error occurs
    """

    expect_configs = correct_expert.copy()
    expect_configs["mag_limit"] = 5
    expect_configs["snr_limit"] = 5
    with pytest.raises(SystemExit) as error_text:
        test_configs = expertConfigs(**expect_configs)

    assert (
        error_text.value.code
        == "ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one or both from config file."
    )


@pytest.mark.parametrize(
    "key_name",
    [
        "uncertainties_on",
        "trailing_losses_on",
        "default_snr_cut",
        "randomization_on",
        "vignetting_on",
        "brute_force",
    ],
)
def test_expertConfig_bool(key_name):
    """
    Tests that wrong inputs for expertConfigs bool attributes is caught correctly
    """

    expect_configs = correct_expert.copy()
    expect_configs[key_name] = "fake"
    with pytest.raises(SystemExit) as error_text:
        test_configs = expertConfigs(**expect_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a bool for config parameter {key_name}. Check value in config file."
    )

    # checking this also works inside DES if statement too.
    expect_configs = correct_expert.copy()
    expect_configs[key_name] = "fake"
    expect_configs["survey_name"] = "des"
    with pytest.raises(SystemExit) as error_text:
        test_configs = expertConfigs(**expect_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a bool for config parameter {key_name}. Check value in config file."
    )


@pytest.mark.parametrize(
    "key_name", ["uncertainties_on", "trailing_losses_on", "randomization_on", "vignetting_on"]
)
def test_expertConfig_bool_DES(key_name):
    """
    Tests that features that should be turned off for DES are turned off.
    """

    # checking this also works for des,
    expect_configs = correct_expert.copy()
    expect_configs[key_name] = True
    expect_configs["survey_name"] = "des"
    with pytest.raises(SystemExit) as error_text:
        test_configs = expertConfigs(**expect_configs)

    assert (
        error_text.value.code
        == "ERROR: DES simulation does not support uncertainties, trailing losses, vignetting and randomization."
    )


@pytest.mark.parametrize("key_name", ["vignetting_on"])
def test_expertConfig_bool_visits_footprint(key_name):
    """
    Tests  features that should be turned off for visits footprint are turned off.
    """

    # checking this also works for des,
    expect_configs = correct_expert.copy()
    expect_configs[key_name] = True
    expect_configs["camera_model"] = "visits_footprint"
    with pytest.raises(SystemExit) as error_text:
        test_configs = expertConfigs(**expect_configs)

    assert error_text.value.code == "ERROR: fov camera model 'visits_footprint' does not support vignetting."


def test_expertConfig_bool_uncertainties_randomisation_logic():
    """
    Tests that should error occurs if uncertainties_on is false when randomization_on is true.
    """

    # checking this also works for des,
    expect_configs = correct_expert.copy()
    expect_configs["randomization_on"] = True
    expect_configs["uncertainties_on"] = False

    with pytest.raises(SystemExit) as error_text:
        test_configs = expertConfigs(**expect_configs)

    assert error_text.value.code == "ERROR: uncertainties_on must be true if randomization_on is true."
