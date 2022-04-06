#!/bin/python

import pytest
import pandas as pd


def test_PPReadPhysicalParameters():
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    rescol = 0.3

    padafr = PPReadPhysicalParameters('./data/test/testcolour.txt', 0, 3, "whitespace")
    val = padafr.at[0, 'g-r']

    assert rescol == val

    return
