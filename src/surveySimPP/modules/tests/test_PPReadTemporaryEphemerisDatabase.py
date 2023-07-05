import os
import pytest

from surveySimPP.tests.data import get_test_filepath


@pytest.fixture
def setup_and_teardown_for_PPReadTemporaryEphemerisDatabase():
    yield

    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))
    stem_name = "testdb_PPIntermDB.db"

    os.remove(os.path.join(temp_path, stem_name))


def test_PPReadTemporaryEphemerisDatabase(setup_and_teardown_for_PPReadTemporaryEphemerisDatabase):
    from surveySimPP.modules.PPMakeTemporaryEphemerisDatabase import PPMakeTemporaryEphemerisDatabase
    from surveySimPP.modules.PPReadTemporaryEphemerisDatabase import PPReadTemporaryEphemerisDatabase
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters

    padacl = PPReadPhysicalParameters(get_test_filepath("testcolour.txt"), 0, 5, "whitespace")
    print(padacl)
    objid_list = padacl["ObjID"].unique().tolist()

    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))
    stem_name = "testdb_PPIntermDB.db"
    daba = PPMakeTemporaryEphemerisDatabase(
        get_test_filepath("oiftestoutput.txt"), os.path.join(temp_path, stem_name), "whitespace"
    )

    padafr = PPReadTemporaryEphemerisDatabase(daba, objid_list)

    nlines = 9

    nlinesdb = len(padafr.index)

    assert nlines == nlinesdb
    return
