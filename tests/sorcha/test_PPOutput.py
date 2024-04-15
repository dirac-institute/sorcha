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
    os.remove(os.path.join(tmp_path, "PPOutput_test_all.csv"))


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
    cur.execute("select * from sorcha_results")
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
    cur.execute("select * from sorcha_results")
    col_names = list(map(lambda x: x[0], cur.description))
    sql_test_in = pd.DataFrame(cur.fetchall(), columns=col_names)

    expected = np.array(
        [
            "S1000000a",
            61769.320619,
            163.8754209,
            -18.8432714,
            164.037713,
            -17.582575,
            3e-06,
            "r",
            19.648,
            0.007,
            23.839,
            18.341701,
            393817194.335,
            -22.515,
            453089476.3503012,
        ],
        dtype=object,
    )

    assert_equal(csv_test_in.loc[0, :].values, expected)
    assert_equal(sql_test_in.loc[0, :].values, expected)

    # additional test to ensure that "all" output option and no rounding works

    configs = {
        "output_size": "all",
        "position_decimals": None,
        "magnitude_decimals": None,
        "output_format": "csv",
    }

    args.outfilestem = "PPOutput_test_all"

    PPWriteOutput(args, configs, observations, 10)

    all_test_in = pd.read_csv(os.path.join(tmp_path, "PPOutput_test_all.csv"))

    expected_all = np.array(
        [
            "S1000000a",
            894816,
            61769.320619,
            393817194.335,
            -22.515,
            164.0377129999997,
            0.059181,
            -17.582575000001285,
            -0.103034,
            -381360770.152,
            236918119.898,
            -61023282.708,
            -8.456,
            -15.118,
            -2.703,
            -20416770.015,
            133676144.369,
            57941007.918,
            -30.238,
            -4.221,
            -1.691,
            18.341701,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.15,
            "COM",
            3.01822,
            0.05208,
            22.56035,
            211.00286,
            335.42134,
            51575.94061,
            14.2,
            54800.0,
            "r",
            1.0585375509059165,
            1.2244982371118207,
            23.86356436464961,
            163.87542090842982,
            -18.84327137012991,
            115.45370443821976,
            19.6553455147994,
            19.65971332007237,
            23.839403736057715,
            2.9880927198448093e-06,
            0.0067559265881139,
            159.7413150392024,
            0.0067756541324796,
            19.64807294986914,
            19.647048752490328,
            164.037713,
            -17.582575,
            66.0,
            19,
            453089476.3503012,
        ],
        dtype=object,
    )

    assert_equal(all_test_in.loc[0, :].values, expected_all)

    return
