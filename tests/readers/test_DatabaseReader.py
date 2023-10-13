import os
import numpy as np
import tempfile

from numpy.testing import assert_equal

from sorcha.readers.DatabaseReader import DatabaseReader
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_DatabaseReader_objects():
    db_file = get_test_filepath("testdb_PPIntermDB.db")

    eph_reader = DatabaseReader(db_file)
    eph_data = eph_reader.read_objects(["S000015", "S000044"])
    assert len(eph_data) == 5
    assert eph_reader.get_reader_info() == "DatabaseReader:" + db_file

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
    assert_equal(column_headings, eph_data.columns.values)

    # Check that we load the correct object ids.
    for i in range(5):
        assert (eph_data.iloc[i].values[0] == "S000015") or (eph_data.iloc[i].values[0] == "S000044")

    # Read different object IDs.
    eph_data2 = eph_reader.read_objects(["S000021"])
    assert len(eph_data2) == 1
    assert_equal(eph_data2.iloc[0].values[0], "S000021")


def test_DatabaseReader_lines():
    db_file = get_test_filepath("testdb_PPIntermDB.db")

    eph_reader = DatabaseReader(db_file)
    eph_data = eph_reader.read_rows()
    assert len(eph_data) == 9

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
    assert_equal(expected_first_row, eph_data.iloc[0].values)

    # Read in rows 3, 4, 5, 6 + the header
    eph_data = eph_reader.read_rows(3, 4)
    assert len(eph_data) == 4
    assert_equal("S000021", eph_data.iloc[0].values[0])
