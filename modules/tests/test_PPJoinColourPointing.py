#!/bin/python

import pytest
import pandas as pd

from ..PPJoinColourPointing import PPJoinColourPointing
from ..PPReadOif import PPReadOif
from ..PPReadColours import PPReadColours


def test_PPJoinColourPointing():

    padafr=PPReadOif('./data/test/oiftestoutput.txt', 'whitespace')
    padacl=PPReadColours('./data/test/testcolour.txt', 0, 5, ' ')
    
    padare=PPJoinColourPointing(padafr,padacl)
    
    ncol=27
    ncolre=len(padare.columns)
    
    assert ncol==ncolre
    return
