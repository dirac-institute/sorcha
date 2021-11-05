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
from ..PPOutWriteHDF5 import PPOutWriteHDF5



def test_PPOutWriteHDF5():


    padafr=PPReadOif('./data/test/oiftestoutput.txt', " ", 'txt')
    padacl=PPReadColours('./data/test/testcolour.txt', 0, 20, " ")
    
    resdf=PPJoinColourPointing(padafr,padacl)
    
    
    resdf1=PPhookBrightnessWithColour(resdf, 'r', 'i-r', 'i')
    resdf3=PPhookBrightnessWithColour(resdf1, 'r', 'g-r', 'g')
    
    
    pada5=PPMatchPointing('./data/test/baseline_10yrs_10klines.db', ['r', 'g', 'i'])
    pada6=PPMatchPointingsAndColours(resdf3,pada5)
    
    
    pada7=PPOutWriteHDF5(pada6,'outtest.h5',str(1))
    
    pd.read_hdf('outtest.h5', str(1)).dtypes

    
    ncols=5
    
    print(pada6)
    
    rer=pd.read_hdf('outtest.h5')
    
    nrs=len(rer.index)

    os.system("rm outtest.h5")

    
    #ncolsre=len(pada6.columns)
    
    assert ncols==nrs
    return     
         