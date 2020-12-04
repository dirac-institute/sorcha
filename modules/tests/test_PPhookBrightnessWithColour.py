#!/bin/python

import pytest
import pandas as pd
#from filtering import PPFilterDetectionEfficiencyThreshold

from ..readOif import readOif
from ..PPhookBrightnessWithColour import PPhookBrightnessWithColour

"""
test_PPresolveFilters.py


Input:  1. file 'oiftrestoutput' 


Action: 1. count lines from raw output
        2. count lines after applying action, one line added
        3. see if number of columns mqtches the predicted one
        
Author: Grigori Fedorets
"""




def test_PPhookBrightnessWithColour():

    padafr=readOif('oiftestoutput')
    ncols=len(padafr.columns)
    ncolscomp=ncols+1
    
    pada1=PPhookBrightnessWithColour(padafr, 'V', 'i-r', 'Vi')
    ncols1=len(pada1.columns)
    
    assert ncolscomp == ncols1
    return
