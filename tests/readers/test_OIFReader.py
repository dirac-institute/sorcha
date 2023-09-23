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
            "FieldMJD_TAI",
            "AstRange(km)",
            "AstRangeRate(km/s)",
            "AstRA(deg)",
            "AstRARate(deg/day)",
            "AstDec(deg)",
            "AstDecRate(deg/day)",
            "Ast-Sun(J2000x)(km)",
            "Ast-Sun(J2000y)(km)",
            "Ast-Sun(J2000z)(km)",
            "Ast-Sun(J2000vx)(km/s)",
            "Ast-Sun(J2000vy)(km/s)",
            "Ast-Sun(J2000vz)(km/s)",
            "Obs-Sun(J2000x)(km)",
            "Obs-Sun(J2000y)(km)",
            "Obs-Sun(J2000z)(km)",
            "Obs-Sun(J2000vx)(km/s)",
            "Obs-Sun(J2000vy)(km/s)",
            "Obs-Sun(J2000vz)(km/s)",
            "Sun-Ast-Obs(deg)",
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

    # Check a mismatched file.
    with pytest.raises(SystemExit) as e:
        reader_ws2 = OIFDataReader(get_test_filepath("testcolour.txt"), inputformat="whitespace")
        _ = reader_ws2.read_rows()
    assert e.type == SystemExit
    assert (
        e.value.code
        == "ERROR: OIFDataReader: column headings do not match expected OIF column headings. Check format of file."
    )

    # Check an invalid file type.
    with pytest.raises(SystemExit) as e:
        reader_ws2 = OIFDataReader(get_test_filepath("testcolour.txt"), inputformat="invalid")
    assert e.type == SystemExit
