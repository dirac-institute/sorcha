import pandas as pd
import sqlite3
import os
import numpy as np
import pytest
from numpy.testing import assert_equal

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath, get_demo_filepath
from sorcha.utilities.sorchaArguments import sorchaArguments
from sorcha.modules.PPOutput import PPWriteOutput
from sorcha.utilities.sorchaConfigs import outputConfigs, linkingfilterConfigs, sorchaConfigs

# some global variables used by tests
observations = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=1)
args = sorchaArguments()


def test_PPOutWriteCSV(tmp_path):
    from sorcha.modules.PPOutput import PPOutWriteCSV

    PPOutWriteCSV(observations, os.path.join(tmp_path, "test_csv_out.csv"))

    test_in = pd.read_csv(os.path.join(tmp_path, "test_csv_out.csv"))

    pd.testing.assert_frame_equal(observations, test_in)


def test_PPOutWriteSqlite3(tmp_path):
    from sorcha.modules.PPOutput import PPOutWriteSqlite3

    PPOutWriteSqlite3(observations, os.path.join(tmp_path, "test_sql_out.db"))

    cnx = sqlite3.connect(os.path.join(tmp_path, "test_sql_out.db"))
    cur = cnx.cursor()
    cur.execute("select * from sorcha_results")
    col_names = list(map(lambda x: x[0], cur.description))

    test_in = pd.DataFrame(cur.fetchall(), columns=col_names)

    pd.testing.assert_frame_equal(observations, test_in)


def test_PPOutWriteHDF5(tmp_path):
    from sorcha.modules.PPOutput import PPOutWriteHDF5

    PPOutWriteHDF5(observations, os.path.join(tmp_path, "test_hdf5_out.h5"), "testchunk")

    test_in = pd.read_hdf(os.path.join(tmp_path, "test_hdf5_out.h5"), key="testchunk")

    pd.testing.assert_frame_equal(observations, test_in)


def test_PPWriteOutput_csv(tmp_path):
    args.outpath = tmp_path
    args.outfilestem = "PPOutput_test_out"
    config_file_location = get_demo_filepath("sorcha_config_demo.ini")
    configs = sorchaConfigs(config_file_location, "rubin_sim")
    configs.output.magnitude_decimals = 3
    configs.output.position_decimals = 7
    configs.linkingfilter.ssp_linking_on = False
    configs.linkingfilter.drop_unlinked = True

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

    # test basic CSV

    PPWriteOutput(args, configs, observations, 10)
    csv_test_in = pd.read_csv(os.path.join(tmp_path, "PPOutput_test_out.csv"))
    assert_equal(csv_test_in.loc[0, :].values, expected)


def test_PPWriteOutput_sql(tmp_path):
    from sorcha.modules.PPOutput import PPIndexSQLDatabase

    args.outpath = tmp_path
    args.outfilestem = "PPOutput_test_out"
    config_file_location = get_demo_filepath("sorcha_config_demo.ini")
    configs = sorchaConfigs(config_file_location, "rubin_sim")
    configs.output.magnitude_decimals = 3
    configs.output.position_decimals = 7
    configs.linkingfilter.ssp_linking_on = False
    configs.linkingfilter.drop_unlinked = True
    configs.output.output_format = "sqlite3"

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

    PPWriteOutput(args, configs, observations, 10)
    PPIndexSQLDatabase(os.path.join(tmp_path, "PPOutput_test_out.db"))

    cnx = sqlite3.connect(os.path.join(tmp_path, "PPOutput_test_out.db"))
    cur = cnx.cursor()
    cur.execute("select * from sorcha_results")
    col_names = list(map(lambda x: x[0], cur.description))
    sql_test_in = pd.DataFrame(cur.fetchall(), columns=col_names)

    assert_equal(sql_test_in.loc[0, :].values, expected)

    # check indexes were properly created
    cur.execute("PRAGMA index_list('sorcha_results')")
    indexes = cur.fetchall()

    index_list = [indexes[i][1] for i in range(0, 3)]
    assert index_list == ["optFilter", "fieldMJD_TAI", "ObjID"]


def test_PPWriteOutput_all(tmp_path):
    # additional test to ensure that "all" output option and no rounding works
    config_file_location = get_demo_filepath("sorcha_config_demo.ini")
    configs = sorchaConfigs(config_file_location, "rubin_sim")
    configs.linkingfilter.ssp_linking_on = False
    configs.linkingfilter.drop_unlinked = True
    configs.output.output_columns = "all"

    args.outpath = tmp_path
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


def test_PPWriteOutput_custom(tmp_path):

    config_file_location = get_demo_filepath("sorcha_config_demo.ini")
    configs = sorchaConfigs(config_file_location, "rubin_sim")
    configs.output.magnitude_decimals = 3
    configs.output.position_decimals = 7
    configs.linkingfilter.ssp_linking_on = False
    configs.linkingfilter.drop_unlinked = True
    out_dict = {
        "output_format": "csv",
        "output_columns": "ObjID , fieldMJD_TAI",
        "position_decimals": 7,
        "magnitude_decimals": 3,
    }
    configs.output = outputConfigs(**out_dict)

    args.outpath = tmp_path
    args.outfilestem = "PPOutput_test_multi"

    PPWriteOutput(args, configs, observations, 10)

    multi_test_in = pd.read_csv(os.path.join(tmp_path, "PPOutput_test_multi.csv"))

    expected_multi = np.array(["S1000000a", 61769.320619], dtype=object)

    assert_equal(multi_test_in.loc[0, :].values, expected_multi)

    # and now we test the error message

    configs = sorchaConfigs(config_file_location, "rubin_sim")
    configs.output.magnitude_decimals = 3
    configs.output.position_decimals = 7
    configs.linkingfilter.ssp_linking_on = False
    configs.linkingfilter.drop_unlinked = True
    out_dict = {
        "output_format": "csv",
        "output_columns": "ObjID , fieldMJD_TAI, dummy_column",
        "position_decimals": 7,
        "magnitude_decimals": 3,
    }
    configs.output = outputConfigs(**out_dict)

    with pytest.raises(SystemExit) as e:
        PPWriteOutput(args, configs, observations, 10)

    assert (
        e.value.code
        == "ERROR: at least one of the columns provided in output_columns does not seem to exist. Check docs and try again."
    )


def test_PPWriteOutput_linking_col(tmp_path):
    args.outpath = tmp_path
    args.outfilestem = "PPOutput_test_linking"

    observations_linktest = observations.copy()

    observations_linktest["object_linked"] = [True]

    config_file_location = get_demo_filepath("sorcha_config_demo.ini")
    configs = sorchaConfigs(config_file_location, "rubin_sim")
    configs.output.magnitude_decimals = 3
    configs.output.position_decimals = 7
    configs.linkingfilter.ssp_linking_on = True
    configs.linkingfilter.drop_unlinked = False

    PPWriteOutput(args, configs, observations_linktest, 10)
    csv_test_in = pd.read_csv(os.path.join(tmp_path, "PPOutput_test_linking.csv"))
    assert "object_linked" in csv_test_in.columns
