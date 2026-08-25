import pytest
from sorcha.configs.lightcurveAndActivityConfigs import lightcurveConfigs, activityConfigs
from sorcha.lightcurves.lightcurve_registration import LC_METHODS
from sorcha.activity.activity_registration import CA_METHODS

correct_lc_model = {"lc_model": None}

correct_activity = {"comet_activity": None}


# lightcurve config test


def test_lightcurve_config():
    """
    makes sure that if lightcurve model provided is not registered an error occurs
    """

    lightcurve_configs = correct_lc_model.copy()

    lightcurve_configs["lc_model"] = "what_model"

    with pytest.raises(SystemExit) as error_text:
        test_configs = lightcurveConfigs(**lightcurve_configs)
    assert (
        error_text.value.code
        == f"The requested light curve model, 'what_model', is not registered. Available lightcurve options are: {list(LC_METHODS.keys())}"
    )


##################################################################################################################################

# activity config test


def test_activity_config():
    """
    makes sure that if comet activity model provided is not registered an error occurs
    """

    activity_configs = correct_activity.copy()

    activity_configs["comet_activity"] = "nothing"

    with pytest.raises(SystemExit) as error_text:
        test_configs = activityConfigs(**activity_configs)
    assert (
        error_text.value.code
        == f"The requested comet activity model, 'nothing', is not registered. Available comet activity models are: {list(CA_METHODS.keys())}"
    )
