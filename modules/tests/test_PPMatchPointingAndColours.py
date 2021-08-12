#!/bin/python

import pytest
import pandas as pd

from ..PPJoinColourPointing import PPJoinColourPointing
from ..PPhookBrightnessWithColour import PPhookBrightnessWithColour
from ..PPReadOif import PPReadOif
from ..PPReadColours import PPReadColours
from ..PPMatchPointing import PPMatchPointing
from ..PPMatchPointingsAndColours import PPMatchPointingsAndColours




def test_PPMatchPointingAndColours():

    padafr=PPReadOif('./data/test/oiftestoutput.txt', ' ')
    padacl=PPReadColours('./data/test/testcolour.txt', 0, 5, ' ')
    
    resdf=PPJoinColourPointing(padafr,padacl)
    
    
    resdf1=PPhookBrightnessWithColour(resdf, 'r', 'i-r', 'i')
    resdf3=PPhookBrightnessWithColour(resdf1, 'r', 'g-r', 'g')
    
    
    pada5=PPMatchPointing('./data/test/baseline_10yrs_10klines.db', ['u', 'g', 'r', 'i', 'z'])
    pada6=PPMatchPointingsAndColours(resdf3,pada5)
    
    ncols=32
    ncolsre=len(pada6.columns)
    
    assert ncols==ncolsre
    return     
         