#!/bin/python

import pytest
import pandas as pd
import sqlite3


def test_PPMakeIntermediatePointingDatabase():

    from surveySimPP.modules.PPMakeIntermediatePointingDatabase import PPMakeIntermediatePointingDatabase

    daba = PPMakeIntermediatePointingDatabase('./data/test/oiftestoutput.txt', './data/test/testdb_PPIntermDB.db', 10)

    nlines = 9

    cnx = sqlite3.connect(daba)

    cur = cnx.cursor()

    cmd = 'select count (*) from interm'
    cur.execute(cmd)

    nlinesdb = cur.fetchall()

    nlinesdb = nlinesdb[0]
    nlinesdb = nlinesdb[0]

    print(type(nlinesdb))

    assert nlines == nlinesdb
    return
