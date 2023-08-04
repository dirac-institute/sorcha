import pytest
from sorcha.activity.activity_registration import (
    register_activity_subclasses,
    update_activity_subclasses,
    CA_METHODS,
)
from sorcha.activity.base_activity import AbstractCometaryActivity


def test_register_subclasses():
    output = register_activity_subclasses()

    assert output == CA_METHODS


def test_register_subclasses_with_duplicate():
    class dup_identity(AbstractCometaryActivity):
        def compute(self):
            return 1

        @staticmethod
        def name_id():
            return "identity"

    with pytest.raises(ValueError) as excinfo:
        _ = register_activity_subclasses()

    assert "duplicate cometary activity calculator name to CA_METHODS: identity" in str(excinfo.value)


def test_update_subclasses():
    class test_activity(AbstractCometaryActivity):
        def compute(self):
            return 1

        @staticmethod
        def name_id():
            return "test_ca"

    update_activity_subclasses()

    assert CA_METHODS["test_ca"] == test_activity
