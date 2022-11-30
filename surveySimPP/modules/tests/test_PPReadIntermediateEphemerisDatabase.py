#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPReadIntermediateEphemerisDatabase(tmp_path):

    from surveySimPP.modules.PPMakeIntermediateEphemerisDatabase import PPMakeIntermediateEphemerisDatabase
    from surveySimPP.modules.PPReadIntermediateEphemerisDatabase import PPReadIntermediateEphemerisDatabase
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters

    padacl = PPReadPhysicalParameters(get_test_filepath('testcolour.txt'), ['g-r', 'i-r', 'z-r'], 0, 5, 'whitespace')
    print(padacl)
    objid_list = padacl['ObjID'].unique().tolist()

    testdb = str(tmp_path / "testdb_PPIntermDB.db")
    daba = PPMakeIntermediateEphemerisDatabase(get_test_filepath('oiftestoutput.txt'), testdb, 'whitespace')

    padafr = PPReadIntermediateEphemerisDatabase(daba, objid_list)

    nlines = 9

    nlinesdb = len(padafr.index)

    assert nlines == nlinesdb
    return
