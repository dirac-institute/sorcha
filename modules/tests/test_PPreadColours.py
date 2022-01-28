#!/bin/python

import pytest
import pandas as pd

from ..PPReadColours import PPReadColours


def test_PPReadColours():
     
     rescol=0.3
     
     padafr=PPReadColours('./data/test/testcolour.txt', 0, 3, "whitespace")
     val=padafr.at[0,'g-r']
     
     assert rescol==val
     
     return
     