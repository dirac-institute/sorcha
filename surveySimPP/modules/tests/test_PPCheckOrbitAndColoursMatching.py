#!/bin/python

import pytest
import pandas as pd


def test_PPCheckOrbitAndColoursMatching():

    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile
    from surveySimPP.modules.PPReadColours import PPReadColours
    from surveySimPP.modules.PPCheckOrbitAndColoursMatching import PPCheckOrbitAndColoursMatching
    from surveySimPP.modules.PPReadOif import PPReadOif

    compval = 1

    padaor = PPReadOrbitFile('./data/test/testorb.des', 0, 10, 'whitespace')
    padacl = PPReadColours('./data/test/testcolour.txt', 0, 10, 'whitespace')
    padapo = PPReadOif('./data/test/oiftestoutput.txt', 'whitespace')

    print(padaor)
    print(padacl)
    print(padapo)

    try:
        PPCheckOrbitAndColoursMatching(padaor, padacl, padapo)
        ret = 1
    except:
        ret = 0

    assert ret == compval

    return
