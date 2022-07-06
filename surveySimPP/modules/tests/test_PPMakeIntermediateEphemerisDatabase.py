#!/bin/python

import pytest
import pandas as pd
import sqlite3

from surveySimPP.tests.data import get_test_filepath


def test_PPMakeIntermediateEphemerisDatabase(tmp_path):

    from surveySimPP.modules.PPMakeIntermediateEphemerisDatabase import PPMakeIntermediateEphemerisDatabase

    testdb = str(tmp_path / "testdb_PPIntermDB.db")
    daba = PPMakeIntermediateEphemerisDatabase(get_test_filepath('oiftestoutput.txt'), testdb, 10)

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
