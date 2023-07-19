import sqlite3
import pandas as pd
import os
import pytest

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


@pytest.fixture
def setup_and_teardown_for_PPMakeTemporaryEphemerisDatabase():
    yield

    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))
    stem_name = "testdb_PPIntermDB.db"

    os.remove(os.path.join(temp_path, stem_name))


def test_PPMakeTemporaryEphemerisDatabase(setup_and_teardown_for_PPMakeTemporaryEphemerisDatabase):
    from sorcha.modules.PPMakeTemporaryEphemerisDatabase import PPMakeTemporaryEphemerisDatabase
    from sorcha.readers.OIFReader import read_full_oif_table

    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))
    stem_name = "testdb_PPIntermDB.db"
    daba = PPMakeTemporaryEphemerisDatabase(
        get_test_filepath("oiftestoutput.txt"), os.path.join(temp_path, stem_name), "whitespace"
    )

    cnx = sqlite3.connect(daba)
    cur = cnx.cursor()

    cur.execute("select * from interm")
    col_names = list(map(lambda x: x[0], cur.description))

    oif_database = pd.DataFrame(cur.fetchall(), columns=col_names)

    oif_file = read_full_oif_table(get_test_filepath("oiftestoutput.txt"), "whitespace")
    pd.testing.assert_frame_equal(oif_file, oif_database)

    cnx.close()

    return
