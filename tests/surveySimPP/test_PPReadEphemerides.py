import pytest

from surveySimPP.utilities.test_data_utilities import get_test_filepath


def test_PPReadEphemerides():
    """Much of the behaviour here is tested by PPReadOif, so this
    test only makes basic checks.
    """

    from surveySimPP.modules.PPReadEphemerides import PPReadEphemerides

    with pytest.raises(SystemExit) as e1:
        oif_file = PPReadEphemerides(get_test_filepath("oiftestoutput.txt"), "wtf", "whitespace")

    assert e1.type == SystemExit
    assert e1.value.code == "PPReadEphemerides: invalid value for ephemerides_type: wtf"

    oif_file = PPReadEphemerides(get_test_filepath("oiftestoutput.txt"), "oif", "whitespace")

    assert len(oif_file) == 9
    assert len(oif_file.columns) == 22

    return
