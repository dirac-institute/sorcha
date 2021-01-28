#!/bin/python

import pytest
import pandas as pd

from ..PPReadOrbitFile import PPReadOrbitFile
from ..PPreadColours import PPreadColours
from ..PPCheckOrbitAndColoursMatching import PPCheckOrbitAndColoursMatching


def test_PPCheckOrbitAndColoursMatching():
     
     compval=1
     
     padaor=PPReadOrbitFile('./data/test/testorb.des')
     padacl=PPreadColours('./data/test/testcolour')
     
     try:
        PPCheckOrbitAndColoursMatching(padaor,padacl)
        ret=1
     except:
        ret=0
     
     
     
     assert ret==compval
     
     return