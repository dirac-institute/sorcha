#!/bin/python

import pytest
import pandas as pd

from ..PPReadOrbitFile import PPReadOrbitFile


def test_PPReadOrbitFile():
     
     rescol=14
     
     padafr=PPReadOrbitFile('./data/test/testorb.des', 0, 14)
     val=len(padafr.columns)
     
     assert rescol==val
     
     return
     