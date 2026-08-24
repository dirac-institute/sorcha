import pytest

from sorcha.modules.PPFadingFunctionFilterWrapper import FadingFunctionFilter


def test_FadingFunctionFilter():
    fading_function_type = "fake_function"

    with pytest.raises(SystemExit) as error_text:
        x = FadingFunctionFilter(fading_function_type=fading_function_type)

    assert (
        error_text.value.code
        == f"ERROR: fading function type {fading_function_type} does not have a function for Fading functin filter."
    )
