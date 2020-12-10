#!/bin/python

import pytest
import pandas as pd

from ..PPJoinColourPointing import PPJoinColourPointing
from ..PPhookBrightnessWithColour import PPhookBrightnessWithColour
from ..readOif import readOif
from ..PPreadColours import PPreadColours
from ..PPMatchPointing import PPMatchPointing





def test_PPMatchPointingAndColours():

    padafr=readOif('oiftestoutput')
    padacl=PPreadColours.PPreadColours('testcolour')
    
    resdf=PPJoinColourPointing.PPJoinColourPointing(padafr,padacl)
    
    
    resdf1=PPhookBrightnessWithColour.PPhookBrightnessWithColour(resdf, 'V', 'i-r', 'i')
    resdf3=PPhookBrightnessWithColour.PPhookBrightnessWithColour(resdf1, 'V', 'g-X', 'g')
    
    
    pada5=PPMatchPointing.PPMatchPointing('baseline_10yrs_10klines.db')
    pada6=PPMatchPointingsAndColours.PPMatchPointingsAndColours(resdf3,pada5)
    
    ncols=30
    ncolsre=len(pada6.columns)
    
    assert ncols==ncolsre
    return     
         