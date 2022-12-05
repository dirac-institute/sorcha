#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPReadCometaryParameters():

    from surveySimPP.modules.PPReadCometaryParameters import PPReadCometaryParameters

    rescol = 1552

    padafr = PPReadCometaryParameters(get_test_filepath('testcomet.txt'), 0, 1, "whitespace")
    val = padafr.at[0, 'afrho1']

    assert rescol == val

    return
