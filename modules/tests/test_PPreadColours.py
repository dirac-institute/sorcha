#!/bin/python

import pytest
import pandas as pd

from ..PPreadColours import PPreadColours


def test_PPreadColours():
     
     rescol=0.3
     
     padafr=PPreadColours('./data/test/testcolour')
     val=padafr.at[0,'g-r']
     
     assert rescol==val
     
     return
     