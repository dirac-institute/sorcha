import pytest
from sorcha.utilities.sorchaConfigs import sorchaConfigs

# initialise an empty object
test_configs = sorchaConfigs()


def test_input_configs():

    input_configs = {"ephemerides_type": "ar", "size_serial_chunk": "5000"}

    test_configs._read_and_validate_input_configs(input_configs)

    # did the ephemerides_type attribute populate correctly?
    assert test_configs.ephemerides_type == "ar"

    # now we check some wrong inputs to make sure they're caught correctly
    input_configs["ephemerides_type"] = "dummy_type"

    # we're telling pytest that we expect this command to fail with a SystemExit
    with pytest.raises(SystemExit) as e1:
        test_configs._read_and_validate_input_configs(input_configs)

    # and then we make sure the error text that triggers is the error text we expect
    assert (
        e1.value.code
        == "ERROR: value dummy_type for config parameter ephemerides_type not recognised. Expecting one of: ['ar', 'external']."
    )

    assert test_configs.size_serial_chunk == 5000

    input_configs["ephemerides_type"] = "ar"  # make sure to reset this before testing the next one
    input_configs["size_serial_chunk"] = "five thousand"

    # size_serial_chunk needs to be castable as an int, so again we expect a SystemExit
    with pytest.raises(SystemExit) as e2:
        test_configs._read_and_validate_input_configs(input_configs)

    assert (
        e2.value.code
        == "ERROR: expected an int for config parameter size_serial_chunk. Check value in config file."
    )
