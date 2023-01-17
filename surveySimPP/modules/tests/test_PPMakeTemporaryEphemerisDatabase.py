#!/bin/python

import sqlite3
import os

from surveySimPP.tests.data import get_test_filepath


def test_PPMakeTemporaryEphemerisDatabase(tmp_path):

    from surveySimPP.modules.PPMakeTemporaryEphemerisDatabase import PPMakeTemporaryEphemerisDatabase

    temp_path = os.path.dirname(get_test_filepath('oiftestoutput.txt'))
    stem_name = ('testdb_PPIntermDB')
    daba = PPMakeTemporaryEphemerisDatabase(get_test_filepath('oiftestoutput.txt'), temp_path, 'whitespace', stemname=stem_name)

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
