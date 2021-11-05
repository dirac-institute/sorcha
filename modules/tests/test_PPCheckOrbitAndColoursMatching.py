#!/bin/python

import pytest
import pandas as pd

from ..PPReadOrbitFile import PPReadOrbitFile
from ..PPReadColours import PPReadColours
from ..PPCheckOrbitAndColoursMatching import PPCheckOrbitAndColoursMatching
from ..PPReadOif import PPReadOif


def test_PPCheckOrbitAndColoursMatching():
     
     compval=1
     
     padaor=PPReadOrbitFile('./data/test/testorb.des', 0, 10, ' ')
     padacl=PPReadColours('./data/test/testcolour.txt', 0, 10, ' ')
     padapo=PPReadOif('./data/test/oiftestoutput.txt', ' ', 'txt')
     
     print(padaor)
     print(padacl)
     print(padapo)
     
     
     try:
        PPCheckOrbitAndColoursMatching(padaor,padacl,padapo)
        ret=1
     except:
        ret=0
     
     
     
     assert ret==compval
     
     return