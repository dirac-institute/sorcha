#!/bin/python

import pytest
import pandas as pd

from ..PPReadOif import PPReadOif
from ..PPhookBrightnessWithColour import PPhookBrightnessWithColour
from ..PPReadColours import PPReadColours
from ..PPJoinColourPointing import PPJoinColourPointing



def test_PPhookBrightnessWithColour():

    padafr=PPReadOif('./data/test/oiftestoutput.txt', ' ')
    padacl=PPReadColours('./data/test/testcolour.txt', 0, 5, ' ')

    resdf=PPJoinColourPointing(padafr,padacl)
    ncols=len(resdf.columns)    
    
    resdf1=PPhookBrightnessWithColour(resdf, 'V', 'i-r', 'i')
    ncols1=len(resdf1.columns)


    ncolscomp=ncols+1
    
    assert ncolscomp == ncols1
    return
