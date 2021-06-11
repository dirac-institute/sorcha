#!/bin/python

import pytest
import pandas as pd
import os, sys

from ..PPJoinColourPointing import PPJoinColourPointing
from ..PPhookBrightnessWithColour import PPhookBrightnessWithColour
from ..PPReadOif import PPReadOif
from ..PPReadColours import PPReadColours
from ..PPMatchPointing import PPMatchPointing
from ..PPMatchPointingsAndColours import PPMatchPointingsAndColours
from ..PPOutWriteCSV import PPOutWriteCSV



def test_PPOutWriteCSV():

    padafr=PPReadOif('./data/test/oiftestoutput', " ")
    padacl=PPReadColours('./data/test/testcolour', 0, 5, " ")
    
    resdf=PPJoinColourPointing(padafr,padacl)
    
    
    resdf1=PPhookBrightnessWithColour(resdf, 'r', 'i-r', 'i')
    resdf3=PPhookBrightnessWithColour(resdf1, 'r', 'g-r', 'g')
    
    
    pada5=PPMatchPointing('./data/baseline_10yrs_10klines.db')
    pada6=PPMatchPointingsAndColours(resdf3,pada5)
    
    
    pada7=PPOutWriteCSV(pada6,'./outtest.csv')
    ncols=10
    
    tpt=os.popen("wc -l ./outtest.csv | awk '{print $1}'")
    cmp=tpt.read()
    cmp.strip()
    cmp1=int(cmp)
    os.system("rm ./outtest.csv")
    
    #ncolsre=len(pada6.columns)
    
    assert ncols==cmp1
    return     
         