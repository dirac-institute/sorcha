#!/bin/python

import pytest
import pandas as pd


def test_PPJoinCOrbitalData():

    from surveySimPP.modules.PPJoinOrbitalData import PPJoinOrbitalData
    from surveySimPP.modules.PPJoinColourPointing import PPJoinColourPointing
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadColours import PPReadColours
    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile

    padafr = PPReadOif('./data/test/oiftestoutput.txt', "whitespace")
    padacl = PPReadColours('./data/test/testcolour.txt', 0, 5, "whitespace")
    padaor = PPReadOrbitFile('./data/test/testorb.des', 0, 5, "whitespace")

    padain = PPJoinColourPointing(padafr, padacl)
    padare = PPJoinOrbitalData(padain, padaor)

    ncol = 36
    ncolre = len(padare.columns)

    assert ncol == ncolre
    return
