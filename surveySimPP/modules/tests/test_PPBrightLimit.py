#!/bin/python

import pandas as pd
from surveySimPP.tests.data import get_test_filepath


def test_PPBrightLimit():
    from surveySimPP.modules.PPBrightLimit import PPBrightLimit

    test_input = pd.read_csv(get_test_filepath("test_input_fullobs.csv"))
    test_output = pd.read_csv(get_test_filepath("test_output_PPBrightLimit.csv"))

    test_result = PPBrightLimit(test_input, 'r', 20.0)

    pd.testing.assert_frame_equal(test_output, test_result)

    return
