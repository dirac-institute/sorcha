#!/bin/python

import pytest
import pandas as pd


def test_PPJoinCOrbitalData():

    from surveySimPP.modules.PPJoinOrbitalData import PPJoinOrbitalData
    from surveySimPP.modules.PPJoinPhysicalParametersPointing import PPJoinPhysicalParametersPointing
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile

    padafr = PPReadOif('./data/test/oiftestoutput.txt', "whitespace")
    padacl = PPReadPhysicalParameters('./data/test/testcolour.txt', 0, 5, "whitespace")
    padaor = PPReadOrbitFile('./data/test/testorb.des', 0, 5, "whitespace")

    padain = PPJoinPhysicalParametersPointing(padafr, padacl)
    padare = PPJoinOrbitalData(padain, padaor)

    ncol = 36
    ncolre = len(padare.columns)

    assert ncol == ncolre
    return
