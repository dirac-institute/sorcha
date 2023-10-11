import numpy as np
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from sorcha.readers.OrbitAuxReader import OrbitAuxReader
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_OrbitAuxReader():
    txt_reader = OrbitAuxReader(get_test_filepath("testorb.des"), "whitespace")
    orbit_txt = txt_reader.read_rows()
    assert_equal(len(orbit_txt), 5)
    assert txt_reader.get_reader_info() == "OrbitAuxReader:" + get_test_filepath("testorb.des")

    csv_reader = OrbitAuxReader(get_test_filepath("testorb.csv"), "csv")
    orbit_csv = csv_reader.read_rows()
    assert_equal(len(orbit_csv), 5)

    # Check we get the same results from both formats.
    assert_frame_equal(orbit_csv, orbit_txt)

    # Check that we modify the columns (i -> incl, etc.)
    expected_columns = np.array(
        ["ObjID", "FORMAT", "q", "e", "inc", "node", "argPeri", "t_p_MJD_TDB", "epochMJD_TDB"], dtype=object
    )
    assert_equal(expected_columns, orbit_txt.columns.values)

    # Check that we read the correct value, including dropped columns.
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
        ],
        dtype=object,
    )
    assert_equal(expected_first_row, orbit_txt.iloc[0].values)

    # No format provided
    with pytest.raises(SystemExit) as e1:
        reader = OrbitAuxReader(get_test_filepath("PPReadOrbitFile_bad.txt"), "whitespace")
        _ = reader.read_rows(0, 14)
    assert e1.type == SystemExit
    assert e1.value.code == "ERROR: PPReadOrbitFile: Orbit format must be provided."

    # Incorrect format
    with pytest.raises(SystemExit) as e2:
        reader = OrbitAuxReader(get_test_filepath("testorb.csv"), "whitespace")
        _ = reader.read_rows(0, 14)
    assert e2.type == SystemExit

    # Inconsistent orbit formats
    with pytest.raises(SystemExit) as e3:
        reader = OrbitAuxReader(get_test_filepath("PPReadOrbitFile_bad_format.csv"), "csv")
        _ = reader.read_rows(0, 14)
    assert e3.type == SystemExit
    assert "consistent FORMAT" in str(e3.value)


# Cometary section
def test_orbit_reader_com():
    """Base case for cometary orbit files"""
    csv_reader = OrbitAuxReader(get_test_filepath("orbit_test_files/orbit_com.csv"), "csv")
    orbit_csv = csv_reader.read_rows()
    assert_equal(len(orbit_csv), 5)

    # Check that we modify the columns (i -> incl, etc.)
    expected_columns = np.array(
        ["ObjID", "FORMAT", "q", "e", "inc", "node", "argPeri", "t_p_MJD_TDB", "epochMJD_TDB"], dtype=object
    )
    assert_equal(expected_columns, orbit_csv.columns.values)

    # Check that we read the correct value, including dropped columns.
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
        ],
        dtype=object,
    )
    assert_equal(expected_first_row, orbit_csv.iloc[0].values)


def test_orbit_reader_com_wrong_columns():
    """If the wrong columns for the format defined in the orbit file, raise
    exception.
    """
    csv_reader = OrbitAuxReader(get_test_filepath("orbit_test_files/orbit_com_wrong_cols.csv"), "csv")

    with pytest.raises(SystemExit) as err:
        _ = csv_reader.read_rows()
    assert "all cometary" in str(err.value)


def test_orbit_reader_bcom():
    """Base case for barycentric cometary orbit files"""
    csv_reader = OrbitAuxReader(get_test_filepath("orbit_test_files/orbit_bcom.csv"), "csv")
    orbit_csv = csv_reader.read_rows()
    assert_equal(len(orbit_csv), 5)

    # Check that we modify the columns (i -> incl, etc.)
    expected_columns = np.array(
        ["ObjID", "FORMAT", "q", "e", "inc", "node", "argPeri", "t_p_MJD_TDB", "epochMJD_TDB"], dtype=object
    )
    assert_equal(expected_columns, orbit_csv.columns.values)

    # Check that we read the correct value, including dropped columns.
    expected_first_row = np.array(
        [
            "S00000t",
            "BCOM",
            0.952105479028,
            0.504888475701,
            4.899098347472,
            148.881068605772,
            39.949789586436,
            54486.32292808,
            54466.0,
        ],
        dtype=object,
    )
    assert_equal(expected_first_row, orbit_csv.iloc[0].values)


# Keplerian orbit section
def test_orbit_reader_kep():
    """Base case test for keplerian orbit files"""
    csv_reader = OrbitAuxReader(get_test_filepath("orbit_test_files/orbit_kep.csv"), "csv")
    orbit_csv = csv_reader.read_rows()
    assert_equal(len(orbit_csv), 5)

    # Check that we modify the columns (i -> incl, etc.)
    expected_columns = np.array(
        ["ObjID", "FORMAT", "a", "e", "inc", "node", "argPeri", "ma", "epochMJD_TDB"], dtype=object
    )
    assert_equal(expected_columns, orbit_csv.columns.values)

    # Check that we read the correct value, including dropped columns.
    expected_first_row = np.array(
        [
            "S00000t",
            "KEP",
            0.952105479028,
            0.504888475701,
            4.899098347472,
            148.881068605772,
            39.949789586436,
            54486.32292808,
            54466.0,
        ],
        dtype=object,
    )
    assert_equal(expected_first_row, orbit_csv.iloc[0].values)


