import numpy as np
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from sorcha.readers.EphemerisReader import EphemerisDataReader
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_EphemerisDataReader():
    """Test that we can read in the ephemeris data from multiple formats."""
    reader_ws = EphemerisDataReader(get_test_filepath("ephemtestoutput.txt"), inputformat="whitespace")
    ephem_file = reader_ws.read_rows()
    assert len(ephem_file) == 9
    assert reader_ws.get_reader_info() == "EphemerisDataReader|CSVDataReader:" + get_test_filepath(
        "ephemtestoutput.txt"
    )

    expected_first_row = np.array(
        [
            "S00000t",
            379,
            59853.205174,
            283890475.515,
            -1.12,
            11.969664,
            -0.280799,
            -0.19939,
            -0.132793,
            426166274.581,
            77286024.759,
            6987943.309,
            -2.356,
            11.386,
            4.087,
            148449956.422,
            18409281.409,
            7975891.432,
            -4.574,
            27.377,
            11.699,
            2.030016,
        ],
        dtype="object",
    )
    assert_equal(expected_first_row, ephem_file.iloc[0].values)

    column_headings = np.array(
        [
            "ObjID",
            "FieldID",
            "fieldMJD_TAI",
            "Range_LTC_km",
            "RangeRate_LTC_km_s",
            "RA_deg",
            "RARateCosDec_deg_day",
            "Dec_deg",
            "DecRate_deg_day",
            "Obj_Sun_x_LTC_km",
            "Obj_Sun_y_LTC_km",
            "Obj_Sun_z_LTC_km",
            "Obj_Sun_vx_LTC_km_s",
            "Obj_Sun_vy_LTC_km_s",
            "Obj_Sun_vz_LTC_km_s",
            "Obs_Sun_x_km",
            "Obs_Sun_y_km",
            "Obs_Sun_z_km",
            "Obs_Sun_vx_km_s",
            "Obs_Sun_vy_km_s",
            "Obs_Sun_vz_km_s",
            "phase_deg",
        ],
        dtype=object,
    )
    assert_equal(column_headings, ephem_file.columns.values)

    # Check we get the same results with the HDF5 data
    reader_h5 = EphemerisDataReader(get_test_filepath("ephemtestoutput.h5"), inputformat="hdf5")
    ephem_hdf5 = reader_h5.read_rows()
    assert_frame_equal(ephem_file, ephem_hdf5)
    assert reader_h5.get_reader_info() == "EphemerisDataReader|HDF5DataReader:" + get_test_filepath(
        "ephemtestoutput.h5"
    )

    # Check we get the same results with the CSV data
    reader_csv = EphemerisDataReader(get_test_filepath("ephemtestoutput.csv"), inputformat="csv")
    ephem_csv = reader_csv.read_rows()
    assert_frame_equal(ephem_file, ephem_csv)
    assert reader_csv.get_reader_info() == "EphemerisDataReader|CSVDataReader:" + get_test_filepath(
        "ephemtestoutput.csv"
    )


def test_EphemerisDataReader_wrong_data():
    """Test that we fail if we read an ephem data with the wrong type of data"""
    with pytest.raises(SystemExit) as e:
        reader_ws2 = EphemerisDataReader(get_test_filepath("testcolour.txt"), inputformat="whitespace")
        _ = reader_ws2.read_rows()
    assert e.type == SystemExit
    assert (
        e.value.code
        == "ERROR: EphemerisDataReader: column headings do not match expected ephemeris column headings. Check format of file."
    )


def test_EphemerisDataReader_wrong_format():
    """Test that we fail if we read an ephemeris file with the wrong type of data"""
    # Check an invalid file type.
    with pytest.raises(SystemExit) as e:
        _ = EphemerisDataReader(get_test_filepath("testcolour.txt"), inputformat="invalid")
    assert e.type == SystemExit

    # Check mismatched file types.
    with pytest.raises(SystemExit) as e:
        _ = EphemerisDataReader(get_test_filepath("ephemtestoutput.txt"), inputformat="csv")
    assert e.type == SystemExit

    with pytest.raises(SystemExit) as e:
        _ = EphemerisDataReader(get_test_filepath("ephemtestoutput.csv"), inputformat="whitespace")
    assert e.type == SystemExit
