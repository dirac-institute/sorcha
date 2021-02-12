#!/bin/python

import pytest
import pandas as pd

from ..PPReadOrbitFile import PPReadOrbitFile
from ..PPreadColours import PPreadColours
from ..PPCheckOrbitAndColoursMatching import PPCheckOrbitAndColoursMatching
from ..readOif import readOif


def test_PPCheckOrbitAndColoursMatching():
     
     compval=1
     
     padaor=PPReadOrbitFile('./data/test/testorb.des')
     padacl=PPreadColours('./data/test/testcolour')
     padapo=readOif('./data/test/oiftestoutput')
     
     try:
        PPCheckOrbitAndColoursMatching(padaor,padacl,padapo)
        ret=1
     except:
        ret=0
     
     
     
     assert ret==compval
     
     return