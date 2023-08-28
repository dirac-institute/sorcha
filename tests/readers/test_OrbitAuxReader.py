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
        ["ObjID", "FORMAT", "q", "e", "inc", "node", "argPeri", "t_p", "epoch"], dtype=object
    )
    assert_equal(expected_columns, orbit_txt.columns.values)

    # Check that we read the correct valude, including dropped columns.
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

    # Incosistent orbit formats
    with pytest.raises(SystemExit) as e3:
        reader = OrbitAuxReader(get_test_filepath("PPReadOrbitFile_bad_format.csv"), "csv")
        _ = reader.read_rows(0, 14)
    assert e3.type == SystemExit
    assert "consistent FORMAT" in str(e3.value)
