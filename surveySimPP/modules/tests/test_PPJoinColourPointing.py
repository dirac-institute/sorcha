#!/bin/python

import pytest
import pandas as pd


def test_PPJoinColourPointing():

    from surveySimPP.modules.PPJoinColourPointing import PPJoinColourPointing
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadColours import PPReadColours

    padafr = PPReadOif('./data/test/oiftestoutput.txt', 'whitespace')
    padacl = PPReadColours('./data/test/testcolour.txt', 0, 5, 'whitespace')

    padare = PPJoinColourPointing(padafr, padacl)

    ncol = 27
    ncolre = len(padare.columns)

    assert ncol == ncolre
    return
