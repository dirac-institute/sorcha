import pandas as pd
import numpy as np
from numpy.testing import assert_equal

from sorcha.modules.PPModuleRNG import PerModuleRNG
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_PPDropObservations():
    from sorcha.modules.PPDetectionProbability import PPDetectionProbability
    from sorcha.modules.PPDropObservations import PPDropObservations

    test_data = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=10)
    test_data["detection_probability"] = PPDetectionProbability(test_data, fillFactor=0.8, w=0.1)

    test_out = PPDropObservations(test_data, PerModuleRNG(2021), "detection_probability")

    expected = [894816, 894838, 897478, 897521, 901987, 902035, 907363, 907416, 907470, 909426]

    assert_equal(test_out["FieldID"].values, expected)

    return
