#!/bin/python

from surveySimPP.tests.data import get_test_filepath
import os


def test_PPReadTemporaryEphemerisDatabase(tmp_path):

    from surveySimPP.modules.PPMakeTemporaryEphemerisDatabase import PPMakeTemporaryEphemerisDatabase
    from surveySimPP.modules.PPReadTemporaryEphemerisDatabase import PPReadTemporaryEphemerisDatabase
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters

    padacl = PPReadPhysicalParameters(get_test_filepath('testcolour.txt'), ['g-r', 'i-r', 'z-r'], 0, 5, 'whitespace')
    print(padacl)
    objid_list = padacl['ObjID'].unique().tolist()

    temp_path = os.path.dirname(get_test_filepath('oiftestoutput.txt'))
    stem_name = ('testdb_PPIntermDB')
    daba = PPMakeTemporaryEphemerisDatabase(get_test_filepath('oiftestoutput.txt'), temp_path, 'whitespace', stemname=stem_name)

    padafr = PPReadTemporaryEphemerisDatabase(daba, objid_list)

    nlines = 9

    nlinesdb = len(padafr.index)

    assert nlines == nlinesdb
    return
