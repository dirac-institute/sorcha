import os
import pytest
import pandas as pd
import sqlite3
from pandas.testing import assert_frame_equal

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath
from sorcha.utilities.createTemporaryDatabases import make_temporary_databases


class args:
    def __init__(self, inputs, stem):
        args.inputs = inputs
        args.stem = stem
        args.chunk = 1e6
        args.force = False


@pytest.fixture
def teardown_for_createTemporaryDatabase():
    yield

    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))
    file1 = "temp_oif_temptest.db"

    os.remove(os.path.join(temp_path, file1))


def test_createTemporaryDatabase(teardown_for_createTemporaryDatabase):
    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))
    test_args = args(temp_path, "oif_")
    make_temporary_databases(test_args)

    expected = pd.read_csv(get_test_filepath("oiftestoutput.txt"), delim_whitespace=True)
    expected_database = expected.drop(["V", "V(H=0)"], axis=1)

    cnx = sqlite3.connect(get_test_filepath("temp_oif_temptest.db"))
    cur = cnx.cursor()
    cur.execute("select * from interm")
    col_names = list(map(lambda x: x[0], cur.description))

    test_database = pd.DataFrame(cur.fetchall(), columns=col_names)

    assert_frame_equal(test_database, expected_database)
