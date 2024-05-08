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
