#!/bin/python

import pytest
import pandas as pd


def test_PPJoinPhysicalParametersPointing():

    from surveySimPP.modules.PPJoinPhysicalParametersPointing import PPJoinPhysicalParametersPointing
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters

    padafr = PPReadOif('./data/test/oiftestoutput.txt', 'whitespace')
    padacl = PPReadPhysicalParameters('./data/test/testcolour.txt', 0, 5, 'whitespace')

    padare = PPJoinPhysicalParametersPointing(padafr, padacl)

    ncol = 27
    ncolre = len(padare.columns)

    assert ncol == ncolre
    return
