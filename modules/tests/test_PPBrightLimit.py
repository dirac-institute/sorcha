#!/bin/python

import pytest
import pandas as pd

from ..PPJoinColourPointing import PPJoinColourPointing
from ..PPhookBrightnessWithColour import PPhookBrightnessWithColour
from ..PPReadOif import PPReadOif
from ..PPReadColours import PPReadColours
from ..PPMatchPointing import PPMatchPointing
from ..PPMatchPointingsAndColours import PPMatchPointingsAndColours
from ..PPBrightLimit import PPBrightLimit



def test_PPBrightLimit():

    padafr=PPReadOif('./data/test/oiftestoutput')
    padacl=PPReadColours('./data/test/testcolour', 0, 5)
    
    resdf=PPJoinColourPointing(padafr,padacl)
    
    
    resdf1=PPhookBrightnessWithColour(resdf, 'r', 'i-r', 'i')
    resdf3=PPhookBrightnessWithColour(resdf1, 'r', 'g-r', 'g')
    
    
    pada5=PPMatchPointing('./data/baseline_10yrs_10klines.db')
    pada6=PPMatchPointingsAndColours(resdf3,pada5)
    
    print(pada6)
    
    pada7=PPBrightLimit(pada6,18.2)
    
    nros=7
    nrosre=len(pada7.index)
    
    assert nros==nrosre
    return     
     
     
