#!/bin/python

import pytest
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord


def test_PPFilterSSPCriterionEfficiency():

    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPFilterSSPCriterionEfficiency import PPFilterSSPCriterionEfficiency

    padafr = PPReadOif('./data/test/oiftestoutput.txt', 'whitespace')
    print(padafr)
    padaout = PPFilterSSPCriterionEfficiency(padafr, 1, 2, 1, 15.0, 1.0)
    print(padaout)
    nlc = 6
    nlco = len(padaout.index)

    assert nlc == nlco
    return
