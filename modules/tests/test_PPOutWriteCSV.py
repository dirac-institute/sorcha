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

    padafr=PPReadOif('./data/test/oiftestoutput.txt', " ", 'txt')
    padacl=PPReadColours('./data/test/testcolour.txt', 0, 5, " ")
    
    resdf=PPJoinColourPointing(padafr,padacl)
    
    
    resdf1=PPhookBrightnessWithColour(resdf, 'r', 'i-r', 'i')
    resdf3=PPhookBrightnessWithColour(resdf1, 'r', 'g-r', 'g')
    
    
    pada5=PPMatchPointing('./data/test/baseline_10yrs_10klines.db', [ 'g', 'r', 'i'])
    pada6=PPMatchPointingsAndColours(resdf3,pada5)
    
    
    pada7=PPOutWriteCSV(pada6,'./outtest.csv')
    ncols=6
    
    tpt=os.popen("wc -l ./outtest.csv | awk '{print $1}'")
    cmp=tpt.read()
    cmp.strip()
    cmp1=int(cmp)
    os.system("rm ./outtest.csv")
    
    #ncolsre=len(pada6.columns)
    
    assert ncols==cmp1
    return     
         