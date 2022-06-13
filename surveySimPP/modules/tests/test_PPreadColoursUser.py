#!/bin/python

import pytest
import pandas as pd

from surveySimPP.tests.data import get_test_filepath


def test_PPreadColoursUser():

    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPreadColoursUser import PPreadColoursUser

    resval = 0.6

    padain = PPReadOif(get_test_filepath('oiftestoutput.txt'), "whitespace")
    padafr = PPreadColoursUser(padain, 'r-X', 0.6, 0.0)

    val = padafr.at[0, 'r-X']

    assert resval == val

    return
