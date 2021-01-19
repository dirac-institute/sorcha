#!/bin/python

import pytest
import pandas as pd
#from filtering import PPFilterDetectionEfficiencyThreshold

from ..readOif import readOif
from ..PPhookBrightnessWithColour import PPhookBrightnessWithColour
from ..PPreadColours import PPreadColours
from ..PPJoinColourPointing import PPJoinColourPointing


"""
test_PPresolveFilters.py


Input:  1. file 'oiftrestoutput' 


Action: 1. count lines from raw output
        2. count lines after applying action, one line added
        3. see if number of columns mqtches the predicted one
        
Author: Grigori Fedorets
"""




def test_PPhookBrightnessWithColour():

    padafr=readOif('./data/test/oiftestoutput')
    padacl=PPreadColours('./data/test/testcolour')

    resdf=PPJoinColourPointing(padafr,padacl)
    ncols=len(resdf.columns)    
    
    resdf1=PPhookBrightnessWithColour(resdf, 'V', 'i-r', 'i')
    ncols1=len(resdf1.columns)


    ncolscomp=ncols+1
    


    
    assert ncolscomp == ncols1
    return
