import pytest

from sorcha.modules.PPFadingFunctionFilterWrapper import FadingFunctionFilter
from sorcha.configs.fadingfunctionConfigs import fadingfunctionConfigs
from sorcha.configs.fovConfigs import fovConfigs
from tests.configs.test_fovConfigs import correct_fov

def test_FadingFunctionFilter():

    fadingfunction_configs = fadingfunctionConfigs()
    fadingfunction_configs.fading_function_type = "fake_function"

    fov_config = fovConfigs(**correct_fov)


    with pytest.raises(SystemExit) as error_text:
        x = FadingFunctionFilter(fadingfunction_configs=fadingfunction_configs, fov_configs=fov_config)

    assert (
        error_text.value.code
        == f"ERROR: fading function type {fadingfunction_configs.fading_function_type} does not have a function for Fading functin filter."
    )
