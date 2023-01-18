#!/bin/python

import pandas as pd
from numpy.testing import assert_equal
from surveySimPP.tests.data import get_test_filepath


def test_PPBrightLimit():
    from surveySimPP.modules.PPBrightLimit import PPBrightLimit

    observations = pd.read_csv(get_test_filepath('test_input_fullobs.csv'))

    result_single = PPBrightLimit(observations, 'r', 23.5)
    expected = [949544, 949566, 950165, 951923, 954563, 213178, 214204, 219154,
                219204]

    assert_equal(result_single['FieldID'].values, expected)

    observing_filters = ['r', 'u', 'g', 'i', 'z']
    bright_limits = [23.5, 23., 23.5, 26., 26.]

    result_multiple = PPBrightLimit(observations, observing_filters, bright_limits)
    expected_multiple = [949544, 950165, 951923, 213178, 214204, 219154]

    assert_equal(result_multiple['FieldID'].values, expected_multiple)

    return
