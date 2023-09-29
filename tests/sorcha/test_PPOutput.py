import pandas as pd
import sqlite3
import os
import numpy as np
import pytest
from numpy.testing import assert_equal

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath
from sorcha.utilities.sorchaArguments import sorchaArguments


@pytest.fixture
def setup_and_teardown_for_PPOutWriteCSV():
    yield

    tmp_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))

    os.remove(os.path.join(tmp_path, "test_csv_out.csv"))


@pytest.fixture
def setup_and_teardown_for_PPOutWriteHDF5():
    yield

    tmp_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))

    os.remove(os.path.join(tmp_path, "test_hdf5_out.h5"))


@pytest.fixture
def setup_and_teardown_for_PPOutWriteSqlite3():
    yield

    tmp_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))

    os.remove(os.path.join(tmp_path, "test_sql_out.db"))


@pytest.fixture
def setup_and_teardown_for_PPWriteOutput():
    yield

    tmp_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))

    os.remove(os.path.join(tmp_path, "PPOutput_test_out.csv"))
    os.remove(os.path.join(tmp_path, "PPOutput_test_out.db"))


def test_PPOutWriteCSV(setup_and_teardown_for_PPOutWriteCSV):
    from sorcha.modules.PPOutput import PPOutWriteCSV

    observations = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=1)
    tmp_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))

    PPOutWriteCSV(observations, os.path.join(tmp_path, "test_csv_out.csv"))

    test_in = pd.read_csv(os.path.join(tmp_path, "test_csv_out.csv"))

    pd.testing.assert_frame_equal(observations, test_in)

    return


def test_PPOutWriteSqlite3(setup_and_teardown_for_PPOutWriteSqlite3):
    from sorcha.modules.PPOutput import PPOutWriteSqlite3

    observations = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=1)
    tmp_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))

    PPOutWriteSqlite3(observations, os.path.join(tmp_path, "test_sql_out.db"))

    cnx = sqlite3.connect(os.path.join(tmp_path, "test_sql_out.db"))
    cur = cnx.cursor()
    cur.execute("select * from pp_results")
    col_names = list(map(lambda x: x[0], cur.description))

    test_in = pd.DataFrame(cur.fetchall(), columns=col_names)

    pd.testing.assert_frame_equal(observations, test_in)

    return


def test_PPOutWriteHDF5(setup_and_teardown_for_PPOutWriteHDF5):
    from sorcha.modules.PPOutput import PPOutWriteHDF5

    observations = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=1)
    tmp_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))

    PPOutWriteHDF5(observations, os.path.join(tmp_path, "test_hdf5_out.h5"), "testchunk")

    test_in = pd.read_hdf(os.path.join(tmp_path, "test_hdf5_out.h5"), key="testchunk")

    pd.testing.assert_frame_equal(observations, test_in)

    return


def test_PPWriteOutput(setup_and_teardown_for_PPWriteOutput):
    from sorcha.modules.PPOutput import PPWriteOutput

    observations = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=1)
    tmp_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))

    args = sorchaArguments()
    args.outpath = tmp_path
    args.outfilestem = "PPOutput_test_out"

    configs = {
        "output_size": "basic",
        "position_decimals": 7,
        "magnitude_decimals": 3,
        "output_format": "csv",
    }

    PPWriteOutput(args, configs, observations, 10)
    csv_test_in = pd.read_csv(os.path.join(tmp_path, "PPOutput_test_out.csv"))

    configs["output_format"] = "sqlite3"
    PPWriteOutput(args, configs, observations, 10)
    cnx = sqlite3.connect(os.path.join(tmp_path, "PPOutput_test_out.db"))
    cur = cnx.cursor()
    cur.execute("select * from pp_results")
    col_names = list(map(lambda x: x[0], cur.description))
    sql_test_in = pd.DataFrame(cur.fetchall(), columns=col_names)

    expected = np.array(
        [
            "S1000000a",
            61769.32062,
            163.8754209,
            -18.8432714,
            164.037713,
            -17.582575,
            3e-06,
            "r",
            19.647,
            19.648,
            0.007,
            0.007,
            23.864,
            23.839,
        ],
        dtype=object,
    )

    assert_equal(csv_test_in.loc[0, :].values, expected)
    assert_equal(sql_test_in.loc[0, :].values, expected)

    return