def test_orbit_reader_kep_wrong_columns():
    """If the wrong columns for the format defined in the orbit file, raise
    exception.
    """
    csv_reader = OrbitAuxReader(get_test_filepath("orbit_test_files/orbit_kep_wrong_cols.csv"), "csv")

    with pytest.raises(SystemExit) as err:
        _ = csv_reader.read_rows()
    assert "all keplerian" in str(err.value)


def test_orbit_reader_bkep():
    """Base case for barycentric keplerian orbit files"""
    csv_reader = OrbitAuxReader(get_test_filepath("orbit_test_files/orbit_bkep.csv"), "csv")
    orbit_csv = csv_reader.read_rows()
    assert_equal(len(orbit_csv), 5)

    # Check that we modify the columns (i -> incl, etc.)
    expected_columns = np.array(
        ["ObjID", "FORMAT", "a", "e", "inc", "node", "argPeri", "ma", "epochMJD_TDB"], dtype=object
    )
    assert_equal(expected_columns, orbit_csv.columns.values)

    # Check that we read the correct value, including dropped columns.
    expected_first_row = np.array(
        [
            "S00000t",
            "BKEP",
            0.952105479028,
            0.504888475701,
            4.899098347472,
            148.881068605772,
            39.949789586436,
            54486.32292808,
            54466.0,
        ],
        dtype=object,
    )
    assert_equal(expected_first_row, orbit_csv.iloc[0].values)


# Cartesian orbit section
def test_orbit_reader_cart():
    """Base case test for cartesian orbit files"""
    csv_reader = OrbitAuxReader(get_test_filepath("orbit_test_files/orbit_cart.csv"), "csv")
    orbit_csv = csv_reader.read_rows()
    assert_equal(len(orbit_csv), 5)

    expected_columns = np.array(
        ["ObjID", "FORMAT", "x", "y", "z", "xdot", "ydot", "zdot", "epochMJD_TDB"], dtype=object
    )
    assert_equal(expected_columns, orbit_csv.columns.values)

    # Check that we read the correct value, including dropped columns.
    expected_first_row = np.array(
        [
            "S00000t",
            "CART",
            0.952105479028,
            0.504888475701,
            4.899098347472,
            148.881068605772,
            39.949789586436,
            54486.32292808,
            54466.0,
        ],
        dtype=object,
    )
    assert_equal(expected_first_row, orbit_csv.iloc[0].values)


def test_orbit_reader_cart_wrong_columns():
    """If the wrong columns for the format defined in the orbit file, raise
    exception.
    """
    csv_reader = OrbitAuxReader(get_test_filepath("orbit_test_files/orbit_cart_wrong_cols.csv"), "csv")

    with pytest.raises(SystemExit) as err:
        _ = csv_reader.read_rows()
    assert "all cartesian" in str(err.value)


def test_orbit_reader_bcart():
    """Base case for barycentric cartesian orbit files"""
    csv_reader = OrbitAuxReader(get_test_filepath("orbit_test_files/orbit_bcart.csv"), "csv")
    orbit_csv = csv_reader.read_rows()
    assert_equal(len(orbit_csv), 5)

    # Check that we modify the columns (i -> incl, etc.)
    expected_columns = np.array(
        ["ObjID", "FORMAT", "x", "y", "z", "xdot", "ydot", "zdot", "epochMJD_TDB"], dtype=object
    )
    assert_equal(expected_columns, orbit_csv.columns.values)

    # Check that we read the correct value, including dropped columns.
    expected_first_row = np.array(
        [
            "S00000t",
            "BCART",
            0.952105479028,
            0.504888475701,
            4.899098347472,
            148.881068605772,
            39.949789586436,
            54486.32292808,
            54466.0,
        ],
        dtype=object,
    )
    assert_equal(expected_first_row, orbit_csv.iloc[0].values)


def test_orbit_reader_unknown_format():
    """If an unknown format is defined, raise an exception"""
    csv_reader = OrbitAuxReader(get_test_filepath("orbit_test_files/orbit_unknown_format.csv"), "csv")

    with pytest.raises(SystemExit) as err:
        _ = csv_reader.read_rows()
    assert "must be one of" in str(err.value)


def test_orbit_reader_extra_columns():
    """If more than 9 columns are provided, raise an exception"""
    csv_reader = OrbitAuxReader(get_test_filepath("orbit_test_files/orbit_extra_cols.csv"), "csv")

    with pytest.raises(SystemExit) as err:
        _ = csv_reader.read_rows()
    assert "only provide the required columns" in str(err.value)
