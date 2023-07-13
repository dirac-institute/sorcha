import pandas as pd
from pandas.testing import assert_frame_equal

from surveySimPP.utilities.test_data_utilities import get_test_filepath


def test_PPReadCometaryParameters():
    from surveySimPP.modules.PPReadCometaryParameters import PPReadCometaryParameters

    observations = PPReadCometaryParameters(get_test_filepath("testcomet.txt"), 0, 1, "whitespace")

    expected = pd.DataFrame({"ObjID": ["67P/Churyumov-Gerasimenko"], "afrho1": [1552], "k": [-3.35]})

    assert_frame_equal(observations, expected)

    return
