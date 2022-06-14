#!/bin/python

import pandas as pd
from surveySimPP.tests.data import get_test_filepath

def test_PPSNRLimit():

    from surveySimPP.modules.PPSNRLimit import PPSNRLimit

    test_input = pd.read_csv(get_test_filepath("test_input_fullobs.csv"))

    test_output = pd.read_csv(get_test_filepath("test_output_PPSNRLimit.csv"))

    test_result = PPSNRLimit(test_input, 15.0)

    pd.testing.assert_frame_equal(test_output, test_result)
