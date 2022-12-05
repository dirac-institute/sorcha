#!/bin/python

import sqlite3

from surveySimPP.tests.data import get_test_filepath


def test_PPMakeTemporaryEphemerisDatabase(tmp_path):

    from surveySimPP.modules.PPMakeTemporaryEphemerisDatabase import PPMakeTemporaryEphemerisDatabase

    testdb = str(tmp_path / "testdb_PPIntermDB.db")
    daba = PPMakeTemporaryEphemerisDatabase(get_test_filepath('oiftestoutput.txt'), testdb, 'whitespace')

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
