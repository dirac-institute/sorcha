
import pytest
from sorcha.configs.inputAndOutputConfigs import phasecurvesConfigs

correct_phasecurve = {"phase_function": "HG"}



# phasecurve configs tests


@pytest.mark.parametrize("key_name", ["phase_function"])
def test_phasecurveConfigs_mandatory(key_name):
    """
    this loops through the mandatory keys and makes sure the code fails correctly when each is missing
    """

    phasecurves_configs = correct_phasecurve.copy()

    del phasecurves_configs[key_name]

    with pytest.raises(SystemExit) as error_text:
        test_configs = phasecurvesConfigs(**phasecurves_configs)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
    )


@pytest.mark.parametrize(
    "key_name, expected_list",
    [("phase_function", "['HG', 'HG1G2', 'HG12', 'linear', 'none']")],
)
def test_phasecurveConfigs_inlist(key_name, expected_list):
    """
    this loops through the keys that need to have one of several set values and makes sure the correct error message triggers when they're not
    """

    phasecurve_configs = correct_phasecurve.copy()

    phasecurve_configs[key_name] = "definitely_fake_bad_key"

    with pytest.raises(SystemExit) as error_text:
        test_configs = phasecurvesConfigs(**phasecurve_configs)
    print(error_text.value.code)
    print(
        f"ERROR: value definitely_fake_bad_key for config parameter {key_name} not recognised. Expecting one of: {expected_list}."
    )
    assert (
        error_text.value.code
        == f"ERROR: value definitely_fake_bad_key for config parameter {key_name} not recognised. Expecting one of: {expected_list}."
    )
