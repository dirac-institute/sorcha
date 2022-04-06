#!/bin/python

import pytest
import pandas as pd


def test_PPReadColours():
    from surveySimPP.modules.PPReadColours import PPReadColours
    rescol = 0.3

    padafr = PPReadColours('./data/test/testcolour.txt', 0, 3, "whitespace")
    val = padafr.at[0, 'g-r']

    assert rescol == val

    return
