#!/bin/python

import pytest
import pandas as pd

from surveySimPP.tests.data import get_test_filepath


def test_PPReadCometaryInput():

    from surveySimPP.modules.PPReadCometaryInput import PPReadCometaryInput

    rescol = 1552

    padafr = PPReadCometaryInput(get_test_filepath('testcomet.txt'), 0, 1, "whitespace")
    val = padafr.at[0, 'afrho1']

    assert rescol == val

    return
