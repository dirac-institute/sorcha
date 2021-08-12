#!/bin/python

import pytest
import pandas as pd

from ..PPReadBrightness import PPReadBrightness


def test_PPReadBrightness():
     
     rescol=0.15
     
     padafr=PPReadBrightness('./data/test/testbrightness.txt', 0, 3, " ")
     val=padafr.at[0,'G']
     
     assert rescol==val
     
     return
     