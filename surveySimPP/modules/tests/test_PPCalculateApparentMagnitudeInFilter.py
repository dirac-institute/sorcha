#!/bin/python
#
#import pytest
#import pandas as pd
#
#from ..PPReadOif import PPReadOif
#from ..PPReadOrbitFile import PPReadOrbitFile
#from ..PPReadColours import PPReadColours
#from ..PPJoinOrbitalData import PPJoinOrbitalData
#from ..PPJoinColourPointing import PPJoinColourPointing
#from ..PPCalculateApparentMagnitudeInFilter import PPCalculateApparentMagnitudeInFilter
#
#
#def test_PPCalculateApparentMagnitudeInFilter():
#     
#     rescol=24.001402
#     
#     padafr=PPReadOif('./data/test/67P.out', "whitespace")
#     padacl=PPReadColours('./data/test/testcometcolour.txt', 0, 3, 'whitespace')
#     padaor=PPReadOrbitFile('./data/test/67P.orb.des', 0, 3, 'whitespace')
#     
#     
#     resdf1=PPJoinColourPointing(padafr,padacl)
#     resdf2=PPJoinOrbitalData(resdf1,padaor)
#          
#     padaw=PPCalculateApparentMagnitudeInFilter(resdf2, 'HG', 'r')
#     
#     val=padaw.at[0,'r']
#     
#     assert rescol==pytest.approx(val,0.00001)
#     
#     return
#     