#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPReadOrbitFile():
    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile
    rescol = 9

    padafr = PPReadOrbitFile(get_test_filepath('testorb.des'), 0, 14, "whitespace")
    val = len(padafr.columns)

    assert rescol == val

    return
