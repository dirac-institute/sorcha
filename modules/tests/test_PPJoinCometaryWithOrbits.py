#!/bin/python

import pytest
import pandas as pd

from ..PPJoinCometaryWithOrbits import PPJoinCometaryWithOrbits
from ..PPJoinColourPointing import PPJoinColourPointing
from ..PPReadOif import PPReadOif
from ..PPReadColours import PPReadColours
from ..PPReadOrbitFile import PPReadOrbitFile


def test_PPJoinCometaryWithOrbits():

    padafr=PPReadOif('./data/test/oiftestoutput.txt', "whitespace")
    padacl=PPReadColours('./data/test/testcolour.txt', 0, 5, " ")
    padaor=PPReadOrbitFile('./data/test/testorb.des', 0, 5, " ")
    
    padain=PPJoinColourPointing(padafr,padacl)
    padare=PPJoinCometaryWithOrbits(padain, padaor)
    
    ncol=35
    ncolre=len(padare.columns)
    
    assert ncol==ncolre
    return