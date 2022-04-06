#!/bin/python

import pytest
import pandas as pd


def test_PPCheckOrbitAndPhysicalParametersMatching():

    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    from surveySimPP.modules.PPCheckOrbitAndPhysicalParametersMatching import PPCheckOrbitAndPhysicalParametersMatching
    from surveySimPP.modules.PPReadOif import PPReadOif

    compval = 1

    padaor = PPReadOrbitFile('./data/test/testorb.des', 0, 10, 'whitespace')
    padacl = PPReadPhysicalParameters('./data/test/testcolour.txt', 0, 10, 'whitespace')
    padapo = PPReadOif('./data/test/oiftestoutput.txt', 'whitespace')

    print(padaor)
    print(padacl)
    print(padapo)

    try:
        PPCheckOrbitAndPhysicalParametersMatching(padaor, padacl, padapo)
        ret = 1
    except:
        ret = 0

    assert ret == compval

    return
