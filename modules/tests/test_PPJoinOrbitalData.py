#!/bin/python

import pytest
import pandas as pd

from ..PPJoinOrbitalData import PPJoinOrbitalData
from ..PPJoinColourPointing import PPJoinColourPointing
from ..PPReadOif import PPReadOif
from ..PPReadColours import PPReadColours
from ..PPReadOrbitFile import PPReadOrbitFile


def test_PPJoinCOrbitalData():

    padafr=PPReadOif('./data/test/oiftestoutput.txt', "whitespace")
    padacl=PPReadColours('./data/test/testcolour.txt', 0, 5, "whitespace")
    padaor=PPReadOrbitFile('./data/test/testorb.des', 0, 5, "whitespace")
    
    padain=PPJoinColourPointing(padafr,padacl)
    padare=PPJoinOrbitalData(padain, padaor)
    
    ncol=36
    ncolre=len(padare.columns)
    
    assert ncol==ncolre
    return