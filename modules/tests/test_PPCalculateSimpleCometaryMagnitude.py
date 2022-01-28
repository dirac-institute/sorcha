#!/bin/python

import pytest
import pandas as pd

from ..PPReadOif import PPReadOif
from ..PPReadColours import PPReadColours
from ..PPReadCometaryInput import PPReadCometaryInput
from ..PPJoinColourPointing import PPJoinColourPointing
from ..PPJoinCometaryWithOrbits import PPJoinCometaryWithOrbits
from ..PPReadOrbitFile import PPReadOrbitFile 
from ..PPCalculateSimpleCometaryMagnitude import PPCalculateSimpleCometaryMagnitude



def test_PPCalculateSimpleCometaryMagnitude():

    padafr=PPReadOif('./data/test/67P.out', 'whitespace')
    padacl=PPReadColours('./data/test/testcometcolour.txt', 0, 3, 'whitespace')
    padaco=PPReadCometaryInput('./data/test/testcomet.txt', 0, 3, 'whitespace')
    padaor=PPReadOrbitFile('./data/test/67P.orb.des', 0, 3, 'whitespace')

    resdf1=PPJoinColourPointing(padafr,padacl)
    resdf2=PPJoinColourPointing(resdf1,padaco)
    resdf3=PPJoinCometaryWithOrbits(resdf2,padaor)
    
    resdf3['r'] = resdf3['V']

    ncols1=len(resdf3.columns) + 3
    
    resdf=PPCalculateSimpleCometaryMagnitude(resdf3,'r')
        
    ncols=len(resdf.columns)    

    
    assert ncols == ncols1
    return
