#!/bin/python

import pytest
import pandas as pd

from ..PPJoinColourPointing import PPJoinColourPointing
from ..readOif import readOif
from ..PPreadColours import PPreadColours


def test_PPJoinColourPointing():

    padafr=readOif('./data/test/oiftestoutput')
    padacl=PPreadColours('./data/test/testcolour')
    
    padare=PPJoinColourPointing(padafr,padacl)
    
    ncol=28
    ncolre=len(padare.columns)
    
    assert ncol==ncolre
    return
