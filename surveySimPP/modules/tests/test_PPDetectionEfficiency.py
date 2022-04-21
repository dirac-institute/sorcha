#!/bin/python

import pytest
import pandas as pd
#from filtering import PPFilterDetectionEfficiencyThreshold


"""
test_detectionEfficencyThreshold.py


Input:  1. file 'oiftrestoutput' 


Action: 1. count lines from raw output
        2. count lines after applying filter
        3. see if threshold is statistically solid
        
Author: Grigori Fedorets
"""


def test_PPDetectionEfficiency():

    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPDetectionEfficiency import PPDetectionEfficiency

    padafr = PPReadOif('./data/test/oiftestoutput.txt', 'whitespace')
    nrows = len(padafr.index)
    pada1 = PPDetectionEfficiency(padafr, 1.00)
    nr1 = len(pada1.index)
    pada2 = PPDetectionEfficiency(padafr, 0.00)
    nr2 = len(pada2.index)

    assert nr1 == nrows
    assert nr2 == 0

    return
