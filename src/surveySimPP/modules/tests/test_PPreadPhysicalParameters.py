import numpy as np
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal
import pytest

from surveySimPP.tests.data import get_test_filepath


def test_PPReadPhysicalParameters():
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters

    params = PPReadPhysicalParameters(get_test_filepath("testcolour.txt"), 0, 3, "whitespace")
    params_csv = PPReadPhysicalParameters(get_test_filepath("testcolour.csv"), 0, 3, "csv")

    expected_first_line = np.array(["S00000t", 17.615, 0.3, 0.0, 0.1, 0.15], dtype=object)
    expected_columns = np.array(["ObjID", "H_r", "g-r", "i-r", "z-r", "GS"], dtype=object)

    assert_frame_equal(params, params_csv)

    assert_equal(params.iloc[0].values, expected_first_line)
    assert_equal(params.columns.values, expected_columns)

    assert len(params) == 3

    with pytest.raises(SystemExit) as e1:
        params = PPReadPhysicalParameters(get_test_filepath("testcolour.txt"), 0, 3, "csv")

    assert e1.type == SystemExit
    assert (
        e1.value.code
        == "ERROR: PPReadPhysicalParameters: Cannot find ObjID in column headings. Check input and input format."
    )

    return
