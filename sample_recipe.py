#!/usr/bin/python


import os,sys
import pandas as pd
#from filtering import PPFilterDetectionEfficiencyThreshold
from modules import PPFilterDetectionEfficiencyThreshold, PPreadColoursUser, PPreadColours
from modules import PPhookBrightnessWithColour, PPJoinColourPointing, PPMatchPointing 
from modules import PPMatchPointingsAndColours, PPFilterSSPCriterionEfficiency


import readOif, PPConfig
#import readColours
#from magnitude import PPreadColoursUser, PPreadColours, PPhookBrightnessWithColour


#oifoutput=sys.argv[1]

# Read config file
oifoutput=PPConfig.oifoutput
colourinput=PPConfig.colourinput
pointingdatabase=PPConfig.pointingdatabase
SSPDetectionEfficiency=PPConfig.SSPDetectionEfficiency

if (PPConfig.verbosity>0):
   print('Reading input pointing history: ', oifoutput)
padafr=readOif.readOif(oifoutput)

if (PPConfig.verbosity>0):
   print('Reading input colours: ', colourinput)
padacl=PPreadColours.PPreadColours(colourinput)


#print('padafr')
#print(padafr)
#print(padacl)
#resdf=pd.concat([padafr,padacl], axis=1, join='inner', keys='ObjID')
if (PPConfig.verbosity>0):
    print('Joining colour data with pointing data...')
resdf=PPJoinColourPointing.PPJoinColourPointing(padafr,padacl)

#resdf=padafr.join(padacl.set_index('ObjID'), on='ObjID')
#print(resdf)

if (PPConfig.verbosity>0):
    print('Applying detection efficiency threshold...')
pada1=PPFilterDetectionEfficiencyThreshold.PPFilterDetectionEfficiencyThreshold(padafr,SSPDetectionEfficiency)


#print(pada1)
#pada2=PPreadColoursUser.PPreadColoursUser(pada1, 'g-X', 0.33, 0.01)
#pada3=PPreadColoursUser.PPreadColoursUser(pada1, 'r-i', 0.25, 0.00, indataf=pada2)

if (PPConfig.verbosity>0):
    print('Hooking colour and brightness information...')
resdf1=PPhookBrightnessWithColour.PPhookBrightnessWithColour(resdf, 'V', 'i-r', 'i')
#resdf2=PPhookBrightnessWithColour.PPhookBrightnessWithColour(resdf1, 'V', 'r-r', 'r')
resdf3=PPhookBrightnessWithColour.PPhookBrightnessWithColour(resdf1, 'V', 'g-X', 'g')
#resdf4=PPhookBrightnessWithColour.PPhookBrightnessWithColour(resdf3, 'V', 'z-r', 'z')



#print('pada2')
#print(pada2)
#print('pada3')
#print(pada3)
#print('pada4')
#print(pada4)
if (PPConfig.verbosity>0):
    print('Matching observationID with appropriate filter...')
pada5=PPMatchPointing.PPMatchPointing(pointingdatabase)
#print(pada5)
if (PPConfig.verbosity>0):
    print('Matching pointings with filters...')
pada6=PPMatchPointingsAndColours.PPMatchPointingsAndColours(resdf3,pada5)
#print(pada6.columns)


#print(pada6)


pada7=PPFilterSSPCriterionEfficiency.PPFilterSSPCriterionEfficiency(pada6)
print(pada7)