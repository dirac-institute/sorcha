import numpy as np
import pytest
from numpy.testing import assert_equal

from sorcha.readers.HDF5Reader import HDF5DataReader
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


@pytest.mark.parametrize("use_cache", [True, False])
def test_HDF5DataReader_read_rows(use_cache):
    """Test that we can read in the OIF data from an HDF5 file."""
    reader = HDF5DataReader(get_test_filepath("oiftestoutput.h5"), cache_table=use_cache)
    oif_data = reader.read_rows()
    assert len(oif_data) == 9
    assert reader.get_reader_info() == "HDF5DataReader:" + get_test_filepath("oiftestoutput.h5")

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
    assert_equal(expected_first_row, oif_data.iloc[0].values)

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
    assert_equal(column_headings, oif_data.columns.values)

    # Read in rows 3, 4, 5, 6 + the header
    oif_data = reader.read_rows(3, 4)
    assert len(oif_data) == 4
    assert_equal(column_headings, oif_data.columns.values)
    assert_equal("S000021", oif_data.iloc[0].values[0])


@pytest.mark.parametrize("use_cache", [True, False])
def test_HDF5DataReader_read_objects(use_cache):
    """Test that we can read in the OIF data for specific object IDs only."""
    reader = HDF5DataReader(get_test_filepath("oiftestoutput.h5"), cache_table=use_cache)
    oif_data = reader.read_objects(["S000015", "S000044"])
    assert len(oif_data) == 5

    # Check that we correctly loaded the header information.
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
    assert_equal(column_headings, oif_data.columns.values)

    # Check that the first row matches.
    expected_first_row = np.array(
        [
            "S000015",
            60,
            59853.050544,
            668175640.541,
            23.682,
            312.82599,
            -0.143012,
            -49.366779,
            0.060345,
            444295081.174,
            -301086798.179,
            -499254823.262,
            1.334,
            2.899,
            -0.966,
            148508007.817,
            18043717.331,
            7819571.632,
            -4.132,
            27.288,
            11.702,
            11.073412,
        ],
        dtype="object",
    )
    assert_equal(expected_first_row, oif_data.iloc[0].values)

    # Check that the remaining rows have the correct IDs.
    assert_equal(oif_data.iloc[1].values[0], "S000015")
    assert_equal(oif_data.iloc[2].values[0], "S000044")
    assert_equal(oif_data.iloc[3].values[0], "S000044")
    assert_equal(oif_data.iloc[4].values[0], "S000044")

    # Read different object IDs.
    oif_data2 = reader.read_objects(["S000021"])
    assert len(oif_data2) == 1
    assert_equal(oif_data2.iloc[0].values[0], "S000021")
