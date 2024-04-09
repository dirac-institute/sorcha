import numpy as np
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from sorcha.readers.OIFReader import OIFDataReader
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_OIFDataReader():
    """Test that we can read in the OIF data from multiple formats."""
    reader_ws = OIFDataReader(get_test_filepath("oiftestoutput.txt"), inputformat="whitespace")
    oif_file = reader_ws.read_rows()
    assert len(oif_file) == 9
    assert reader_ws.get_reader_info() == "OIFDataReader|CSVDataReader:" + get_test_filepath(
        "oiftestoutput.txt"
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
    assert_equal(expected_first_row, oif_file.iloc[0].values)

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
    assert_equal(column_headings, oif_file.columns.values)

    # Check we get the same results with the HDF5 data
    reader_h5 = OIFDataReader(get_test_filepath("oiftestoutput.h5"), inputformat="hdf5")
    oif_hdf5 = reader_h5.read_rows()
    assert_frame_equal(oif_file, oif_hdf5)
    assert reader_h5.get_reader_info() == "OIFDataReader|HDF5DataReader:" + get_test_filepath(
        "oiftestoutput.h5"
    )

    # Check we get the same results with the CSV data
    reader_csv = OIFDataReader(get_test_filepath("oiftestoutput.csv"), inputformat="csv")
    oif_csv = reader_csv.read_rows()
    assert_frame_equal(oif_file, oif_csv)
    assert reader_csv.get_reader_info() == "OIFDataReader|CSVDataReader:" + get_test_filepath(
        "oiftestoutput.csv"
    )


def test_OIFDataReader_wrong_data():
    """Test that we fail if we read an OIF data with the wrong type of data"""
    with pytest.raises(SystemExit) as e:
        reader_ws2 = OIFDataReader(get_test_filepath("testcolour.txt"), inputformat="whitespace")
        _ = reader_ws2.read_rows()
    assert e.type == SystemExit
    assert (
        e.value.code
        == "ERROR: OIFDataReader: column headings do not match expected OIF column headings. Check format of file."
    )


def test_OIFDataReader_wrong_format():
    """Test that we fail if we read an OIF data with the wrong type of data"""
    # Check an invalid file type.
    with pytest.raises(SystemExit) as e:
        _ = OIFDataReader(get_test_filepath("testcolour.txt"), inputformat="invalid")
    assert e.type == SystemExit

    # Check mismatched file types.
    with pytest.raises(SystemExit) as e:
        _ = OIFDataReader(get_test_filepath("oiftestoutput.txt"), inputformat="csv")
    assert e.type == SystemExit

    with pytest.raises(SystemExit) as e:
        _ = OIFDataReader(get_test_filepath("oiftestoutput.csv"), inputformat="whitespace")
    assert e.type == SystemExit
