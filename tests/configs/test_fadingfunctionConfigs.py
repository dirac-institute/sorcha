import pytest 
from sorcha.configs.fadingfunctionConfigs import fadingfunctionConfigs

correct_fadingfunction = {
    "fading_function_on": True,
    "fading_function_width": 0.1,
    "fading_function_peak_efficiency": 1.0,
    "survey_name": "rubin_sim",
    "des_transient_efficency": None,
    "fading_function_type": "general",
}


# fadingfunction config tests


@pytest.mark.parametrize("key_name", ["fading_function_width", "fading_function_peak_efficiency"])
def test_fadingfunctionConfig_on_float(key_name):
    """
    Tests that wrong inputs for fadingfunctionConfig float attributes is caught correctly
    """

    fadingfunction_configs = correct_fadingfunction.copy()
    test_configs = fadingfunctionConfigs(**fadingfunction_configs)
    assert test_configs.__dict__ == fadingfunction_configs

    fadingfunction_configs[key_name] = "ten"
    with pytest.raises(SystemExit) as error_text:
        test_configs = fadingfunctionConfigs(**fadingfunction_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a float for config parameter {key_name}. Check value in config file."
    )


def test_fadingfunctionConfig_on_float():
    """
    Tests that wrong inputs for fadingfunctionConfig float attributes is caught correctly
    """

    fadingfunction_configs = correct_fadingfunction.copy()

    # "set up for per_obs"
    fadingfunction_configs["fading_function_peak_efficiency"] = None
    fadingfunction_configs["fading_function_width"] = None

    fadingfunction_configs["des_transient_efficency"] = 0.955

    test_configs = fadingfunctionConfigs(**fadingfunction_configs)

    fadingfunction_configs["des_transient_efficency"] = 0.955
    fadingfunction_configs["fading_function_type"] = "des_per_obs"
    # test cast as float
    assert test_configs.__dict__ == fadingfunction_configs

    fadingfunction_configs["des_transient_efficency"] = "ten"
    with pytest.raises(SystemExit) as error_text:
        test_configs = fadingfunctionConfigs(**fadingfunction_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a float for config parameter des_transient_efficency. Check value in config file."
    )


@pytest.mark.parametrize("key_name", ["fading_function_width", "fading_function_peak_efficiency"])
def test_fadingfunction_outofbounds(key_name):
    """
    Tests that values in fadingfunctionConfigs are creating error messages when out of bounds
    """

    fadingfunction_configs = correct_fadingfunction.copy()
    fadingfunction_configs[key_name] = 10
    if key_name == "fading_function_width":
        with pytest.raises(SystemExit) as error_text:
            test_configs = fadingfunctionConfigs(**fadingfunction_configs)
        assert (
            error_text.value.code
            == "ERROR: fading_function_width out of bounds. Must be greater than zero and less than 0.5."
        )
    if key_name == "fading_function_peak_efficiency":
        with pytest.raises(SystemExit) as error_text:
            test_configs = fadingfunctionConfigs(**fadingfunction_configs)
        assert (
            error_text.value.code
            == "ERROR: fading_function_peak_efficiency out of bounds. Must be between 0 and 1."
        )


def test_fadingfunction_allnone():
    """
    This loops through the not required keys and makes sure the code fails correctly when all attributes are none
    """
    fadingfunction_configs = correct_fadingfunction.copy()
    fadingfunction_configs["fading_function_on"] = None
    fadingfunction_configs["fading_function_width"] = 5.0
    fadingfunction_configs["fading_function_peak_efficiency"] = None
    with pytest.raises(SystemExit) as error_text:
        test_configs = fadingfunctionConfigs(**fadingfunction_configs)
    assert (
        error_text.value.code
        == "ERROR: Both fading_function_peak_efficiency and fading_function_width are needed to be supplied for fading function"
    )

