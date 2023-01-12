import pandas as pd
import numpy as np
from numpy.testing import assert_equal

from surveySimPP.tests.data import get_test_filepath


def test_PPLinkingFilter():

    from surveySimPP.modules.PPLinkingFilter import PPLinkingFilter

    test_data = pd.read_csv(get_test_filepath('test_input_fullobs.csv'))

    rng = np.random.default_rng(2021)

    detection_efficiency = 0.95
    min_observations = 2
    min_tracklets = 3
    tracklet_interval = 15
    minimum_separation = 0.5

    # this line may seem pointless but Pandas does NOT like operating on slices
    # of dataframes as it can't tell if it's a view or a copy and will throw a
    # warning if this line is removed, so the test will fail.
    test_obs = test_data[0:20].copy()

    test_data_out = PPLinkingFilter(test_obs,
                                    detection_efficiency,
                                    min_observations,
                                    min_tracklets,
                                    tracklet_interval,
                                    minimum_separation,
                                    rng)

    expected = [894816, 894838, 897478, 897521, 901987, 902035, 907363, 907416,
                907470, 909426, 909452, 910850, 910872, 915246, 922013, 922034,
                922035, 926281, 926288]

    assert_equal(test_data_out['FieldID'].values, expected)

    return
