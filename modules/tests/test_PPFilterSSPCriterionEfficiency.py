#!/bin/python

import pytest
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord

from ..readOif import readOif
from ..PPFilterSSPCriterionEfficiency import PPFilterSSPCriterionEfficiency




def test_PPFilterSSPCriterionEfficiency():

    padafr=readOif('./data/test/oiftestoutput')
    padaout=PPFilterSSPCriterionEfficiency(padafr,2,1,15.0,0.5)
    print(padaout)
    nlc=6
    nlco=len(padaout.index)
    
    assert nlc==nlco
    return