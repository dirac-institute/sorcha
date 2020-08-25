#!/usr/bin/python

import pandas as pd
from filtering import PPFilterDetectionEfficiencyThreshold
import readOif


padafr=readOif.readOif('oiftestoutput')
print(padafr)
pada1=PPFilterDetectionEfficiencyThreshold.PPFilterDetectionEfficiencyThreshold(padafr,0.95)
print(pada1)