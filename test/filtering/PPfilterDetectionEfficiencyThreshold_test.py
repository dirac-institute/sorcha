#!/bin/python

import pandas as pd
from filtering import PPFilterDetectionEfficiencyThreshold
import readOif

"""
detectionEfficencyThreshold_test.py


Input:  1. file 'oiftrestoutput' 


Action: 1. count lines from raw output
        2. count lines after applying filter
        3. see if threshold is statistically solid
        
Output: 1 if passes test, 0 if not

Author: Grigori Fedorets
"""



padafr=read_oif.read_oif('oiftestoutput')
nrows=len(padafr.index)
pada1=PPFilterDetectionEfficiencyThreshold.PPFilterDetectionEfficiencyThreshold(padafr,1.00)
nr1=len(pada1.index)
pada2=PPFilterDetectionEfficiencyThreshold.PPFilterDetectionEfficiencyThreshold(padafr,0.00)
nr2=len(pada2.index)

retint=0
if(nr1==nrows and nr2==0):
    retint=1
print(retint)    
    
