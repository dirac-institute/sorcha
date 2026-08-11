import pytest

from sorcha.modules.PPFadingFunctionFilterWrapper import FadingFunctionFilter


def test_FadingFunctionFilter():

    survey_name = "fake_survey"

    with pytest.raises(SystemExit) as error_text:
        x = FadingFunctionFilter(survey_name= survey_name)

    assert (
        error_text.value.code
        == f"ERROR: Survey {survey_name} does not have a function for Fading functin filter."
    )
    