#!/bin/python

import pytest
import pandas as pd
#from filtering import PPFilterDetectionEfficiencyThreshold

from ..PPReadOif import PPReadOif
from ..PPFilterDetectionEfficiencyThreshold import PPFilterDetectionEfficiencyThreshold

"""
test_detectionEfficencyThreshold.py


Input:  1. file 'oiftrestoutput' 


Action: 1. count lines from raw output
        2. count lines after applying filter
        3. see if threshold is statistically solid
        
Author: Grigori Fedorets
"""

def test_PPFilterDetectionEfficiencyThreshold():

    padafr=PPReadOif('./data/test/oiftestoutput.txt', ' ')
    nrows=len(padafr.index)
    pada1=PPFilterDetectionEfficiencyThreshold(padafr,1.00)
    nr1=len(pada1.index)
    pada2=PPFilterDetectionEfficiencyThreshold(padafr,0.00)
    nr2=len(pada2.index)
    
    assert nr1 == nrows
    assert nr2 == 0
    
    return

    
