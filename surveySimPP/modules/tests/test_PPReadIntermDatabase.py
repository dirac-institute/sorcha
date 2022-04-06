#!/bin/python

import pytest
import pandas as pd
import sqlite3


def test_PPReadIntermDatabase():

    from surveySimPP.modules.PPMakeIntermediatePointingDatabase import PPMakeIntermediatePointingDatabase
    from surveySimPP.modules.PPReadIntermDatabase import PPReadIntermDatabase
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    padacl = PPReadPhysicalParameters('./data/test/testcolour.txt', 0, 5, 'whitespace')
    print(padacl)
    objid_list = padacl['ObjID'].unique().tolist()

    daba = PPMakeIntermediatePointingDatabase('./data/test/oiftestoutput.txt', './data/test/testdb_PPIntermDB.db', 10)

    padafr = PPReadIntermDatabase('./data/test/testdb_PPIntermDB.db', objid_list)

    nlines = 9

    nlinesdb = len(padafr.index)

    assert nlines == nlinesdb
    return
