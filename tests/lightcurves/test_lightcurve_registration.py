import pytest
from sorcha.lightcurves.lightcurve_registration import (
    register_lc_subclasses,
    update_lc_subclasses,
    LC_METHODS,
)
from sorcha.lightcurves.base_lightcurve import AbstractLightCurve


def test_register_subclasses():
    output = register_lc_subclasses()

    assert output == LC_METHODS


def test_register_subclasses_with_duplicate():
    class dup_identity(AbstractLightCurve):
        def compute(self):
            return 1

        @staticmethod
        def name_id():
            return "identity"

    with pytest.raises(ValueError) as excinfo:
        _ = register_lc_subclasses()

    assert "duplicate Lightcurve calculator name to LC_METHODS: identity" in str(excinfo.value)


def test_update_subclasses():
    class test_lc(AbstractLightCurve):
        def compute(self):
            return 1

        @staticmethod
        def name_id():
            return "test_lc"

    update_lc_subclasses()

    assert LC_METHODS["test_lc"] == test_lc
