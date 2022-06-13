#!/bin/python

import pytest
import pandas as pd
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord

from surveySimPP.tests.data import get_test_filepath


def test_PPFilterSSPLinking():

    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPFilterSSPLinking import PPFilterSSPLinking

    padafr = PPReadOif(get_test_filepath('oiftestoutput.txt'), 'whitespace')
    
    rng = np.random.default_rng(2021)
    
    print(padafr)
    padaout = PPFilterSSPLinking(padafr, 1, 2, 1, 15.0, 1.0, rng)
    print(padaout)
    nlc = 6
    nlco = len(padaout.index)

    assert nlc == nlco
    return
