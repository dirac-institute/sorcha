#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPJoinCOrbitalData():

    from surveySimPP.modules.PPJoinOrbitalData import PPJoinOrbitalData
    from surveySimPP.modules.PPJoinPhysicalParametersPointing import PPJoinPhysicalParametersPointing
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile

    padafr = PPReadOif(get_test_filepath('oiftestoutput.txt'), "whitespace")
    padacl = PPReadPhysicalParameters(get_test_filepath('testcolour.txt'), ['g-r', 'i-r', 'z-r'], 0, 5, "whitespace")
    padaor = PPReadOrbitFile(get_test_filepath('testorb.des'), 0, 5, "whitespace")

    padain = PPJoinPhysicalParametersPointing(padafr, padacl)
    padare = PPJoinOrbitalData(padain, padaor)

    ncol = 35
    ncolre = len(padare.columns)

    assert ncol == ncolre
    return
