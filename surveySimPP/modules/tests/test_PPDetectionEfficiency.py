#!/bin/python

import pandas as pd
import numpy as np
from numpy.testing import assert_equal

from surveySimPP.tests.data import get_test_filepath


def test_PPDetectionEfficiency():

    from surveySimPP.modules.PPDetectionEfficiency import PPDetectionEfficiency

    rng = np.random.default_rng(2021)

    test_data = pd.read_csv(get_test_filepath('test_input_fullobs.csv'))

    test_out = PPDetectionEfficiency(test_data[0:15], 0.95, rng)

    expected = [894816, 894838, 897478, 897521, 901987, 902035, 907363, 907416,
                907470, 909426, 909452, 910850, 910872, 915246]

    assert_equal(test_out['FieldID'].values, expected)

    return
