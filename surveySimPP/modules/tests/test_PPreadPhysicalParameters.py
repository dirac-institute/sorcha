#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPReadPhysicalParameters():
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    rescol = 0.3

    padafr = PPReadPhysicalParameters(get_test_filepath('testcolour.txt'), ['g-r', 'i-r', 'z-r'], 0, 3, "whitespace")
    val = padafr.at[0, 'g-r']

    assert rescol == val

    return
