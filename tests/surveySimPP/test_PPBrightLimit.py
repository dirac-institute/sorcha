import pandas as pd
import numpy as np
import pytest

from numpy.testing import assert_equal


def test_PPBrightLimit():
    from sorcha.modules.PPBrightLimit import PPBrightLimit

    observation_ID = np.arange(1, 11)
    observation_filter = ["r", "r", "r", "r", "r", "g", "g", "g", "g", "g"]
    observation_mag = np.append(np.arange(10.0, 15.0), np.arange(10.0, 15.0))

    observations = pd.DataFrame(
        {"ObjID": observation_ID, "optFilter": observation_filter, "observedPSFMag": observation_mag}
    )

    observing_filters = ["r", "g"]

    result_single = PPBrightLimit(observations, observing_filters, 12.0)
    result_multiple = PPBrightLimit(observations, observing_filters, [12.0, 13.0])

    assert_equal(result_single["ObjID"].values, [3, 4, 5, 8, 9, 10])
    assert_equal(result_multiple["ObjID"].values, [3, 4, 5, 9, 10])

    with pytest.raises(SystemExit) as e:
        result_single = PPBrightLimit(observations, observing_filters, 12)

    assert e.type == SystemExit
    assert e.value.code == "ERROR: PPBrightLimit: expected a float or list of floats for bright_limit."

    return
