#!/bin/python

import pytest
import pandas as pd


def test_PPCalculateSimpleCometaryMagnitude():

    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadColours import PPReadColours
    from surveySimPP.modules.PPReadCometaryInput import PPReadCometaryInput
    from surveySimPP.modules.PPJoinColourPointing import PPJoinColourPointing
    from surveySimPP.modules.PPJoinOrbitalData import PPJoinOrbitalData
    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile
    from surveySimPP.modules.PPCalculateSimpleCometaryMagnitude import PPCalculateSimpleCometaryMagnitude

    padafr = PPReadOif('./data/test/67P.out', 'whitespace')
    padacl = PPReadColours('./data/test/testcometcolour.txt', 0, 3, 'whitespace')
    padaco = PPReadCometaryInput('./data/test/testcomet.txt', 0, 3, 'whitespace')
    padaor = PPReadOrbitFile('./data/test/67P.orb.des', 0, 3, 'whitespace')

    resdf1 = PPJoinColourPointing(padafr, padacl)
    resdf2 = PPJoinColourPointing(resdf1, padaco)
    resdf3 = PPJoinOrbitalData(resdf2, padaor)

    #resdf3['r'] = resdf3['V']

    ncols1 = len(resdf3.columns) + 3

    resdf = PPCalculateSimpleCometaryMagnitude(resdf3, 'r')

    ncols = len(resdf.columns)

    assert ncols == ncols1
    return
