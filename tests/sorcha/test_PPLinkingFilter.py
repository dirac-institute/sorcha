import pandas as pd
import numpy as np
from numpy.testing import assert_equal

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_PPLinkingFilter():
    from sorcha.modules.PPLinkingFilter import PPLinkingFilter

    test_data = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=20)

    rng = np.random.default_rng(2021)

    detection_efficiency = 0.95
    min_observations = 2
    min_tracklets = 3
    tracklet_interval = 15
    minimum_separation = 0.5

    test_data_out = PPLinkingFilter(
        test_data,
        detection_efficiency,
        min_observations,
        min_tracklets,
        tracklet_interval,
        minimum_separation,
        rng,
    )

    expected = [
        907416,
        907470,
        909426,
        909452,
        910850,
        910872,
        915246,
        922013,
        922034,
        922035,
        926281,
        926288,
    ]

    assert_equal(test_data_out["FieldID"].values, expected)

    return
