import pytest
import pandas as pd
import sqlite3
import os
from pandas.testing import assert_frame_equal

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


class args:
    def __init__(self, tmp_path):
        temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))

        args.filename = os.path.join(tmp_path, "test_res_database.db")
        args.inputs = temp_path
        args.outputs = temp_path
        args.stem = "sqlresults"
        args.comet = False


def test_get_column_names():
    from sorcha.utilities.createResultsSQLDatabase import get_column_names

    col_names = get_column_names(get_test_filepath("sqlresults.db"))

    expected_colnames = [
        "ObjID",
        "FieldMJD_TAI",
        "fieldRA",
        "fieldDec",
        "AstRA(deg)",
        "AstDec(deg)",
        "AstrometricSigma(deg)",
        "optFilter",
        "observedPSFMag",
        "observedTrailedSourceMag",
        "PhotometricSigmaPSF(mag)",
        "PhotometricSigmaTrailedSource(mag)",
        "fiveSigmaDepth",
        "fiveSigmaDepthAtSource",
    ]

    assert col_names == expected_colnames

    return


def test_create_inputs_table(tmp_path):
    from sorcha.utilities.createResultsSQLDatabase import create_inputs_table

    data_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))

    cnx_out = sqlite3.connect(os.path.join(tmp_path, "test_inputs_table.db"))
    create_inputs_table(cnx_out, data_path, "params")
    cnx_out.close()

    cnx_in = sqlite3.connect(os.path.join(tmp_path, "test_inputs_table.db"))
    cur = cnx_in.cursor()
    cur.execute("select * from params")
    col_names = list(map(lambda x: x[0], cur.description))
    test_inputs = pd.DataFrame(cur.fetchall(), columns=col_names)
    cnx_in.close()

    test_inputs.drop("index", axis=1, inplace=True)
    test_inputs.sort_values("ObjID", inplace=True)
    test_inputs.reset_index(drop=True, inplace=True)

    expected_inputs = pd.read_csv(get_test_filepath("testcolour.txt"), delim_whitespace=True)

    assert_frame_equal(test_inputs, expected_inputs)

    with pytest.raises(SystemExit) as e:
        cnx_err = sqlite3.connect(os.path.join(tmp_path, "test_dummy.db"))
        create_inputs_table(cnx_out, data_path, "dummy")
        cnx_err.close()

    assert e.type == SystemExit
    assert e.value.code == "Could not find any dummy files in given inputs folder."

    return


def test_create_results_table(tmp_path):
    from sorcha.utilities.createResultsSQLDatabase import create_results_table

    data_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))

    cnx_out = sqlite3.connect(os.path.join(tmp_path, "test_results_table.db"))
    create_results_table(cnx_out, get_test_filepath("baseline_10klines_2.0.db"), data_path, "sqlresults")
    cnx_out.close()

    cnx_in = sqlite3.connect(os.path.join(tmp_path, "test_results_table.db"))
    cur = cnx_in.cursor()
    cur.execute("select * from pp_results")
    col_names = list(map(lambda x: x[0], cur.description))
    test_inputs = pd.DataFrame(cur.fetchall(), columns=col_names)
    cnx_out.close()

    expected_inputs = pd.read_csv(get_test_filepath("testobs_clean.csv"))

    assert_frame_equal(test_inputs, expected_inputs)

    with pytest.raises(SystemExit) as e:
        cnx_out = sqlite3.connect(os.path.join(tmp_path, "test_dummy.db"))
        create_results_table(cnx_out, get_test_filepath("baseline_10klines_2.0.db"), data_path, "dummy")
        cnx_out.close()

    assert e.type == SystemExit
    assert e.value.code == "Could not find any .db files using given filepath and stem."

    return


def test_create_results_database(tmp_path):
    from sorcha.utilities.createResultsSQLDatabase import create_results_database

    test_args = args(tmp_path)

    create_results_database(test_args)

    cnx_in = sqlite3.connect(os.path.join(tmp_path, "test_res_database.db"))
    cur = cnx_in.cursor()

    cur.execute("select * from orbits")
    col_names = list(map(lambda x: x[0], cur.description))
    test_orbits = pd.DataFrame(cur.fetchall(), columns=col_names)

    cur.execute("select * from pp_results")
    col_names = list(map(lambda x: x[0], cur.description))
    test_results = pd.DataFrame(cur.fetchall(), columns=col_names)

    cnx_in.close()

    test_orbits.drop("index", axis=1, inplace=True)
    test_orbits.sort_values("ObjID", inplace=True)
    test_orbits.rename(columns={"orig_index": "INDEX"}, inplace=True)
    test_orbits.reset_index(drop=True, inplace=True)

    expected_orbits = pd.read_csv(get_test_filepath("testorb.des"), delim_whitespace=True)
    expected_results = pd.read_csv(get_test_filepath("testobs_clean.csv"))

    assert_frame_equal(test_orbits, expected_orbits)
    assert_frame_equal(test_results, expected_results)

    return
