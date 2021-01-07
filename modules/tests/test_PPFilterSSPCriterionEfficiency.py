#!/bin/python

import pytest
import pandas as pd

from ..readOif import readOif
from ..PPFilterSSPCriterionEfficiency import PPFilterSSPCriterionEfficiency




def test_PPFilterSSPCriterionEfficiency():

    padafr=readOif('./data/test/oiftestoutput')
    padaout=PPFilterSSPCriterionEfficiency(padafr)
    
    nlc=3
    nlco=len(padaout.index)
    
    assert nlc==nlco
    return