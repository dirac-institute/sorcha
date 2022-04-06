#!/bin/python

import pytest
import pandas as pd


def test_PPReadOrbitFile():
    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile
    rescol = 10

    padafr = PPReadOrbitFile('./data/test/testorb.des', 0, 14, "whitespace")
    val = len(padafr.columns)

    assert rescol == val

    return
