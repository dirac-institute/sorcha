import numpy as np
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from surveySimPP.tests.data import get_test_filepath


def test_PPReadOrbitFile():
    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile

    orbit_file = PPReadOrbitFile(get_test_filepath("testorb.des"), 0, 14, "whitespace")
    orbit_csv = PPReadOrbitFile(get_test_filepath("testorb.csv"), 0, 14, "csv")

    expected_first_row = np.array(
        [
            "S00000t",
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

    expected_columns = np.array(["ObjID", "q", "e", "incl", "node", "argperi", "t_p", "t_0"], dtype=object)

    assert_frame_equal(orbit_csv, orbit_file)

    assert_equal(expected_first_row, orbit_file.iloc[0].values)
    assert_equal(expected_columns, orbit_file.columns.values)

    assert len(orbit_file) == 5

    with pytest.raises(SystemExit) as e1:
        orbit_file = PPReadOrbitFile(get_test_filepath("PPReadOrbitFile_bad.txt"), 0, 14, "whitespace")

    assert e1.type == SystemExit
    assert (
        e1.value.code
        == "ERROR: PPReadOrbitFile: H column present in orbits data file. H must be included in physical parameters file only."
    )

    with pytest.raises(SystemExit) as e2:
        orbit_csv = PPReadOrbitFile(get_test_filepath("testorb.csv"), 0, 14, "whitespace")

    assert e2.type == SystemExit
    assert (
        e2.value.code
        == "ERROR: PPReadOrbitFile: Cannot find ObjID in column headings. Check input and input format."
    )

    return
