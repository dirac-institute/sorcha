#!/bin/python

import pytest
import pandas as pd

from ..PPReadOif import PPReadOif
from ..PPReadBrightness import PPReadBrightness
from ..PPJoinColourPointing import PPJoinColourPointing
from ..PPCalculateApparentMagnitude import PPCalculateApparentMagnitude


def test_PPCalculateApparentMagnitude():
     
     rescol=17.599933
     
     padafr=PPReadOif('./data/test/oiftestoutput', " ")
     padabr=PPReadBrightness('./data/test/testbrightness', 0, 3, " ")
     
     padain=PPJoinColourPointing(padafr,padabr)
     
     padaw=PPCalculateApparentMagnitude(padain, 'HG', 'r')
     
     val=padaw.at[0,'r']
     
     assert rescol==pytest.approx(val,0.00001)
     
     return
     