#!/usr/bin/python

import pandas as pd
from filtering import PPFilterDetectionEfficiencyThreshold
import readOif
import readColours
from magnitude import readColoursUser

padafr=readOif.readOif('oiftestoutput')
padacl=PPreadColours.PPreadColours('testcolour')
print('padafr')
print(padafr)
print(padacl)
#resdf=pd.concat([padafr,padacl], axis=1, join='inner', keys='ObjID')
resdf=padafr.join(padacl.set_index('ObjID'), on='ObjID')
print(resdf)
pada1=PPFilterDetectionEfficiencyThreshold.PPFilterDetectionEfficiencyThreshold(padafr,0.95)
print(pada1)
pada2=PPreadColoursUser.PPreadColoursUser(pada1, 'g-X', 0.33, 0.01)
pada3=PPreadColoursUser.PPreadColoursUser(pada1, 'r-X', 0.25, 0.00, indataf=pada2)

print(pada2)
print('+++')
print(pada3)