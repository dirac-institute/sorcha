# OBSOLETE!
#
#!/bin/python
#
#import pytest
#import pandas as pd
##from filtering import PPFilterDetectionEfficiencyThreshold
#
#from ..readOif import readOif
#from ..PPhookBrightnessWithColour import PPhookBrightnessWithColour
#from ..PPreadColours import PPreadColours
#from ..PPresolveFilters import PPresolveFilters
#
#"""
#test_PPresolveFilters.py
#
#
#Input:  1. file 'oiftrestoutput' 
#        2. file 'testcolour'
#
#
#ction: 1. count lines from raw output
#        2. count lines after applying action, one line added
#        3. see if number of columns mqtches the predicted one
#        
#Author: Grigori Fedorets
#"""
#
#
#
#
#def test_PPresolveFilters():
#
#    padafr=readOif('oiftestoutput')
#    padacl=PPreadColours('testcolour')
#    ncols=len(padafr.columns)
#    ncolscomp=ncols+1
#    
#    pada1=PPhookBrightnessWithColour(padafr, 'V', 'i-r', 'r')
#    ncols1=len(pada1.columns)
#    
#    assert ncolscomp == ncols1
#    return
#