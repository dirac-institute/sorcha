import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from surveySimPP.readers.CSVReader import CSVDataReader
from surveySimPP.tests.data import get_test_filepath
    

def test_CSVDataReader_orbits():
    """Test that we can read in the orbit data.

    This test does not perform any transformations, filtering, or validation of the orbit data.
    It just loads it directly from a CSV.
    """
    orbit_des_reader = CSVDataReader(get_test_filepath("testorb.des"), "whitespace")
    assert orbit_des_reader.header_row == 0
    orbit_des = orbit_des_reader.read_rows()

    orbit_csv_reader = CSVDataReader(get_test_filepath("testorb.csv"), "csv")
    assert orbit_csv_reader.header_row == 0
    orbit_csv = orbit_des_reader.read_rows()

    # Check that the two files are the same.
    assert_frame_equal(orbit_csv, orbit_des)

    # Check that the column names and first row match expectations.
    expected_first_row = np.array(
        [
            "S00000t",
            "COM",
            0.952105479028,
            0.504888475701,
            4.899098347472,
            148.881068605772,
            39.949789586436,
            54486.32292808,
            54466.0,
            1,
            6, 
            0.0158834222877167,
            "MOPS"
        ],
        dtype=object,
    )
    
    expected_columns = np.array(
        [
            "ObjID",
            "FORMAT",
             "q",
            "e",
            "i",
            "node",
            "argperi",
            "t_p",
            "t_0",
            "INDEX",
            "N_PAR",
            "MOID",
            "COMPCODE",
        ], dtype=object
    )
    assert_equal(expected_first_row, orbit_des.iloc[0].values)
    assert_equal(expected_columns, orbit_des.columns.values)
    assert len(orbit_des) == 5

    with pytest.raises(SystemExit) as e2:
        bad_reader = CSVDataReader(get_test_filepath("testorb.csv"), "whitespace")
        bad_table = bad_reader.read_rows()        
    assert e2.type == SystemExit


def test_CSVDataReader_parameters():
    """Test that we can read in the parameters data.

    This test does not perform any transformations, filtering, or validation of the parameters data.
    It just loads it directly from a CSV.
    """
    # Only read in the first two lines.
    txt_reader = CSVDataReader(get_test_filepath("testcolour.txt"), "whitespace")
    assert txt_reader.header_row == 0
    params_txt = txt_reader.read_rows(0, 2)
    assert len(params_txt) == 2

    csv_reader = CSVDataReader(get_test_filepath("testcolour.csv"), "csv")
    assert csv_reader.header_row == 0
    params_csv = csv_reader.read_rows(0, 2)
    assert len(params_txt) == 2

    expected_first_line = np.array(
        ["S00000t", 17.615, 0.3, 0.0, 0.1, 0.15], dtype=object
    )
    expected_columns = np.array(
        ["ObjID", "H_r", "g-r", "i-r", "z-r", "GS"], dtype=object
    )
    assert_frame_equal(params_txt, params_csv)

    assert_equal(params_txt.iloc[0].values, expected_first_line)
    assert_equal(params_txt.columns.values, expected_columns)

    # Check a bad read.
    with pytest.raises(SystemExit) as e1:
        bad_reader = CSVDataReader(get_test_filepath("testcolour.txt"), "csv")
        bad_table = bad_reader.read_rows()        
    assert e1.type == SystemExit

    # Test reading the full text file.
    params_txt2 = txt_reader.read_rows()
    assert len(params_txt2) == 5
